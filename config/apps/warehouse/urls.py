from django.urls import path
from .views import (
    index, dashboard, MovementReportView,
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView,
    WagonListView, MovementListView, InventoryListView,
    movement_create,
    BatchListView, BatchDetailView, BatchCreateView, BatchUpdateView,
    export_products_excel, export_movements_excel, export_wagons_excel
)

app_name = 'warehouse'

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('movements/report/', MovementReportView.as_view(), name='movement_report'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('wagons/', WagonListView.as_view(), name='wagon_list'),
    path('movements/', MovementListView.as_view(), name='movement_list'),
    path('movements/create/', movement_create, name='movement_create'),
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('batches/', BatchListView.as_view(), name='batch_list'),
    path('batches/create/', BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:pk>/update/', BatchUpdateView.as_view(), name='batch_update'),
    path('export/products/excel/', export_products_excel, name='export_products_excel'),
    path('export/movements/excel/', export_movements_excel, name='export_movements_excel'),
    path('export/wagons/excel/', export_wagons_excel, name='export_wagons_excel'),
]
