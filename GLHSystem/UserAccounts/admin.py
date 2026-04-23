from django.contrib import admin
from UserAccounts.models import User, ProducerAccount, CustomerAccount

# Register your models here.

admin.site.register(User)
admin.site.register(ProducerAccount)
admin.site.register(CustomerAccount)
