from django.db import models

from products.models import Product


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    membership = models.CharField(max_length=10, default="퍼플")

    class Meta:
        db_table = "users"

class Cart(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = "carts"