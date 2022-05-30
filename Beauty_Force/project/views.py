from django.shortcuts import render
from django.views import View


class Main_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class Brands_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'brands.html')
