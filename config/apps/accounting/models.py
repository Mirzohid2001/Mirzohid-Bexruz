from django.db import models
from apps.warehouse.models import Movement, ReservoirMovement



class FinanceOperation(models.Model):
    OPERATION_TYPES = (
        ('income', 'Daromad'),
        ('expense', 'Xarajat'),
    )
    movement = models.OneToOneField(Movement, on_delete=models.CASCADE, blank=True, null=True)
    reservoir_movement = models.OneToOneField(ReservoirMovement, on_delete=models.CASCADE, blank=True, null=True)
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPES)
    amount = models.FloatField(default=0, verbose_name="Summa")
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_type} - {self.amount}"
