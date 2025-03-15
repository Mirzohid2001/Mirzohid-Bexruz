from django.contrib import admin
from .models import Product, Wagon, Movement, Inventory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'volume', 'weight', 'price_usd', 'price_sum', 'in_qty', 'out_qty', 'created_at')
    search_fields = ('code', 'name', 'category')
    list_filter = ('category', 'created_at')


@admin.register(Wagon)
class WagonAdmin(admin.ModelAdmin):
    list_display = ('wagon_number', 'wagon_type', 'net_weight', 'meter_weight', 'capacity', 'volume', 'price_sum', 'condition')
    search_fields = ('wagon_number', 'wagon_type')
    list_filter = ('wagon_type', 'condition')


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'document_number', 'product', 'wagon', 'movement_type', 'quantity', 'price_sum', 'note', 'created_at')
    list_filter = ('movement_type', 'date', 'product')
    search_fields = ('document_number', 'product__name', 'wagon__wagon_number')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)
