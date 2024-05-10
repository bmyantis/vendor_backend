# Generated by Django 4.2.11 on 2024-05-09 13:54

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('on_time_delivery_rate', models.FloatField(default=0)),
                ('quality_rating_avg', models.FloatField(default=0)),
                ('average_response_time', models.FloatField(default=0)),
                ('fulfillment_rate', models.FloatField(default=0)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
        ),
    ]
