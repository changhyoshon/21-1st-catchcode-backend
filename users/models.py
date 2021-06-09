from django.db import models

class User(models.Model):
    phone_number = models.CharField(max_length=20)
    name         = models.CharField(max_length=45)
    password     = models.CharField(max_length=200)
    sex          = models.IntegerField()
    admin        = models.IntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    is_delete    = models.BooleanField(null=True)

    class Meta:
        db_table = 'users'