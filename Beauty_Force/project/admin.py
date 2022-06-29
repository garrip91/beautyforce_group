from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin, ImportMixin
from django import forms
from import_export import fields, resources
from import_export.widgets import *

admin.site.register(Users)
admin.site.register(Delivery_Addresses)
admin.site.register(Brands)
admin.site.register(Press)


# admin.site.register(Bestsellers_Line)
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Bestsellers_Line)
class Bestsellers_Line_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('line',)


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


class Images_For_Product(admin.TabularInline):
    model = Product_Images


class Import_Product(resources.ModelResource):
    brand = fields.Field(column_name='brand', attribute='brand', widget=ForeignKeyWidget(Brands, 'brand_name'))
    product_line = fields.Field(column_name='product_line', attribute='product_line',
                                widget=ForeignKeyWidget(Bestsellers_Line, 'line'))

    class Meta:
        model = Product


class PropsAdminImage(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [Images_For_Product, ]
    resource_class = Import_Product


admin.site.register(Product, PropsAdminImage)

admin.site.site_header = "Панель администратора Beauty Force"
admin.site.site_title = "Панель администратора Beauty Force"
admin.site.index_title = "Добро пожаловать"
