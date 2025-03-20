from django import forms
from .models import Movement, Product, Wagon, Batch, Reservoir, ReservoirMovement,LocalClient, LocalMovement

class MovementForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    density = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'id_density'}))
    liter = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'id_liter'}))
    specific_weight = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'id_specific_weight'}))
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'id':'id_quantity'}))

    class Meta:
        model = Movement
        fields = ['document_number', 'product', 'batch', 'wagon', 'date', 'movement_type', 'density', 'liter', 'specific_weight', 'quantity', 'price_sum', 'note']
        widgets = {
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'wagon': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'price_sum': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'volume', 'weight', 'price_usd', 'price_sum', 'description', 'warehouse']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class WagonForm(forms.ModelForm):
    class Meta:
        model = Wagon
        fields = ['wagon_number', 'wagon_type', 'net_weight', 'meter_weight', 'capacity', 'volume', 'price_sum', 'condition']
        widgets = {
            'wagon_number': forms.TextInput(attrs={'class': 'form-control'}),
            'wagon_type': forms.TextInput(attrs={'class': 'form-control'}),
            'net_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'meter_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_sum': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BatchForm(forms.ModelForm):
    manufacture_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Batch
        fields = ['product', 'batch_number', 'manufacture_date', 'expiry_date']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReservoirForm(forms.ModelForm):
    class Meta:
        model = Reservoir
        fields = ['warehouse', 'name', 'capacity', 'product']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
        }

class ReservoirMovementForm(forms.ModelForm):
    class Meta:
        model = ReservoirMovement
        fields = ['reservoir', 'product', 'date', 'movement_type', 'quantity', 'note']
        widgets = {
            'reservoir': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LocalClientForm(forms.ModelForm):
    class Meta:
        model = LocalClient
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LocalMovementForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LocalMovement
        fields = ['client', 'wagon', 'product', 'date', 'density', 'temperature', 'liter', 'mass', 'note']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'wagon': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'density': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_density'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'liter': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_liter'}),
            'mass': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_mass', 'readonly': 'readonly'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }