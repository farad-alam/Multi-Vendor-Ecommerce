from django.shortcuts import render
from . models import SliderArea
from products.models import Industry
# Create your views here.

def home(request):
    slider = SliderArea.objects.all()
    industry = Industry.objects.all()
    context = {
        'slider':slider,
        'industry':industry
    }
    return render(request,'home/home.html', context)