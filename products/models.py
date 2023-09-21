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
    
class Product(models.Model):
    title = models.CharField( max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    regular_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    modle = models.CharField(max_length=50)
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    tag = models.CharField(max_length=50, help_text='enter your tag coma separated')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    
    