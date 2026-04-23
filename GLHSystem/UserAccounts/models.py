from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User class is inheriting from AbstractUser class
class User(AbstractUser):

    #(database value, admin value)
    USERTYPE = (
        ("customer", "Customer"),
        ("producer", "Producer"),
    )

    user_type = models.CharField(max_length=15, choices = USERTYPE, default="customer")
    user_loyalty_points = models.IntegerField(default = 0)

    #Fucntions to check user permissions and too return admin view
    #TODO: Consider turning into propertys
    @property
    def is_customer(self):
        return self.user_type == "customer"
    @property
    def is_producer(self):
        return self.user_type == "producer"
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class ProducerAccount(models.Model):
    #If the user is deleted all related objects should be deleted, this allows for easier complience with GDPR in regards to users having the right to have their accounts deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='Images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}, {self.store_name}"

class CustomerAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.last_name},{self.user.first_name}"