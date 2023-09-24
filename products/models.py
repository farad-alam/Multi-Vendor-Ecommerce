from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
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
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    regular_price = models.PositiveIntegerField()
    discounted_parcent = models.PositiveIntegerField()
    description = RichTextField(max_length=2000)
    modle = models.CharField(max_length=50)
    categories = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
    tag = models.CharField(max_length=50, help_text='enter your tag coma separated')
    details_description = RichTextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def discounted_price(self):
        price = self.regular_price - (self.regular_price*self.discounted_parcent)/100
        price = f"{price:.2f}"
        return price

    #discounted_price

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
    
    
class ProductImage(models.Model):
    image = models.CharField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

class ProductAditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=70)
    details = models.CharField(max_length=150)

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)


    @property
    def total_product_price(self):
        price = self.product.discounted_price*self.quantity
        price = f"{price:.2f}"
        return price
    

    def __str__(self):
        return self.product.title
    

# quantity
# total_price


    
