from django.db import models

class Category(models.Model):
    name      = models.CharField(max_length=20)
    image_url = models.CharField(max_length=200)

    class Meta:
        db_table = 'categories'

class Country(models.Model):
    name      = models.CharField(max_length=20)
    image_url = models.CharField(max_length=200)

    class Meta:
        db_table = 'countries'

class Size(models.Model):
    size = models.CharField(max_length=10)

    class Meta:
        db_table = 'sizes'

class Content(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'contents'

class Product(models.Model):
    name            = models.CharField(max_length=45)
    description     = models.TextField()
    category        = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    country         = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    color           = models.CharField(max_length=45)
    catch_code      = models.IntegerField()
    created_at      = models.DateTimeField(auto_now_add=True)
    product_size    = models.ManyToManyField(Size, through='ProductSize')
    product_content = models.ManyToManyField(Content, through='ProductContent')

    class Meta:
        db_table = 'products'

class ProductSize(models.Model):
    size    = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    stock   = models.IntegerField()
    price   = models.DecimalField(max_digits=18, decimal_places=2)
    
    class Meta:
        db_table = 'product_sizes'

class ProductContent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, null=True, on_delete=models.SET_NULL)
    percent = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = 'product_contents'

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url     = models.CharField(max_length=500)

    class Meta:
        db_table = 'images'