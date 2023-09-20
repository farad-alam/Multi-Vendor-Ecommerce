from django.db import models
from django.utils.text import slugify

# Create your models here.

class Industry(models.Model):
    name = models.CharField( max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField( auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Industry, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    
class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name