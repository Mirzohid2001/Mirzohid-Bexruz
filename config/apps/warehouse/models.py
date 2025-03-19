from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.warehouse.utils import send_telegram_message


class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ombor nomi")
    location = models.CharField(max_length=200, verbose_name="Manzil", blank=True, null=True)
    zone = models.CharField(max_length=50, verbose_name="Zona", blank=True, null=True)
    location_code = models.CharField(max_length=20, verbose_name="Location Code", blank=True, null=True)
    description = models.TextField(verbose_name="Tavsif", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "склад"
        verbose_name_plural = "склады"


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Kod")
    name = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategoriya")
    volume = models.FloatField(verbose_name="Hajmi (l)", default=0)
    weight = models.FloatField(verbose_name="Og'irligi (kg)", default=0)
    price_usd = models.FloatField(verbose_name="Narx (USD)", default=0, null=True, blank=True)
    price_sum = models.FloatField(verbose_name="Narx (so'm)", default=0, null=True, blank=True)
    in_qty = models.FloatField(verbose_name="Umumiy kirim (qty)", default=0)
    min_stock = models.FloatField(verbose_name="Minimum ruxsat etilgan qoldiq", default=0)
    out_qty = models.FloatField(verbose_name="Umumiy chiqim (qty)", default=0)
    description = models.TextField(verbose_name="Tavsif", blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, verbose_name="Ombor", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    zone = models.CharField(max_length=50, verbose_name="Zona", blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def net_quantity(self):
        return self.in_qty - self.out_qty

    def check_threshold(self):
        current_qty = self.net_quantity()
        if current_qty < self.min_stock:
            message = (
                f"Ogohlantirish: Mahsulot '{self.name}' (Kod: {self.code}) "
                f"qoldigi {current_qty} ga tushdi. Minimum ruxsat etilgan qoldiq: {self.min_stock}. "
                "Iltimos, to'ldiring!"
            )
            send_telegram_message(message)

    class Meta:
        ordering = ['code']
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    batch_number = models.CharField(max_length=50, verbose_name="Partiya raqami")
    manufacture_date = models.DateField(blank=True, null=True, verbose_name="Ishlab chiqarilgan sana")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Yaroqlilik muddati")

    in_qty = models.FloatField(default=0, verbose_name="Kirim (qty)")
    out_qty = models.FloatField(default=0, verbose_name="Chiqim (qty)")
    quantity = models.FloatField(default=0, verbose_name="Joriy qoldiq (qty)")

    def __str__(self):
        return f"{self.batch_number} - {self.product.name}"

    def net_quantity(self):
        return self.in_qty - self.out_qty

    class Meta:
        unique_together = ('product', 'batch_number')
        verbose_name = "Партия"
        verbose_name_plural = "Партиялар"


class Wagon(models.Model):
    wagon_number = models.CharField(max_length=20, unique=True, verbose_name="Vagon raqami")
    wagon_type = models.CharField(max_length=50, verbose_name="Vagon turi")
    net_weight = models.FloatField(verbose_name="Netto og'irligi", default=0)
    meter_weight = models.FloatField(verbose_name="Meter og'irligi", default=0)
    capacity = models.FloatField(verbose_name="Sig'im (tonna)", default=0)
    volume = models.FloatField(verbose_name="Hajmi (L)", default=0)
    price_sum = models.FloatField(verbose_name="Umumiy summa (so'm)", default=0)
    condition = models.CharField(max_length=50, verbose_name="Holati", default="Yaxshi")

    def __str__(self):
        return f"{self.wagon_number} ({self.wagon_type})"

    class Meta:
        ordering = ['wagon_number']
        verbose_name = "Вагон"
        verbose_name_plural = "Вагонлар"


class Movement(models.Model):
    MOVEMENT_TYPES = (
        ('in', "Kirim"),
        ('out', "Chiqim"),
    )
    document_number = models.CharField(max_length=50, verbose_name="Hujjat raqami", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Partiya")
    wagon = models.ForeignKey(Wagon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vagon")
    date = models.DateField(verbose_name="Sana", default=timezone.now)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name="Harakat turi")
    quantity = models.FloatField(verbose_name="Miqdor (qty)")
    price_sum = models.FloatField(verbose_name="Narx (so'm)", default=0)
    note = models.TextField(verbose_name="Izoh", blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Ombor", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return f"{self.date} - {self.product.name} - {self.get_movement_type_display()} - {self.quantity}"

    def clean(self):
        if self.movement_type == 'out':
            available = self.product.net_quantity()
            if self.quantity > available:
                raise ValidationError(
                    f"Mavjud qoldiq ({available}) dan oshiq chiqim kiritish mumkin emas!"
                )

    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)

        product_obj = self.product
        all_in = Movement.objects.filter(product=product_obj, movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
        all_out = Movement.objects.filter(product=product_obj, movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
        product_obj.in_qty = all_in
        product_obj.out_qty = all_out
        product_obj.save()

        if self.batch:
            batch_obj = self.batch
            batch_in = Movement.objects.filter(batch=batch_obj, movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
            batch_out = Movement.objects.filter(batch=batch_obj, movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
            batch_obj.in_qty = batch_in
            batch_obj.out_qty = batch_out
            batch_obj.quantity = batch_in - batch_out
            batch_obj.save()

        inv, created = Inventory.objects.get_or_create(product=product_obj)
        inv.quantity = all_in - all_out
        inv.save()

        product_obj.check_threshold()

    class Meta:
        ordering = ['-date']
        verbose_name = "Движение"
        verbose_name_plural = "Движения"


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.FloatField(verbose_name="Qoldiq (qty)", default=0)

    def __str__(self):
        return f"{self.product.name} qoldiq: {self.quantity}"
    
    class Meta:
        verbose_name = "Инвентарь"
        verbose_name_plural = "Инвентарь"
    
class Reservoir(models.Model):
    warehouse = models.ForeignKey(
        'Warehouse', on_delete=models.CASCADE, 
        verbose_name="Ombor", blank=True, null=True
    )
    name = models.CharField(max_length=100, verbose_name="Rezervuar nomi")
    capacity = models.FloatField(verbose_name="Sig'im (L yoki tonna)", default=0)
    product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, 
        verbose_name="Saqlanayotgan mahsulot", blank=True, null=True
    )

    in_qty = models.FloatField(default=0, verbose_name="Kirim (qty)")
    out_qty = models.FloatField(default=0, verbose_name="Chiqim (qty)")
    quantity = models.FloatField(default=0, verbose_name="Joriy qoldiq (qty)")

    def __str__(self):
        return f"{self.name} (Qoldiq: {self.quantity})"
    
    class Meta:
        verbose_name = "Rezervuar"
        verbose_name_plural = "Rezervuarlar"


class ReservoirMovement(models.Model):
    MOVEMENT_TYPES = (
        ('in', "Kirim (to'ldirish)"),
        ('out', "Chiqim (bo'shatish)"),
    )
    reservoir = models.ForeignKey(
        Reservoir, on_delete=models.CASCADE, 
        verbose_name="Rezervuar"
    )
    product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, 
        verbose_name="Mahsulot", blank=True, null=True
    )
    date = models.DateField(verbose_name="Sana", default=timezone.now)
    movement_type = models.CharField(
        max_length=3, choices=MOVEMENT_TYPES, verbose_name="Harakat turi"
    )
    quantity = models.FloatField(verbose_name="Miqdor (qty)")
    note = models.TextField(verbose_name="Izoh", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return f"{self.date} - {self.reservoir.name} - {self.get_movement_type_display()} - {self.quantity}"
    
    def clean(self):
        if self.movement_type == 'out':
            available = self.reservoir.in_qty - self.reservoir.out_qty
            if self.quantity > available:
                raise ValidationError(
                    f"Rezervuarda faqat {available} mavjud, lekin {self.quantity} chiqim qilinmoqda!"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        res = self.reservoir
        total_in = ReservoirMovement.objects.filter(
            reservoir=res, movement_type='in'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_out = ReservoirMovement.objects.filter(
            reservoir=res, movement_type='out'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        res.in_qty = total_in
        res.out_qty = total_out
        res.quantity = total_in - total_out
        res.save()

    class Meta:
        verbose_name = "Rezervuar harakati"
        verbose_name_plural = "Rezervuar harakatlari"


class AuditLog(models.Model):
    action = models.CharField(max_length=20)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} [{self.object_id}] {self.action} at {self.timestamp}"
    
    class Meta:
        verbose_name = "Audit log"
        verbose_name_plural = "Audit logs"