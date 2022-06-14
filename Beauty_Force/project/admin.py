from django.contrib import admin
from .models import *

admin.site.register(Users)
admin.site.register(Delivery_Addresses)
admin.site.register(Brands)
admin.site.register(Product)
admin.site.register(Purchase_History)
admin.site.register(Category)


class Order_Item_Inline(admin.TabularInline):
    model = Order_Items
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient',
                    'address', 'paid',
                    'created_at', 'order_date']
    list_filter = ['paid', 'created_at', 'order_date']
    inlines = [Order_Item_Inline]


admin.site.register(Orders, OrderAdmin)
