from django.contrib import admin
from .models import GuestInfo, Order, OrderItem, ShippingZone, ShippingRate 
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(GuestInfo)
admin.site.register(ShippingZone)
admin.site.register(ShippingRate)
