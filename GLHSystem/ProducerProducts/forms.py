from django import forms
from .models import Product


#Allows producers to add products
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description","ingredients", "price", "stock", "image", "product_allergens"]
        widgets = {
            'product_allergens': forms.CheckboxSelectMultiple(),
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description","ingredients", "price", "stock", "image", "product_allergens"]
        widgets = {
            'product_allergens': forms.CheckboxSelectMultiple(),
        }