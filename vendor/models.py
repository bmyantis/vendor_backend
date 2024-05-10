import uuid
from hashid_field import HashidAutoField

from django.db import models


class Vendor(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    code = models.CharField(max_length=50, unique=True, editable=False)  # Make it non-editable

    def save(self, *args, **kwargs):
        if not self.code:  # Generate vendor code if not provided
            self.code = uuid.uuid4().hex[:12]  # Use first 12 characters of UUID
        super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class HistoricalPerformance(models.Model):
    id = HashidAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.vendor}"
