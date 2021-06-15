import json

from django.http      import JsonResponse
from django.views     import View
from django.utils     import timezone

from users.utils     import LoginStatus
from orders.models   import Order, OrderItem
from products.models import ProductSize

class OrdersPayment(View):
    @LoginStatus
    def post(self, request):
        try:
            id = request.user.id

            datas = json.loads(request.body)

            is_paid = Order.objects.filter(
                id      = datas['orderId'],
                user_id = id,
                status  = 1
            ).update(status_id = 2)
            
            if not is_paid:
                return JsonResponse({'result' : 'INVALID PAYMENT'}, status=400)

            return JsonResponse({'result' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'result' : 'INVALID KEY'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result' : 'EMPTY BODY'}, status=400)

class OrdersCart(View):
    @LoginStatus
    def get(self, request):
        try:
            id = request.user.id

            order = Order.objects.get(user_id = id, status_id = 1)
            
            order_items = order.orderitem_set.all().select_related('product', 'size').prefetch_related('product__product_size', 'product__image_set')

            result = {
                'orderId' : order.id,
                'products':[
                    {
                        'productId'   : object.product_id,
                        'productName' : object.product.name,
                        'catchCode'   : object.product.catch_code,
                        'thumbNail'   : object.product.image_set.all().order_by('id').first().url,
                        'quantity'    : object.quantity,
                        'totalPrice'  : object.total_price,
                        'sizeId'      : object.size_id,
                        'sizeName'    : object.size.name,
                        'stock'       : object.product.productsize_set.filter(size_id = object.size_id).first().stock,
                        'orderItemId' : object.id
                    } for object in order_items
                ]
            }

            return JsonResponse({'result' : result}, status=200)
        except Order.MultipleObjectsReturned:
            return JsonResponse({'result' : 'INVALID CART'}, status=412)
        except Order.DoesNotExist:
            return JsonResponse({'result' : {'orderId'  : -1, 'products' : []}}, status=200)

    @LoginStatus
    def post(self, request):
        try:
            datas = json.loads(request.body)

            id = request.user.id

            obj, created = Order.objects.get_or_create(
                user_id   = id,
                status_id = 1
            )
        
            if not created:
                obj.updated_at = timezone.now()
                obj.save()
            
            order_item = OrderItem.objects.filter(
                order_id   = obj.id,
                size_id    = datas['sizeId'],
                product_id = datas['productId']
            ).select_related('product').prefetch_related('product__product_size').first()
        
            if not order_item:
                price = ProductSize.objects.get(
                    product_id = datas['productId'],
                    size_id    = datas['sizeId']
                ).price

                OrderItem(
                    order_id    = obj.id,
                    quantity    = datas['quantity'],
                    total_price = datas['quantity'] * price,
                    size_id     = datas['sizeId'],
                    product_id  = datas['productId']
                ).save()
            else:
                total_price = order_item.product.productsize_set.filter(size_id = datas['sizeId']).first().price
                total_price = total_price * datas['quantity']

                order_item.quantity    = order_item.quantity + datas['quantity']
                order_item.total_price = order_item.total_price + total_price
                order_item.save()

            return JsonResponse({'result' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'result' : 'INVALID KEY'}, status=400)
        except ProductSize.DoesNotExist:
            return JsonResponse({'result' : 'INVALID PRODUCT'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result' : 'EMPTY BODY'}, status=400)

    @LoginStatus
    def delete(self, request):
        try:
            datas = json.loads(request.body)

            order_item = OrderItem.objects.get(id = datas['orderItemId'])

            if order_item.delete():
                order_item_count = OrderItem.objects.filter(order_id = order_item.order_id).count()

                if not order_item_count:
                    Order.objects.filter(id = order_item.order_id).delete()

            return JsonResponse({'result' : 'SUCCESS'}, status=204)
        except KeyError:
            return JsonResponse({'result' : 'INVALID KEY'}, status=400)
        except OrderItem.DoesNotExist:
            return JsonResponse({'result' : 'INVALID PRODUCT'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result' : 'EMPTY BODY'}, status=400)