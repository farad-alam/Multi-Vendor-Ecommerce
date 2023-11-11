from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser
# Create your models here.

class VendorStore(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=("vendor_user"), on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=115,unique=True, blank=True)
    logo = models.ImageField( upload_to='media/vendoreStore/logo/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    cover_photo = models.ImageField( upload_to='media/vendoreStore/coverPhoto/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(VendorStore,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

