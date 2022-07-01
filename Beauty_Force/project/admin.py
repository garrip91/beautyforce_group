from django.contrib import admin
from .models import *
from .forms import *

from import_export.admin import ImportExportModelAdmin
from django import forms
from import_export import fields, resources
from import_export.widgets import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail

admin.site.register(Delivery_Addresses)
admin.site.register(Brands)
admin.site.register(Press)


@admin.register(Users)
class Users_Admin(admin.ModelAdmin):
    list_display = ['username', ]
    actions = ['send_mail_admin', ]

    def send_mail_admin(modeladmin, request, queryset):
        users_email = []
        for users in queryset.all():
            users_email.append(users.email)
        if 'apply' in request.POST:
            print(request.POST)
            return HttpResponseRedirect(request.get_full_path())
        # if 'send' in request.POST:
        #    print('sdfs')
        #    if form.is_valid():
        #        subject = form.cleaned_data['subject']
        #        message = form.cleaned_data['message']
        #        print('fsdfs')
        #        print(subject)
        #        print(message)
        #        return HttpResponseRedirect(request.get_full_path())
        else:
            form = Send_Mail_Admin_Form()
        return render(request, 'admin/admin_send_mail.html', {'form': form, 'orders': queryset})

    send_mail_admin.short_description = 'Сделать рассылку'


@admin.register(Bestsellers_Line)
class Bestsellers_Line_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['line', ]
    list_filter = ['line', ]
    search_fields = ['line', ]


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
    list_filter = ['brand', 'title', ]
    search_fields = ['brand__brand_name', ]


admin.site.register(Product, PropsAdminImage)
