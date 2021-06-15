import sys

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum, Q

from .models import Product, ProductSize, Image, ProductContent, Category, Country

class ProductCategories(View):
  def get(self, request):
    result = {
      'categories' : [
        {
          'id'       : object.id,
          'name'     : object.name,
          'imageUrl' : object.image_url
        } for object in Category.objects.all()
      ],
      'countries' : [
        {
          'id'       : object.id,
          'name'     : object.name,
          'imageUrl' : object.image_url
        } for object in Country.objects.all()
      ]
    }
    return JsonResponse({'productCategories' : result}, status=200)

class ProductDetails(View):
    def get(self, request, products_id):
        product          = Product.objects.get(id=products_id)
        images           = Image.objects.filter(product_id=product.id)
        product_contents = ProductContent.objects.filter(product_id=product.id)
        product_sizes    = ProductSize.objects.filter(product_id=product.id)
        
        result={
                    'id'                : product.id,
                    'categoryId'        : product.category.id,
                    'category'          : product.category.name,
                    'name'              : product.name,
                    'description'       : product.description,
                    'country'           : product.country.name,
                    'countryId'         : product.country.id,
                    'color'             : product.color,    
                    'priceAndSize'      : [{'sizeId': product_size.size.id, 'sizeName' : product_size.size.name, 'price' : product_size.price, 'stock' : product_size.stock} for product_size in product_sizes],
                    'image'             : [image.url for image in images],  
                    'productSubstance'  : [{'name' : product_content.content.name, 'value': product_content.percent} for product_content in product_contents]
        }
        return JsonResponse({'productDetails' : result}, status=200)

class ProductListInfo(View):
    def get(self, request, details, number):       
        catch        = request.GET.get('catch', None)
        color        = request.GET.get('color', None)
        price_max    = request.GET.get('priceMax', sys.maxsize)
        price_min    = request.GET.get('priceMin', 0)

        q = Q()

        if details == 'country' and number != 0:
            q.add(Q(country_id=number), q.AND)
            
        if details == 'category' and number != 0:
            pattern_identifier = Category.objects.get(id=number).name
            q.add(Q(category_id=number), q.AND)
            q.add(Q(category_id=6, name__istartswith=pattern_identifier), q.OR) 

        if catch:
            q.add(Q(catch_code=catch), q.AND)

        if color:
            q.add(Q(color=color), q.AND)

        q.add(Q(productsize__price__range=(price_min, price_max)), q.AND)
        q.add(Q(productsize__size_id=3), q.AND)
        
        result = [
            {
                'id'         : product.id,
                'name'       : product.name,
                'catchCode'  : product.catch_code,
                'countryId'  : product.country.id,
                'categoryId' : product.category.id,
                'price'      : product.productsize_set.filter(size_id=3).first().price, #size_id=3 이 가장 저렴한 small size 입니다
                'thumbNail'  : product.image_set.filter(product_id=product.id).first().url,
                'stock'      : product.productsize_set.filter(product_id=product.id).aggregate(Sum('stock'))['stock__sum']
    
            } for product in Product.objects.filter(q)
        ]
        return JsonResponse({'productListInfo' : result}, status=200)

            
