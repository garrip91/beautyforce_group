from django.contrib import admin
from .models import *
from .forms import *

from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail

admin.site.register(Delivery_Addresses)

admin.site.register(Press)


class Brands_Category(admin.TabularInline):
    model = Brands_Category


class Brand_Benefits(admin.TabularInline):
    model = Brand_Benefits


class Compound_And_Ingredients(admin.TabularInline):
    model = Compound_And_Ingredients


class Brand_Images(admin.TabularInline):
    model = Brands_Images


class Reviews(admin.TabularInline):
    model = Reviews


class Brands_Video(admin.TabularInline):
    model = Brands_Video


class Brands_Admin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [Brands_Category, Brand_Benefits, Compound_And_Ingredients, Reviews, Brand_Images, Brands_Video, ]
    list_display = ['brand_name', ]
    list_filter = ['brand_name', ]
    search_fields = ['brand_name', ]


admin.site.register(Brands, Brands_Admin)


@admin.register(Users)
class Users_Admin(admin.ModelAdmin):
    list_display = ['username', ]
    actions = ['send_mail_admin', ]

    def send_mail_admin(self, request, queryset):
        users_email = []
        for users in queryset:
            users_email.append(users.email)
        form = Send_Mail_Admin_Form(request.POST)
        if 'apply' in request.POST:
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                try:
                    send_mail(
                        subject,
                        message,
                        'reg@beforce.ru',
                        users_email,
                        fail_silently=False,
                    )
                    self.message_user(request, 'Сообщения успешно отправлены')
                    return HttpResponseRedirect(request.get_full_path())
                except:
                    self.message_user(request, 'Сообщения не отправлены, попробуйте снова')
                    return HttpResponseRedirect(request.get_full_path())
        return render(request, 'admin/admin_send_mail.html', {'form': form, 'users': queryset})

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
