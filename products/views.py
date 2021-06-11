from django.http  import JsonResponse
from django.views import View

from .models import Product, ProductSize, Image, ProductContent

class ProductDetails(View):
    def get(self, request, products_id):
        product          = Product.objects.get(id=products_id)
        image            = Image.objects.get(product_id=product.id)
        product_contents = ProductContent.objects.filter(product_id=product.id)
        product_sizes    = ProductSize.objects.filter(product_id=product.id)
        
        result={
            'products' :
                {
                    'id'                : product.id,
                    'category'          : product.category.name,
                    'name'              : product.name,
                    'description'       : product.description,
                    'price'             : [{product_size.size.id: product_size.price for product_size in product_sizes}],
                    'size'              : [{product_size.size.id: product_size.stock for product_size in product_sizes}],
                    'image'             : image.url,
                    'country'           : product.country.name,
                    'color'             : product.color,                 
                    'product_substance' : [{product_content.content.name: product_content.percent for product_content in product_contents}]
                }
        }
        return JsonResponse({'result' : result}, status=200)