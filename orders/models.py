from django.db import models

from users.models    import User
from products.models import Product, Size

class OrderStatus(models.Model):
    status = models.CharField(max_length = 45)

    class Meta:
        db_table = 'order_status'

class Order(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True)
    status       = models.ForeignKey(OrderStatus, null=True, on_delete=models.SET_NULL)
    user         = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    total_price = models.DecimalField(max_digits=18, decimal_places=2)
    size        = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    product     = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'order_items'