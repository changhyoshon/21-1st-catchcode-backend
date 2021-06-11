from django.urls import path
from .views import ProductDetails, ProductCategories
urlpatterns = [
  path('/<int:products_id>', ProductDetails.as_view()),
  path('/categories', ProductCategories.as_view())
]