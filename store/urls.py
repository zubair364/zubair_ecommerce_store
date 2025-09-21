from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("about/", views.about_us, name="about_us"),
    path("services/", views.services, name="services"),
]
