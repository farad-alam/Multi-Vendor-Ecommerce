# Generated by Django 4.2.5 on 2023-09-22 04:11

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_description_productdetailsdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='details_description',
            field=ckeditor.fields.RichTextField(default=1, max_length=5000),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProductDetailsDescription',
        ),
    ]
