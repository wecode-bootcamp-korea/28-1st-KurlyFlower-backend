import csv
import os
import sys

import django


os.chdir('.')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'kurlyflower.settings')
django.setup()

from products.models import Category, Image, Packaging, Product, Subcategory

def category_insert():
    category_list = [
        Category(id=1, name="채소"),
        Category(id=2, name="과일"),
        Category(id=3, name="정육"),
        Category(id=4, name="수산")
    ]

    if not Category.objects.exists():
        Category.objects.bulk_create(category_list)

    subcategory_list = [
        Subcategory(id=1, name="특수야채", category_id=1),
        Subcategory(id=2, name="일반야채", category_id=1),
        Subcategory(id=3, name="국산", category_id=2),
        Subcategory(id=4, name="수입", category_id=2),
        Subcategory(id=5, name="소고기", category_id=3),
        Subcategory(id=6, name="돼지고기", category_id=3),
        Subcategory(id=7, name="생선", category_id=4),
        Subcategory(id=8, name="조개", category_id=4)
    ]
    if not Subcategory.objects.exists():
        Subcategory.objects.bulk_create(subcategory_list)

    packaging_type_list = [
        Packaging(id=1, name="상온"),
        Packaging(id=2, name="냉장"),
        Packaging(id=3, name="냉동")
    ]

    if not Packaging.objects.exists():
        Packaging.objects.bulk_create(packaging_type_list)

def product_insert():
    with open('resource/products.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        product_list = []
        for row in reader:
            product_list.append(
                Product(
                    name           = row['name'],
                    description    = row['description'],
                    price          = row['price'],
                    units          = row['units'],
                    weights        = row['weights'],
                    shipping_type  = row['shipping_type'],
                    origin         = row['origin'],
                    thumbnail_url  = row['thumbnail_url'],
                    category_id    = row['category_id'],
                    subcategory_id = row['subcategory_id'],
                )
            )
        if not Product.objects.exists():
            Product.objects.bulk_create(product_list)
            print("PRODUCTS UPLOADED SUCCESSFULY!")

def packaging_insert():
    with open('resource/products.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            name           = row['name']
            packaging_type = row['packaging']

            product = Product.objects.filter(name=name).first()
            package = Packaging.objects.filter(name=packaging_type).first()
            product.packaging.add(package)

        if Packaging.objects.exists():
            print("PACKAGING TYPE UPLOADED SUCCESSFULY!")

def image_insert():
    with open('resource/detail_image.csv', 'r', encoding='utf-8-sig') as f:
        image_reader = csv.DictReader(f)

        detail_image_list = []
        for row in image_reader:
            print(row)
            product_id = Product.objects.filter(name=row['name']).first().id
            detail_image_list.append(
                Image(
                    product_id = product_id,
                    url = row['image'],
                )
            )

        if not Image.objects.exists():
            Image.objects.bulk_create(detail_image_list)
            print("DETAIL IMAGE UPLOADED SUCCESSFULY!")

category_insert()
product_insert()
packaging_insert()
image_insert()
