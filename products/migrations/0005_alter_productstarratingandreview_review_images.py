# Generated by Django 4.2.5 on 2023-11-17 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productstarratingandreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstarratingandreview',
            name='review_images',
            field=models.ImageField(blank=True, upload_to='product-review-images/'),
        ),
    ]
