import json

from django.http      import JsonResponse
from django.views     import View
from django.utils     import timezone
from django.db.models import Sum

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
        id = request.user.id

        order = Order.objects.filter(user_id=id, status_id=1) or False

        if not order:
            return JsonResponse({'result' : {
                'orderId'  : -1,
                'products' : []
            }}, status=200)

        order_items = order[0].orderitem_set.all()

        result = {
            'orderId' : order[0].id,
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
                    'stock'       : object.product.productsize_set.all().aggregate(Sum('stock'))['stock__sum'],
                    'orderItemId' : object.id
                } for object in order_items
            ]
        }

        return JsonResponse({'result' : result}, status=200)

    @LoginStatus
    def post(self, request):
        try:
            datas = json.loads(request.body)

            id = request.user.id

            obj, created = Order.objects.get_or_create(
                user_id=id,
                status_id=1
            )
        
            if not created:
                Order.objects.filter(id = obj.id).update(updated_at = timezone.now())
            
            order_item = OrderItem.objects.filter(
                order_id=obj.id,
                size_id=datas['sizeId'],
                product_id=datas['productId']
            ) or False
        
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
                total_price = ProductSize.objects.get(
                    product_id = datas['productId'], 
                    size_id    = datas['sizeId']
                ).price * datas['quantity']

                OrderItem.objects.filter(id=order_item[0].id).update(
                    quantity    = order_item[0].quantity + datas['quantity'],
                    total_price = order_item[0].total_price + total_price
                )
            return JsonResponse({'result' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'result' : 'INVALID KEY'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result' : 'EMPTY BODY'}, status=400)

    @LoginStatus
    def delete(self, request):
        try:
            datas = json.loads(request.body)

            order_item = OrderItem.objects.filter(id = datas['orderItemId'])
            order_id   = -1 if not len(order_item) else order_item[0].order_id
            is_deleted = False if not order_item.delete()[0] else True

            if is_deleted:
                order_item_count = OrderItem.objects.filter(order_id = order_id).count()

                if not order_item_count:
                    Order.objects.filter(id = order_id).delete()

            return JsonResponse({'result' : 'SUCCESS'}, status=204)
        except KeyError:
            return JsonResponse({'result' : 'INVALID KEY'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'result' : 'EMPTY BODY'}, status=400)