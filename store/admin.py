from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'LOW')
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class productAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status(self, product: models.Product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

@admin.register(models.Customer)
class customerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

class orderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0

@admin.register(models.Order)
class orderAdmin(admin.ModelAdmin):
    inlines = [orderItemInline]
    autocomplete_fields = ['customer']  
    list_display = ['customer_name','payment_status']
    list_per_page = 10
    list_select_related = ['customer']

    @admin.display(ordering='customer')
    def customer_name(self, order: models.Order):
        return order.customer.user.first_name + ' ' + order.customer.user.last_name

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection: models.Collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': collection.id})
        return format_html(f'<a href="{url}">{collection.products_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )