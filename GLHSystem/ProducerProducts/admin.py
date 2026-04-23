from django.contrib import admin
from .models import Allergen, Product

# Register your models here.

admin.site.register(Allergen)
admin.site.register(Product)