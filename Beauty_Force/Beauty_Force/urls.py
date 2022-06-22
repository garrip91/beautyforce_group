from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from project.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main_Page.as_view(), name='main_page'),
    path('brands/', Brands_Page.as_view(), name='brands'),
    path('catalog/', Catalog_Page.as_view(), name='catalog'),
    path('catalog/<slug>/<title>/', Catalog_Item.as_view(), name='catalog_item'),
    path('brand/', Brand_Page.as_view(), name='brand'),
    path('partnership/', Partnership_Page.as_view(), name='partnership'),
    path('press/', Press_Page.as_view(), name='press'),
    path('contacts/', Contacts_Page.as_view(), name='contacts'),
    path('privacy/', Privacy_Policy_Page.as_view(), name='privacy'),
    path('register/', Register_Page.as_view(), name='register'),
    path('login/', Login_Page.as_view(), name='login'),
    path('b2b_catalog/', B2B_Catalog_Page.as_view(), name='b2b_catalog'),
    path('basket/', Basket_Page.as_view(), name='basket'),
    path('personal_account/', Users_Lk_Page.as_view(), name='personal_account'),
    path('personal_account/orders_history/', Users_Orders_History.as_view(), name='orders_history'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate,
         name='activate'),
    path('password_reset/', Password_Reset.as_view(), name='password_reset'),
    path('add_to_cart/<product_id>/', Add_To_Cart.as_view(), name='add_to_cart'),
    path('remove_from_cart/<product_id>/', Delete_From_Cart.as_view(), name='remove_from_cart'),
    path("contact_us/", Contact_Us.as_view(), name='contact_us')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
