from django.contrib import admin
from .models import *

admin.site.register(Users)
admin.site.register(Delivery_Addresses)
admin.site.register(Brands)
admin.site.register(Product)
admin.site.register(Purchase_History)
admin.site.register(Category)