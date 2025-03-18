# accounting/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.warehouse.models import Movement
from .models import FinanceOperation

@receiver(post_save, sender=Movement)
def create_finance_operation_for_movement(sender, instance, created, **kwargs):
    if created:
        if instance.movement_type == 'out':
            FinanceOperation.objects.create(
                movement=instance,
                operation_type='income',
                amount=instance.price_sum,
                note=f"Auto finance record for movement {instance.id}"
            )
        else:
            FinanceOperation.objects.create(
                movement=instance,
                operation_type='expense',
                amount=instance.price_sum,
                note=f"Purchase record for movement {instance.id}"
            )
