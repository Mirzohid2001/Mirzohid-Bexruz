from django.urls import path
from .views import (
    index, dashboard, MovementReportView,
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView,
    WagonListView, MovementListView, InventoryListView,
    MovementCreateView,
    BatchListView, BatchDetailView, BatchCreateView, BatchUpdateView,
    export_products_excel, export_movements_excel, export_wagons_excel ,ReservoirCreateView, ReservoirListView, ReservoirDetailView, 
    ReservoirUpdateView,ReservoirMovementListView, ReservoirMovementCreateView,WarehouseReportView,LocalClientListView, LocalClientCreateView,
    LocalMovementListView, LocalMovementCreateView,PlacementCreateView, PlacementListView, PlacementUpdateView,WagonDetailView
)

app_name = 'warehouse'

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('movements/report/', MovementReportView.as_view(), name='movement_report'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('wagons/', WagonListView.as_view(), name='wagon_list'),
    path('movements/', MovementListView.as_view(), name='movement_list'),
    path('movements/create/',MovementCreateView.as_view(), name='movement_create'),
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('batches/', BatchListView.as_view(), name='batch_list'),
    path('batches/create/', BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:pk>/update/', BatchUpdateView.as_view(), name='batch_update'),
    path('export/products/excel/', export_products_excel, name='export_products_excel'),
    path('export/movements/excel/', export_movements_excel, name='export_movements_excel'),
    path('export/wagons/excel/', export_wagons_excel, name='export_wagons_excel'),
    path('reservoirs/', ReservoirListView.as_view(), name='reservoir_list'),
    path('reservoirs/create/', ReservoirCreateView.as_view(), name='reservoir_create'),
    path('reservoirs/<int:pk>/', ReservoirDetailView.as_view(), name='reservoir_detail'),
    path('reservoirs/<int:pk>/update/', ReservoirUpdateView.as_view(), name='reservoir_update'),
    path('reservoir-movements/', ReservoirMovementListView.as_view(), name='reservoir_movement_list'),
    path('reservoir-movements/create/', ReservoirMovementCreateView.as_view(), name='reservoir_movement_create'),
    path('warehouse-report/', WarehouseReportView.as_view(), name='warehouse_report'),
    path('local-clients/', LocalClientListView.as_view(), name='localclient_list'),
    path('local-clients/create/', LocalClientCreateView.as_view(), name='localclient_create'),
    path('local-movements/', LocalMovementListView.as_view(), name='localmovement_list'),
    path('local-movements/create/', LocalMovementCreateView.as_view(), name='localmovement_create'),
    path('placements/', PlacementListView.as_view(), name='placement_list'),
    path('placements/create/', PlacementCreateView.as_view(), name='placement_create'),
    path('placements/<int:pk>/update/', PlacementUpdateView.as_view(), name='placement_update'),
    path('wagons/<int:pk>/', WagonDetailView.as_view(), name='wagon_detail'),
]
