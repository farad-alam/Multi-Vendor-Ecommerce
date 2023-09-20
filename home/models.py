from django.db import models
from django.utils.text import slugify
import uuid
# Create your models here.

class SliderArea(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    title = models.CharField(max_length=200)
    discount = models.PositiveIntegerField()
    product_url = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.title





