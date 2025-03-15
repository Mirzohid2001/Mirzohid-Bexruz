import django_filters
from .models import Movement, Product, Wagon

class MovementFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date", label="Sana oralig'i")
    product = django_filters.CharFilter(field_name="product__name", lookup_expr='icontains', label="Mahsulot nomi")
    wagon = django_filters.CharFilter(field_name="wagon__wagon_number", lookup_expr='icontains', label="Vagon raqami")
    movement_type = django_filters.ChoiceFilter(choices=Movement.MOVEMENT_TYPES, label="Harakat turi")

    class Meta:
        model = Movement
        fields = ['date', 'product', 'wagon', 'movement_type']


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains', label="Mahsulot nomi")
    category = django_filters.CharFilter(field_name="category", lookup_expr='icontains', label="Kategoriya")

    class Meta:
        model = Product
        fields = ['name', 'category']


class WagonFilter(django_filters.FilterSet):
    wagon_number = django_filters.CharFilter(field_name="wagon_number", lookup_expr='icontains', label="Vagon raqami")
    wagon_type = django_filters.CharFilter(field_name="wagon_type", lookup_expr='icontains', label="Vagon turi")

    class Meta:
        model = Wagon
        fields = ['wagon_number', 'wagon_type']
