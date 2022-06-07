from django.shortcuts import render
from django.views import View


class Main_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class Brands_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'brands.html')


class Catalog_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'catalog.html')


class Catalog_Item(View):
    # def get(self, request, name, *args, **kwargs):
    def get(self, request, *args, **kwargs):
        return render(request, 'catalog_item.html')


class Brand_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'brand_page.html')


class Partnership_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'partnership.html')


class Press_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'press.html')


class Contacts_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contacts.html')


class Privacy_Policy_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'privacy.html')


class Register_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')


class Login_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')