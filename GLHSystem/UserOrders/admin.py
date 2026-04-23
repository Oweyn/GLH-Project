from django.contrib import admin
from UserOrders.models import Order, OrderItem

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)