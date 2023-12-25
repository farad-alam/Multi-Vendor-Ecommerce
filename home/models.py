from django.db import models
from django.utils.text import slugify
# Create your models here.

#Front Big Slider
class SliderArea(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    title = models.CharField(max_length=200)
    discount = models.PositiveIntegerField()
    product_url = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.title

class DisplayHotProductInCategories(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    title = models.CharField(max_length=200)
    categories = models.ForeignKey("products.Categories",  on_delete=models.DO_NOTHING)
    product_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class PopularCategories(models.Model):
    image = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None)
    categories = models.ForeignKey("products.Categories",  on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categories.name

    
    




