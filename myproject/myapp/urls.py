from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='index'),
    path('search/', views.search_products, name='search'),
    path('api/search/', views.search_dropdown_api, name='search_api'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('blog/', views.blog, name='blog'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('buy_now/<int:id>/', views.buy_now, name='buy_now'),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('remove_all_cart/', views.remove_all_cart, name='remove_all_cart'),
    path('plus/<int:id>/', views.plus, name='plus'),
    path('minus/<int:id>/', views.minus, name='minus'),

    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('invoice/<int:order_id>/', views.invoice_pdf, name='invoice_pdf'),

    path('contact/', views.contact, name='contact'),
    path('my_account/', views.my_account, name='my_account'),
    path('order_successfull/', views.order_successfull, name='order_successfull'),
    path('product_details/<int:product_id>/',
         views.product_details, name='product_details'),
    path('billing/', views.billing, name='billing'),


    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:id>/',
         views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:id>/',
         views.remove_wishlist, name='remove_wishlist'),
    path('subscribe_newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
