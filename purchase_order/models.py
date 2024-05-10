import uuid
from hashid_field import HashidAutoField
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from vendor.models import Vendor


class PurchaseOrder(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    id = HashidAutoField(primary_key=True)
    number = models.CharField(max_length=50, unique=True, editable=False)  # Make it non-editable
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_index=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, db_index=True)
    quality_rating = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(5)])
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        """Validate the model fields."""
        """quantity must greater than zero and delivery date must be greater or same with order date."""
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than zero.'})
        if self.order_date and self.delivery_date and self.delivery_date < self.order_date:
            raise ValidationError({"delivery_date": "Delivery date must be greater or same with order date."})
    
    def save(self, *args, **kwargs):
        if not self.number:  # Generate PO number if not provided
            self.number = uuid.uuid4().hex[:12]  # Use first 12 characters of UUID
        super(PurchaseOrder, self).save(*args, **kwargs)

    def __str__(self):
        return self.number
