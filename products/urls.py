from django.urls import path

from .views import ProductDetails, ProductCategories, ProductListInfo
urlpatterns = [
  path('/<int:products_id>', ProductDetails.as_view()),
  path('/categories', ProductCategories.as_view()),
  path('/<str:details>/<int:number>', ProductListInfo.as_view())
]

