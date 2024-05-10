# Generated by Django 4.2.11 on 2024-05-09 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0002_alter_purchaseorder_issue_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='quality_rating',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
