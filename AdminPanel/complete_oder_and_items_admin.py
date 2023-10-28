from django.contrib import admin
from django.forms import inlineformset_factory
from products.models import *
from django.shortcuts import redirect

class CompleteOderItemTabularInline(admin.TabularInline):
    model = CompletedOderItems
    extra = 0

class CompleteOderModelAdmin(admin.ModelAdmin):
    list_display = ['oder_number','sub_total_price','paid','status','user']
    list_filter = ['status','complete_date']
    inlines = (CompleteOderItemTabularInline,)