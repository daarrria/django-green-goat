from django.contrib import admin
from django.db.models import Sum
from .models import Category, Product, Client, Review, Order, OrderItem, Table, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category_name")
    list_filter = ("category__name",)
    search_fields = ("name", "description")

    def category_name(self, obj):
        return obj.category.name

    category_name.short_description = "Category"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product_name", "user", "rating", "date")
    list_filter = ("product__name", "user")
    search_fields = ("text",)

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Product"

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "date_joined")
    search_fields = ("username", "email")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "delivery_address",
        "preferred_delivery_time",
        "phone_number",
        "full_name",
        "order_date",
    )
    search_fields = ("user__username", "delivery_address", "phone_number", "full_name")
    list_filter = ("user", "order_date")
    inlines = [OrderItemInline]

    def get_total_price(self, obj):
        return obj.products.aggregate(total_price=Sum('orderitem__price'))['total_price']

    get_total_price.short_description = "Total Price"

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "seats",
        "shape",
        "horizontal_coordinate",
        "vertical_coordinate",
        "width_percentage",
        "length_percentage",
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("get_table_number", "date", "customer_name", "customer_email")

    def get_table_number(self, obj):
        return ", ".join(str(table.table.number) for table in obj.reserved_tables.all())

    get_table_number.short_description = "Table Number"