from django.urls import path
from .views import ProductList, ProductCategories, ProductDetails
urlpatterns = [
  path('/<int:products_id>', ProductDetails.as_view()),
  path('/categories', ProductCategories.as_view()),
  path('',ProductList.as_view())
]