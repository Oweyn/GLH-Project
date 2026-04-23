from django.db import models
from UserAccounts.models import ProducerAccount

# Create your models here.

#Allergens can be added throught the admin portal as there is a set ammount but the law may change and more allergens may need to be added
class Allergen(models.Model):
    allergen_name = models.CharField(max_length = 100, unique=True, blank=False)

#Items will show as their assigned name instaed of their assigned objectID
    def __str__(self):
        return f"{self.allergen_name}"


# Creates all the needed fields for each product
class Product(models.Model):
    producer = models.ForeignKey(ProducerAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    ingredients = models.TextField()
    
    #Uploads all product images to static/Images folder
    image = models.ImageField(upload_to='Images/')
    product_allergens = models.ManyToManyField(Allergen)

    def __str__(self):
        return f"{self.name},{self.producer.store_name}"

