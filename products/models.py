from django.db import models
from django.db.models.fields import DecimalField


class Product(models.Model):
    name           = models.CharField(max_length=300)
    description    = models.CharField(max_length=500)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    units          = models.CharField(max_length=20)
    weights        = models.DecimalField(max_digits=10, decimal_places=1)
    shipping_type  = models.CharField(max_length=30, default="샛별배송")
    origin         = models.CharField(max_length=200)
    thumbnail_url  = models.URLField()
    category       = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory    = models.ForeignKey("Subcategory", on_delete=models.CASCADE)
    packaging      = models.ManyToManyField("Packaging")

    class Meta:
        db_table = "products"

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "categories"

class Subcategory(models.Model):
    name     = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = "subcategories"

class Image(models.Model):
    url     = models.URLField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"

class Packaging(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "packagings"
