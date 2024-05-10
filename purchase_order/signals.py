import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, Vendor

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    """Update the vendor's historical performance based on the purchase order status"""
    vendor = instance.vendor
    vendor_historical_performance = vendor.historicalperformance_set.first()
    avg_quality_rating = vendor_historical_performance.quality_rating_avg if vendor_historical_performance else 0
    on_time_delivery_rate = vendor_historical_performance.on_time_delivery_rate if vendor_historical_performance else 0
        
    if instance.status == PurchaseOrder.COMPLETED:  # Only perform this when the order is completed
        # Calculate the on-time delivery rate of the vendor
        logger.info("Calculate the on-time delivery rate of vendor: (%s)", str(instance.vendor.id))
        completed_orders_count = vendor.purchaseorder_set.filter(status=PurchaseOrder.COMPLETED).count()
        # this code if the completed_date field doesn't exist
        # the formula is on_time_delivery_rate = on_time_orders_count / completed_orders_count * 100
        # so on_time_orders_count = on_time_delivery_rate * completed_orders_count / 100
        # if instance.delivery_date >= timezone.now():
        #     on_time_orders_count = 1
        # if vendor_historical_performance:
        #     on_time_delivery_rate = vendor_historical_performance.on_time_delivery_rate
        #     on_time_orders_count += (on_time_delivery_rate * (completed_orders_count - 1)) / 100
        #     on_time_delivery_rate = (on_time_orders_count / completed_orders_count) * 100
        # else:
        #     on_time_delivery_rate = (on_time_orders_count / completed_orders_count) * 100
        
        on_time_delivered_pos = vendor.purchaseorder_set.filter(
            status=PurchaseOrder.COMPLETED,
            delivery_date__gte=timezone.now()
        ).count()
        if completed_orders_count > 0:
            on_time_delivery_rate = (on_time_delivered_pos / completed_orders_count) * 100

        # Calculate the average quality rating of the vendor
        logger.info("Calculate the average quality rating of vendor: (%s)", str(instance.vendor.id))
        quality_ratings = vendor.purchaseorder_set.filter(quality_rating__isnull=False).values_list('quality_rating', flat=True)
        if quality_ratings:
            avg_quality_rating = sum(quality_ratings) / len(quality_ratings)
        
    # Update the on_time_delivery_rate of the vendor
    vendor.historicalperformance_set.update_or_create(
        defaults={'on_time_delivery_rate': on_time_delivery_rate, 'quality_rating_avg': avg_quality_rating}
    )

@receiver(pre_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    """Update the vendor's historical performance based on the purchase order status"""
    vendor = instance.vendor
    vendor_historical_performance = vendor.historicalperformance_set.first()
    fulfillment_rate = vendor_historical_performance.fulfillment_rate if vendor_historical_performance else 0
    
    # Update the fulfillment rate of the vendor
    logger.info("Update the fulfillment rate of vendor: (%s)", str(instance.vendor.id))
    if instance.pk:  # Only if the instance is already saved in the database
        previous_instance = PurchaseOrder.objects.get(pk=instance.pk)
        previous_status = previous_instance.status
        current_status = instance.status
        if previous_status != current_status:
            completed_orders = vendor.purchaseorder_set.filter(status=PurchaseOrder.COMPLETED, issue_date__isnull=True).count()
            total_orders = vendor.purchaseorder_set.all().count()
            if total_orders > 0 and current_status == PurchaseOrder.COMPLETED and instance.issue_date is None:
                fulfillment_rate = ((completed_orders + 1) / total_orders) * 100
            
            # Update the on_time_delivery_rate of the vendor
            vendor.historicalperformance_set.update_or_create(
                defaults={'fulfillment_rate': fulfillment_rate}
            )
