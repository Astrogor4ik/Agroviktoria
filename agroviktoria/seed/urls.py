from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('store/', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name='update_item'),
    path('store/<slug:prod_slug>', show_post, name='product'),
    path('category/<slug:cat_slug>', show_category, name='category'),
    path('clean_seed/', clean_seed, name='clean_seed'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('delivery/', delivery, name='delivery'),
    path('we_on_map/', we_on_map, name='we_on_map'),
    path('process_order/', processOrder, name='process_order'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logoutUser, name='logout')




]