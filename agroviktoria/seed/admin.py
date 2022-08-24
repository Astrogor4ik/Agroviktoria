from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_prod', 'price', 'time_create', 'time_update', 'top_sale', 'is_published', 'digital')
    list_display_links = ('id', 'name_prod', 'top_sale')
    search_fields = ('name_prod', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'top_sale')
    prepopulated_fields = {"slug": ('name_prod',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_cat')
    list_display_links = ('id', 'name_cat')
    search_fields = ('name_cat',)
    prepopulated_fields = {"slug_cat": ('name_cat',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_orderd')
    list_display_links = ('id',)
    search_fields = ('customer',)
    #list_editable = ('complete',)
    list_filter = ('complete', 'date_orderd')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'last_name', 'phone', 'email')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'name')
    #list_editable = ('complete',)
    #list_filter = ('time_create', 'email')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'region', 'city', 'mail', 'date_added')
    list_display_links = ('customer', 'order')
    search_fields = ('region', 'city')
    #list_editable = ('is_published',)
    list_filter = ('date_added', )

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'date_added')
    list_display_links = ('order',)
    search_fields = ('order',)
    #list_editable = ('complete',)
    list_filter = ('date_added', )




admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
