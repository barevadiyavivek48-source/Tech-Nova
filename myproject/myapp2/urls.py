
from django.urls import path
from . import views
app_name = 'vendor'


urlpatterns = [
    path('vendor_account/', views.vendor_account, name='vendor_account'),
    path('vendor_grid/', views.vendor_grid, name='vendor_grid'),
    path('vendor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor_add_category/', views.vendor_add_category,
         name='vendor_add_category'),
    path('vendor_add_product/', views.vendor_add_product,
         name='vendor_add_product'),
]
