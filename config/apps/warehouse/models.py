from django.db import models
from django.db.models import Sum, Q
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
        verbose_name = "Ombor"
        verbose_name_plural = "Omborlar"


class Product(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Kod")
    name = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategoriya")
    volume = models.FloatField(verbose_name="Hajmi (l)", default=0)
    weight = models.FloatField(verbose_name="Og'irligi (kg)", default=0)
    density = models.FloatField(verbose_name="Zichlik (kg/l)", default=0)
    specific_weight = models.FloatField(verbose_name="Udel Og'irligi", default=0)
    price_usd = models.FloatField(verbose_name="Narx (USD)", default=0, null=True, blank=True)
    price_sum = models.FloatField(verbose_name="Narx (so'm)", default=0, null=True, blank=True)
    in_qty = models.FloatField(verbose_name="Umumiy kirim (qty)", default=0)
    min_stock = models.FloatField(verbose_name="Minimum ruxsat etilgan qoldiq", default=0)
    out_qty = models.FloatField(verbose_name="Umumiy chiqim (qty)", default=0)
    description = models.TextField(verbose_name="Tavsif", blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Ombor", blank=True, null=True)
    zone = models.CharField(max_length=50, verbose_name="Zona", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    def save(self, *args, **kwargs):
        if self.volume and self.weight:
            self.density = self.weight / self.volume
            self.specific_weight = self.density
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def net_quantity(self):
        if self.in_qty is None:
            self.in_qty = 0
        if self.out_qty is None:
            self.out_qty = 0
        return self.in_qty - self.out_qty


    def check_threshold(self):
        current_qty = self.net_quantity()
        if current_qty < self.min_stock:
            message = f"Ogohlantirish: Mahsulot '{self.name}' (Kod: {self.code}) qoldigi {current_qty} ga tushdi. Minimum: {self.min_stock}. Iltimos, to'ldiring!"
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
        return (self.in_qty or 0) - (self.out_qty or 0)

    class Meta:
        unique_together = ('product', 'batch_number')
        verbose_name = "Партия"
        verbose_name_plural = "Партиялар"

class WagonType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Vagon turi")
    meter_shtok_map = models.JSONField(blank=True, null=True, 
        help_text="Masalan: {'1.0': 1000, '1.2':1200}, meter → litr")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Vagon turi"
        verbose_name_plural = "Vagon turlari"


class Wagon(models.Model):
    wagon_number = models.CharField(max_length=20, unique=True, verbose_name="Vagon raqami")
    wagon_type = models.ForeignKey(WagonType, on_delete=models.SET_NULL, null=True, verbose_name="Vagon tipi")
    net_weight = models.FloatField(verbose_name="Netto og'irligi", default=0)
    meter_weight = models.FloatField(verbose_name="Meter og'irligi", default=0)
    capacity = models.FloatField(verbose_name="Sig'im (tonna)", default=0)
    volume = models.FloatField(verbose_name="Hajmi (L)", default=0)
    price_sum = models.FloatField(verbose_name="Umumiy summa (so'm)", default=0)
    condition = models.CharField(max_length=50, verbose_name="Holati", default="Yaxshi")

    def __str__(self):
        return f"{self.wagon_number} ({self.wagon_type})"
    
    def calculate_litr_from_meter(self, meter_value: float) -> float:
        if not self.wagon_type or not self.wagon_type.meter_shtok_map:
            return 0
        best_key = str(meter_value)
        return self.wagon_type.meter_shtok_map.get(best_key, 0)

    class Meta:
        ordering = ['wagon_number']
        verbose_name = "Вагон"
        verbose_name_plural = "Вагонлар"

class LocalClient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Klient nomi")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klientlar"
    

class LocalMovement(models.Model):
    client = models.ForeignKey(
        LocalClient, on_delete=models.CASCADE, verbose_name="Klient"
    )
    wagon = models.ForeignKey(
        Wagon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vagon"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mahsulot"
    )
    date = models.DateField(verbose_name="Sana", default=timezone.now)
    density = models.FloatField(verbose_name="Zichlik (Удел)", default=0)
    temperature = models.FloatField(verbose_name="Harorat (°C)", default=0)
    liter = models.FloatField(verbose_name="Litr", default=0)
    mass = models.FloatField(verbose_name="Massa (kg)", default=0)
    doc_ton = models.FloatField(verbose_name="Hujjat bo'yicha ton", default=0)
    fact_ton = models.FloatField(verbose_name="Fakt ton", default=0)
    difference_ton = models.FloatField(verbose_name="Farq (ton)", default=0, editable=False)
    specific_weight = models.FloatField(verbose_name="Udel og‘irlik", default=0, blank=True, null=True)

    note = models.TextField(verbose_name="Izoh", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.density and self.liter:
            self.mass = self.density * self.liter
            self.specific_weight = self.density
        self.difference_ton = self.doc_ton - self.fact_ton

        super().save(*args, **kwargs)

    def clean(self):
        if self.liter < 0 or self.mass < 0:
            raise ValidationError("Litr yoki massa manfiy bo'lishi mumkin emas.")

    def __str__(self):
        return f"{self.client.name} - {self.product} - {self.mass} kg"

    class Meta:
        verbose_name = "Harakat"
        verbose_name_plural = "Harakatlar"

class Movement(models.Model):
    MOVEMENT_TYPES = (
        ('in', "Kirim"),
        ('out', "Chiqim"),
    )
    document_number = models.CharField(max_length=50, verbose_name="Hujjat raqami", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    wagon = models.ForeignKey(Wagon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vagon")
    date = models.DateField(verbose_name="Sana", default=timezone.now)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name="Harakat turi")
    quantity = models.FloatField(verbose_name="Miqdor (qty)")
    density = models.FloatField(verbose_name="Zichlik", default=0, null=True, blank=True)
    liter = models.FloatField(verbose_name="Litr", default=0, null=True, blank=True)
    specific_weight = models.FloatField(verbose_name="Udel og'irlik", default=0, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Parтия")
    price_sum = models.FloatField(verbose_name="Narx (so'm)", default=0)
    note = models.TextField(verbose_name="Izoh", blank=True, null=True)
    doc_ton = models.FloatField(verbose_name="Hujjat bo'yicha ton", default=0)
    fact_ton = models.FloatField(verbose_name="Fakt ton", default=0)
    difference_ton = models.FloatField(verbose_name="Farq (ton)", default=0, editable=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Ombor", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def save(self, *args, **kwargs):
        self.difference_ton = self.doc_ton - self.fact_ton

        if self.density and self.liter:
            self.quantity = self.density * self.liter
            self.specific_weight = self.density

        super().save(*args, **kwargs)

        product_obj = self.product
        total_in = Movement.objects.filter(product=product_obj, movement_type='in').aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_out = Movement.objects.filter(product=product_obj, movement_type='out').aggregate(Sum('quantity'))['quantity__sum'] or 0
        product_obj.in_qty = total_in
        product_obj.out_qty = total_out
        product_obj.save()
        inv, created = Inventory.objects.get_or_create(product=product_obj)
        inv.quantity = total_in - total_out
        inv.save()
        product_obj.check_threshold()

    def clean(self):
        if self.movement_type == 'out':
            available = self.product.net_quantity() or 0
            qty = self.quantity or 0
            if qty > available:
                raise ValidationError(
                    f"Mavjud qoldiq ({available}) dan oshiq chiqim kiritish mumkin emas!"
                )

    def __str__(self):
        return f"{self.date} - {self.product.name} - {self.get_movement_type_display()} - {self.quantity}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Движение"
        verbose_name_plural = "Движения"


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.FloatField(verbose_name="Qoldiq (qty)", default=0)

    def __str__(self):
        return f"{self.product.name} qoldiq: {self.quantity}"


class Reservoir(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Ombor", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Rezervuar nomi")
    capacity = models.FloatField(verbose_name="Sig'im (L yoki tonna)", default=0)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Saqlanayotgan mahsulot", blank=True, null=True)
    in_qty = models.FloatField(default=0, verbose_name="Kirim (qty)")
    out_qty = models.FloatField(default=0, verbose_name="Chiqim (qty)")
    quantity = models.FloatField(default=0, verbose_name="Joriy qoldiq (qty)")

    def __str__(self):
        return f"{self.name} (Qoldiq: {self.quantity})"


class ReservoirMovement(models.Model):
    MOVEMENT_TYPES = (
        ('in', "Kirim (to'ldirish)"),
        ('out', "Chiqim (bo'shatish)"),
    )
    reservoir = models.ForeignKey(Reservoir, on_delete=models.CASCADE, verbose_name="Rezervuar")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Mahsulot", blank=True, null=True)
    date = models.DateField(verbose_name="Sana", default=timezone.now)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name="Harakat turi")
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
        total_in = ReservoirMovement.objects.filter(reservoir=res, movement_type='in').aggregate(total=Sum('quantity'))['total'] or 0
        total_out = ReservoirMovement.objects.filter(reservoir=res, movement_type='out').aggregate(total=Sum('quantity'))['total'] or 0
        res.in_qty = total_in
        res.out_qty = total_out
        res.quantity = total_in - total_out
        res.save()

class Placement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    wagon = models.ForeignKey('Wagon', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vagon")
    reservoir = models.ForeignKey('Reservoir', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rezervuar")
    quantity = models.FloatField(verbose_name="Qisman miqdor (litr yoki kg)", default=0)
    movement = models.ForeignKey('Movement', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Harakat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.wagon and not self.reservoir:
            raise ValidationError("Vagon yoki Rezervuarni tanlashingiz kerak.")
        if self.wagon and self.reservoir:
            raise ValidationError("Faqat bitta joy tanlanishi mumkin: vagon yoki rezervuar.")
        if self.quantity <= 0:
            raise ValidationError("Miqdor manfiy yoki 0 bo‘lishi mumkin emas.")
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        place = self.wagon.wagon_number if self.wagon else self.reservoir.name
        return f"{self.product.name}: {self.quantity} → {place}"



class AuditLog(models.Model):
    action = models.CharField(max_length=20)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} [{self.object_id}] {self.action} at {self.timestamp}"
