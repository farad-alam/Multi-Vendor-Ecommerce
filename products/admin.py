from django.contrib import admin
from . models import Industry, Categories, SubCategories
# Register your models here.
admin.site.register(Industry)
admin.site.register(Categories)
admin.site.register(SubCategories)
