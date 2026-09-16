from django.db import models
from django.conf import settings
from courses.models import Group

class Payment(models.Model):
    PAYMENT_TYPES = (
        ('CASH', 'Naqd'),
        ('CARD', 'Karta orqali'),
        ('CLICK', 'Click / Payme'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name="Talaba"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Guruh"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To'lov summasi")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, default='CARD', verbose_name="To'lov turi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="To'langan vaqti")

    def __str__(self):
        return f"{self.student.username} - {self.amount} so'm ({self.group.name})"