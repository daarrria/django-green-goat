from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import (
    Category,
    Product,
    Review,
    Order,
    OrderItem,
    Table,
    Reservation,
    ReservedTable
)
from .forms import (
    ClientCreationForm, 
    ClientAuthenticationForm, 
    ReviewForm
)
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from json import loads
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string

def c_register(request):
    if request.user.is_authenticated:
        return redirect("products_list")

    if request.method == "POST":
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Добро пожаловать в GREEN GOAT!'
            message = render_to_string('store/welcome_email_template.html', {
                'user': user,
                'domain': current_site.domain,
            })
            from_email = 'GREEN GOAT <greengoat1488@outlook.com>'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            login(request, user)
            return redirect("products_list")
    else:
        form = ClientCreationForm()
    return render(request, "store/auth/register.html", {"form": form})

def c_login(request):
    if request.user.is_authenticated:
        return redirect("products_list")

    if request.method == "POST":
        form = ClientAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get("next", "products_list")
            return redirect(next_url)
    else:
        form = ClientAuthenticationForm()
    return render(request, "store/auth/login.html", {"form": form})

@login_required
def c_logout(request):
    logout(request)
    return redirect("products_list")

def products_list(request):
    name_query = request.GET.get("name", "")
    category_filter = request.GET.get("category", "")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    products = Product.objects.all()

    if name_query:
        products = products.filter(name__icontains=name_query)

    if price_min is not None and price_min.isnumeric():
        products = products.filter(price__gte=price_min)

    if price_max is not None and price_max.isnumeric():
        products = products.filter(price__lte=price_max)

    if category_filter:
        products = products.filter(category__name__icontains=category_filter)

    categories_with_products = Category.objects.filter(
        product__in=products
    ).distinct()

    return render(
        request,
        "store/products.html",
        {
            "categories": categories_with_products,
            "products": products,
            "name_query": name_query,
            "category_filter": category_filter,
            "price_min": price_min,
            "price_max": price_max,
        },
    )

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product).order_by("-date")
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        reviews = reviews.exclude(user=request.user)

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            if not user_review:
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect("product", product_id=product_id)
    else:
        form = ReviewForm()
        
    if user_review:
        reviews = [user_review] + list(reviews)

    return render(
        request,
        "store/product.html",
        {
            "product": product,
            "reviews": reviews,
            "form": form,
            "user_review": user_review,
        },
    )

@login_required
def cart(request):
    cart_items = request.session.get("cart", {})

    products_in_cart = []
    total_price = Decimal(0)

    if isinstance(cart_items, dict):
        for item_id, quantity in cart_items.items():
            product = get_object_or_404(Product, pk=item_id)
            product_price = product.price * quantity
            total_price += product_price
            products_in_cart.append({"product": product, "quantity": quantity, "product_price": product_price})

    return render(request, "store/cart.html", {"products_in_cart": products_in_cart, "total_price": total_price})

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    if not isinstance(product_id, str):
        product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    next_url = request.POST.get("next", "/")
    return redirect(next_url)

@login_required
def update_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")

        cart = request.session.get("cart", {})

        if not isinstance(product_id, str):
            product_id = str(product_id)

        if product_id in cart:
            if action == "increase":
                cart[product_id] += 1
            elif action == "decrease":
                if cart[product_id] <= 1:
                    del cart[product_id]
                else:
                    cart[product_id] -= 1
            elif action == "remove":
                del cart[product_id]

        request.session["cart"] = cart

    return redirect("cart")

@login_required
def place_order(request):
    now = timezone.now()
    default_delivery_time = (now + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("products_list")

    if request.method == "POST":
        preferred_delivery_time = request.POST.get("preferred_delivery_time")

        preferred_delivery_time_datetime = timezone.datetime.strptime(preferred_delivery_time, '%Y-%m-%dT%H:%M')

        if preferred_delivery_time_datetime < now + timedelta(hours=1):
            preferred_delivery_time = default_delivery_time

        delivery_address = request.POST.get("delivery_address")
        phone_number = request.POST.get("phone_number")
        full_name = request.POST.get("full_name")

        order = Order.objects.create(
            user=request.user,
            delivery_address=delivery_address,
            preferred_delivery_time=preferred_delivery_time,
            phone_number=phone_number,
            full_name=full_name,
        )

        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        total_price = order.orderitem_set.aggregate(order_total_price=Sum('price'))['order_total_price']
        order.total_price = total_price
        order.save()

        request.session["cart"] = {}

        return render(request, "store/order_confirmation.html", {"order": order})

    return render(request, "store/order.html", {"default_delivery_time": default_delivery_time})

@login_required
def order_confirmation(request):
    return render(request, "store/order_confirmation.html")

def send_reservation_email(reservation):
    subject = 'Бронювання у GreenGoat'
    message = render_to_string('store/reservation_email_template.html', {'reservation': reservation})
    from_email = 'GREEN GOAT <greengoat8818662023@outlook.com>'
    recipient_list = [reservation.customer_email]

    send_mail(subject, message, from_email, recipient_list, html_message=message)

@login_required
def reservation(request):
    now = timezone.now()
    min_date = now.strftime('%Y-%m-%d')

    if request.method == "POST":
        selected_date = request.POST.get("date", datetime.now().strftime("%Y-%m-%d"))
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")

        if selected_date_obj.date() < datetime.now().date():
            return redirect('reservation')

        selected_tables = loads(request.POST.get("selected_tables", "[]"))

        if not are_tables_available(selected_tables, selected_date_obj):
            return redirect('reservation')

        customer_name = request.POST.get("customer_name")
        customer_email = request.POST.get("customer_email")

        reservation = Reservation.objects.create(
            date=selected_date_obj,
            customer_name=customer_name,
            customer_email=customer_email,
        )
        for table_id in selected_tables:
            ReservedTable.objects.create(reservation=reservation, table_id=table_id)
            
        send_reservation_email(reservation)

        return render(request, "store/reservation_confirmation.html", {"reservation": reservation})

    else:
        date = request.GET.get("date", datetime.now().strftime("%Y-%m-%d"))
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        if date_obj.date() < datetime.now().date():
            return redirect('reservation')

        tables = Table.objects.all()

        for table in tables:
            table.is_reserved = ReservedTable.objects.filter(
                table_id=table.id, reservation__date=date_obj
            ).exists()

        reservations = Reservation.objects.filter(date=date_obj)

        return render(
            request,
            "store/reservation.html",
            {"tables": tables, "reservations": reservations, "selected_date": date_obj, "min_date": min_date},
        )

def are_tables_available(selected_tables, selected_date_obj):
    reserved_tables = ReservedTable.objects.filter(
        table_id__in=selected_tables, reservation__date=selected_date_obj
    )
    return not reserved_tables.exists()