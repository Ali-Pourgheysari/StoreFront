from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import productAdmin
from store.models import Product
from tags.models import TaggedItem

# Register your models here.

class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0

class CustomProductAdmin(productAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)