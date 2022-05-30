
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from project.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main_Page.as_view(), name='main_page'),
    path('brands/', Brands_Page.as_view(), name='brands'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
