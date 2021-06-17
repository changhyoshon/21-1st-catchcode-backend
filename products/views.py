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
    def get(self, request):       
        catch       = request.GET.get('catch', None)
        color       = request.GET.get('color', None)
        price_max   = request.GET.get('priceMax', sys.maxsize)
        price_min   = request.GET.get('priceMin', 0)
        country_id  = request.GET.get('country', None)
        category_id = request.GET.get('category', None)

        q = Q()

        if country_id:
            q.add(Q(country_id=country_id), q.AND)

        if category_id:
            pattern_identifier = Category.objects.get(id=category_id).name
            q.add(Q(category_id=category_id), q.AND)
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

class ProductList(View):
    def get(self,request):
        # main 페이지 10개 게시물 뽑아오기
        result = [
          {
            'id'        : object.id,
            'name'      : object.name,
            'price'     : object.productsize_set.filter(size_id=3).first().price,
            'thumbNail' : object.image_set.all().order_by('id').first().url,
            'catchCode' : object.catch_code,
            'stock'     : object.productsize_set.aggregate(Sum('stock'))['stock__sum']
          } for object in Product.objects.all().order_by('-created_at')[:10]
        ]
        return JsonResponse({"productList":result},status = 200)


            
