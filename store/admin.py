from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


# Register your models here.
@admin.register(models.Product)
class productAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

@admin.register(models.Customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(models.Order)
class orderAdmin(admin.ModelAdmin):
    list_display = ['customer_name','payment_status']
    list_per_page = 10
    list_select_related = ['customer']

    @admin.display(ordering='customer')
    def customer_name(self, order):
        return order.customer.first_name + ' ' + order.customer.last_name

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': collection.id})
        return format_html(f'<a href="{url}">{collection.products_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )