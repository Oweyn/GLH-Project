from django.db import models
from UserAccounts.models import User
from ProducerProducts.models import Product

# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    delivery_order = models.BooleanField(default=False)
    total_order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_delivery_address = models.CharField(max_length=600, default="")
    loyalty_points_earned = models.PositiveIntegerField(default = 0)

    #This is a loop to calulate the total cost of all items in the cart
    #TODO: Check this was actually used
    def cart_total(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

    ##TODO: add admin view

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    individal_item_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=8)

    ##TODO: to add admin view