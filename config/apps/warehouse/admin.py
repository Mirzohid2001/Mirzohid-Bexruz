from django.contrib import admin
from .models import (
    Warehouse, Product, Batch, Wagon, Movement, Inventory, Reservoir, ReservoirMovement, AuditLog, LocalClient, LocalMovement,Placement,WagonType
)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'zone', 'location_code')
    search_fields = ('name', 'location', 'zone')
    list_filter = ('zone', 'location')

@admin.register(WagonType)
class WagonTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'meter_shtok_map')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'warehouse', 'in_qty', 'out_qty', 'net_quantity_display', 'min_stock', 'created_at')
    search_fields = ('code', 'name', 'category')
    list_filter = ('warehouse', 'category', 'created_at')
    ordering = ('code',)

    def net_quantity_display(self, obj):
        return obj.net_quantity()
    net_quantity_display.short_description = "Net Qoldiq"

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'product', 'manufacture_date', 'expiry_date', 'in_qty', 'out_qty', 'quantity')
    search_fields = ('batch_number', 'product__name')
    list_filter = ('manufacture_date', 'expiry_date', 'product')
    ordering = ('-manufacture_date',)

@admin.register(Wagon)
class WagonAdmin(admin.ModelAdmin):
    list_display = ('wagon_number', 'wagon_type', 'net_weight', 'meter_weight', 'capacity', 'volume', 'price_sum', 'condition')
    search_fields = ('wagon_number', 'wagon_type')
    list_filter = ('wagon_type', 'condition')
    ordering = ('wagon_number',)

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'document_number', 'product', 'wagon', 'movement_type', 'quantity', 'price_sum', 'created_at')
    search_fields = ('document_number', 'product__name', 'wagon__wagon_number')
    list_filter = ('movement_type', 'date', 'product')
    ordering = ('-date',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)

@admin.register(Reservoir)
class ReservoirAdmin(admin.ModelAdmin):
    list_display = ('name', 'warehouse', 'capacity', 'product', 'in_qty', 'out_qty', 'quantity')
    search_fields = ('name', 'warehouse__name', 'product__name')
    list_filter = ('warehouse', 'product')
    ordering = ('name',)

@admin.register(ReservoirMovement)
class ReservoirMovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'reservoir', 'product', 'movement_type', 'quantity', 'created_at')
    search_fields = ('reservoir__name', 'product__name')
    list_filter = ('movement_type', 'date', 'reservoir')
    ordering = ('-date',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'object_id', 'action', 'timestamp')
    search_fields = ('model_name', 'object_id', 'action')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(LocalClient)
class LocalClientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(LocalMovement)
class LocalMovementAdmin(admin.ModelAdmin):
    list_display = ('client', 'wagon', 'product', 'date', 'density', 'temperature', 'liter', 'mass')
    search_fields = ('client__name', 'product__name', 'wagon__wagon_number')
    list_filter = ('date', 'client', 'product')
    ordering = ('-date',)

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ['product', 'wagon', 'reservoir', 'quantity', 'movement', 'created_at']
    search_fields = ['product__name', 'wagon__wagon_number', 'reservoir__name']
    list_filter = ['product', 'wagon', 'reservoir', 'movement']
    ordering = ['-created_at']



