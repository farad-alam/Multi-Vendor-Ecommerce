from django.contrib import admin
from django.forms import inlineformset_factory
from products.models import *
from django.shortcuts import redirect

# Register your models here.



class PlacedOderItemTabularAdmin(admin.TabularInline):
    model = PlacedeOderItem
    extra = 0

class OderManagementAdmin(admin.ModelAdmin):
    list_display = ['order_number','sub_total_price','paid','user']
    list_editable = ['paid']
    list_filter = ['status','placed_date']
    inlines = (PlacedOderItemTabularAdmin,)

    
    def save_model(self, request, obj, form, change):

        # deleted placed oder & placedOderItem and
        # make nwe CompletedOder & completedOderItem on oder status Chnaged
        if change and obj.status == 'Oder Shipped' :
            completed_oder = CompletedOder(
            user = obj.user,
            shipping_address = obj.shipping_address,
            sub_total_price =obj.sub_total_price,
            paid = obj.paid,
            status = 'Oder Shipped',
            oder_number = obj.order_number
            )
            completed_oder.save()
            placed_oder_items = PlacedeOderItem.objects.filter(placed_oder=obj)
            for placed_oder_item in placed_oder_items:
                completed_oder_items = CompletedOderItems(
                    completed_oder  = completed_oder,
                    product = placed_oder_item.product,
                    quantity = placed_oder_item.quantity,
                    total_price = placed_oder_item.total_price
                )
                completed_oder_items.save()
                placed_oder_item.delete()
            obj.delete()
            return redirect('/custom-admin/products/placedoder/')
            

        obj.save()
        super().save_model(request, obj, form, change)

        if change == False:
            # Create and associate 'PlacedOderItem' instances without saving them immediately
            PlacedeOderItemFormSet = inlineformset_factory(PlacedOder, PlacedeOderItem, fields=('product', 'quantity'))
            formset = PlacedeOderItemFormSet(request.POST, instance=obj)
            
            if formset.is_valid():
                formset.save()

            # Calculate Subtotal price on PlaceOder, after saving the placedOderItem     
            if obj.order_items.exists():
                sub_total_price = 0
                for item in obj.order_items.all():
                    sub_total_price += item.total_price
                obj.sub_total_price = sub_total_price
                obj.save()

        else:
            # Updating 'PlacedOderItem' instances without saving them immediately
            PlacedeOderItemFormSet = inlineformset_factory(PlacedOder, PlacedeOderItem, fields=('product', 'quantity'))
            formset = PlacedeOderItemFormSet(request.POST, instance=obj)
            
            if formset.is_valid():
                formset.save()

            # Calculate Subtotal price on PlaceOder, after Modifing the placedOderItem     
            if obj.order_items.exists():
                sub_total_price = 0
                for item in obj.order_items.all():
                    sub_total_price += item.total_price
                obj.sub_total_price = sub_total_price
                obj.save()

