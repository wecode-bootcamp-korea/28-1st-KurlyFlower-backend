# Generated by Django 4.0 on 2021-12-29 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_rename_packaging_type_packaging_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="weights",
            field=models.CharField(max_length=20),
        ),
    ]
