from django.db import models
from UserAccounts.models import User
from ProducerProducts.models import Product

# Create your models here.

#Each customer should only have one cart
class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)

##TODO add admin view
    def __str__(self):
        return f"{self.customer.last_name}, {self.customer.first_name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

##TODO consider changing to a property as better coding practices
#TODO: Check this function isnt redundant
    def subtotal(self):
        return self.product.price * self.quantity

##TODO add admin view
    def __str__(self):
        return f"{self.product}"

def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(customer=user)
    return cart