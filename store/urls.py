from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    products_list,
    product,
    c_register,
    c_login,
    c_logout,
    cart,
    add_to_cart,
    update_cart,
    place_order,
    order_confirmation,
    reservation,
)

urlpatterns = [
    path("", products_list, name="products_list"),
    path("product/<int:product_id>/", product, name="product"),
    path("register/", c_register, name="register"),
    path("login/", c_login, name="login"),
    path("logout/", c_logout, name="logout"),
    path("cart/", cart, name="cart"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("update_cart/", update_cart, name="update_cart"),
    path("order/", place_order, name="order"),
    path("order_confirmation/", order_confirmation, name="order_confirmation"),
    path("reservation/", reservation, name="reservation"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
