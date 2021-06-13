from django.urls import path

from .views import OrdersPayment, OrdersCart

urlpatterns = [
    path('/payment', OrdersPayment.as_view()),
    path('/cart', OrdersCart.as_view())
]