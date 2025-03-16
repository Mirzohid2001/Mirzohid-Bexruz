import io
import pandas as pd
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from .models import Product, Wagon, Movement, Inventory, Batch
from .forms import MovementForm, ProductForm, WagonForm, BatchForm
from .filters import MovementFilter, ProductFilter, WagonFilter

def index(request):
    return render(request, 'warehouse/index.html')


def dashboard(request):
    total_in = Movement.objects.filter(movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
    total_out = Movement.objects.filter(movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
    net_movement = total_in - total_out

    inventory_summary = Inventory.objects.select_related('product').all()
    product_aggregates = Product.objects.annotate(net_qty=F('in_qty') - F('out_qty'))

    context = {
        'total_in': total_in,
        'total_out': total_out,
        'net_movement': net_movement,
        'inventory_summary': inventory_summary,
        'product_aggregates': product_aggregates,
    }
    return render(request, 'warehouse/dashboard.html', context)


class MovementReportView(TemplateView):
    template_name = "warehouse/movement_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movements = Movement.objects.all()
        total_in = movements.filter(movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
        total_out = movements.filter(movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
        net = total_in - total_out
        context.update({
            'movements': movements,
            'total_in': total_in,
            'total_out': total_out,
            'net': net,
        })
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'warehouse/product_list.html'
    context_object_name = 'products'
    ordering = ['code']

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter = ProductFilter(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'warehouse/product_detail.html'
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        movements = Movement.objects.filter(product=product)
        total_in = movements.filter(movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
        total_out = movements.filter(movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
        net_qty = total_in - total_out
        context.update({
            'movements': movements,
            'total_in': total_in,
            'total_out': total_out,
            'net_qty': net_qty,
        })
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'warehouse/product_create.html'

    def get_success_url(self):
        return reverse('warehouse:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'warehouse/product_update.html'

    def get_success_url(self):
        return reverse('warehouse:product_list')


class WagonListView(ListView):
    model = Wagon
    template_name = 'warehouse/wagon_list.html'
    context_object_name = 'wagons'
    ordering = ['wagon_number']

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter = WagonFilter(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class MovementListView(ListView):
    model = Movement
    template_name = 'warehouse/movement_list.html'
    context_object_name = 'movements'
    ordering = ['-date']

    def get_queryset(self):
        qs = super().get_queryset().select_related('product', 'wagon', 'batch')
        self.filter = MovementFilter(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class InventoryListView(ListView):
    model = Inventory
    template_name = 'warehouse/inventory_list.html'
    context_object_name = 'inventory'


class BatchListView(ListView):
    model = Batch
    template_name = 'warehouse/batch_list.html'
    context_object_name = 'batches'
    ordering = ['-id']


class BatchDetailView(DetailView):
    model = Batch
    template_name = 'warehouse/batch_detail.html'
    context_object_name = 'batch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = self.get_object()
        movements = Movement.objects.filter(batch=batch)
        total_in = movements.filter(movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
        total_out = movements.filter(movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
        net_qty = total_in - total_out
        context.update({
            'movements': movements,
            'total_in': total_in,
            'total_out': total_out,
            'net_qty': net_qty,
        })
        return context


class BatchCreateView(CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'warehouse/batch_form.html'

    def get_success_url(self):
        return reverse('warehouse:batch_list')


class BatchUpdateView(UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'warehouse/batch_form.html'
    def get_success_url(self):
        return reverse('warehouse:batch_list')


def movement_create(request):
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('warehouse:movement_list'))
    else:
        form = MovementForm()
    return render(request, 'warehouse/movement_create.html', {'form': form})



def export_products_excel(request):
    qs = Product.objects.all().values(
        'code', 'name', 'category', 'volume', 'weight', 
        'price_usd', 'price_sum', 'in_qty', 'out_qty'
    )
    df = pd.DataFrame(list(qs))
    df.rename(columns={
        'code': 'Kod',
        'name': 'Mahsulot nomi',
        'category': 'Kategoriya',
        'volume': 'Hajmi (l)',
        'weight': "Og'irligi (kg)",
        'price_usd': "Narx (USD)",
        'price_sum': "Narx (so'm)",
        'in_qty': "Umumiy kirim",
        'out_qty': "Umumiy chiqim",
    }, inplace=True)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Products')
    writer.save()
    output.seek(0)
    response = HttpResponse(
        output.read(), 
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    return response


def export_movements_excel(request):
    qs = Movement.objects.select_related('product', 'wagon').all().values(
        'document_number', 'product__name', 'wagon__wagon_number', 
        'date', 'movement_type', 'quantity', 'price_sum', 'note'
    )
    df = pd.DataFrame(list(qs))
    df.rename(columns={
        'document_number': 'Hujjat #',
        'product__name': 'Mahsulot',
        'wagon__wagon_number': 'Vagon raqami',
        'date': 'Sana',
        'movement_type': 'Harakat turi',
        'quantity': 'Miqdor',
        'price_sum': "Narx (so'm)",
        'note': 'Izoh',
    }, inplace=True)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Movements')
    writer.save()
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="movements.xlsx"'
    return response


def export_wagons_excel(request):
    qs = Wagon.objects.all().values(
        'wagon_number', 'wagon_type', 'net_weight', 'meter_weight',
        'capacity', 'volume', 'price_sum', 'condition'
    )
    df = pd.DataFrame(list(qs))
    df.rename(columns={
        'wagon_number': 'Vagon raqami',
        'wagon_type': 'Vagon turi',
        'net_weight': "Netto (kg)",
        'meter_weight': "Meter (kg)",
        'capacity': "Sig'im (tonna)",
        'volume': "Hajmi (L)",
        'price_sum': "Umumiy summa (so'm)",
        'condition': "Holati",
    }, inplace=True)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Wagons')
    writer.save()
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="wagons.xlsx"'
    return response
