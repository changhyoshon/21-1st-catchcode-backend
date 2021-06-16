from django.urls import path

from .views import ProductDetails, ProductCategories, ProductListInfo, ProductList

urlpatterns = [
  path('/<int:products_id>', ProductDetails.as_view()),
  path('/categories', ProductCategories.as_view()),
  path('/search', ProductListInfo.as_view()),
  path('', ProductList.as_view())
]

