from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("books/<int:id>", views.book_page, name="book"),
    path("cart", views.cart, name="cart"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("change_amount/<int:id>", views.change_amount, name="change_amount"),
    path("purchase_paid", views.purchase_paid, name="purchase_paid"),
    path("purchases", views.purchases, name="purchases"),
] 
