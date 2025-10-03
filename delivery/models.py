from django.db import models


class DeliveryZone(models.Model):
    pincode = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    is_deliverable = models.BooleanField(default=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_days = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pincode} - {self.city}, {self.state}"

    class Meta:
        ordering = ['pincode']


class DeliveryCheck(models.Model):
    pincode = models.CharField(max_length=10)
    is_deliverable = models.BooleanField()
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_days = models.PositiveIntegerField(default=3)
    message = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pincode} - {'Deliverable' if self.is_deliverable else 'Not Deliverable'}"

    class Meta:
        ordering = ['-checked_at']
