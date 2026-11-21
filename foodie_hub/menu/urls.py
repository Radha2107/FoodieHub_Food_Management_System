from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:food_id>/", views.update_cart, name="update_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.my_orders, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
