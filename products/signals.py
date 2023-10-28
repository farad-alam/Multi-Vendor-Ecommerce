from .models import PlacedOder, CompletedOder, CompletedOderItems, PlacedeOderItem
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import redirect


# @receiver(pre_save, sender=PlacedOder)
# def create_completedOder(sender,instance,**kwargs):
#     if instance.status == 'Oder Shipped':
#         completed_oder = CompletedOder(
#             user = instance.user,
#             shipping_address = instance.shipping_address,
#             sub_total_price =instance.sub_total_price,
#             status = 'Oder Shipped',
#             oder_number = instance.order_number
#         )
#         completed_oder.save()
#         placed_oder_items = PlacedeOderItem.objects.filter(placed_oder=instance)
#         for placed_oder_item in placed_oder_items:
#             completed_oder_items = CompletedOderItems(
#                 completed_oder  = completed_oder,
#                 product = placed_oder_item.product,
#                 quantity = placed_oder_item.quantity,
#                 total_price = placed_oder_item.total_price
#             )
#             completed_oder_items.save()
#             placed_oder_item.delete()
        
#         print(sender)
#         print(instance)
#         # Set a session variable to indicate a redirect
#         instance.redirect_adter_completion = True
#         print(True)

# @receiver(post_save, sender=PlacedOder)
# def calculate_subtotal(sender,instance,**kwargs):
#     if instance.order_items.exists():
#         sub_total_price = 0
#         for item in instance.order_items.all():
#             sub_total_price += item.total_price
#         instance.sub_total_price = sub_total_price
        
        