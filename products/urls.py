from django.urls import path
from .views import ProductDetails
urlpatterns = [
  path('/details/<products_id>', ProductDetails.as_view())
]