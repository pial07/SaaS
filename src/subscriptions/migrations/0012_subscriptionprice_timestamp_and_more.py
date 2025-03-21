# Generated by Django 5.1.6 on 2025-03-10 06:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0011_subscriptionprice_featured_subscriptionprice_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionprice',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriptionprice',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subscriptionprice',
            name='featured',
            field=models.BooleanField(default=True, help_text='Featured on Django Subscriptions Home Page'),
        ),
        migrations.AlterField(
            model_name='subscriptionprice',
            name='order',
            field=models.IntegerField(default=-1, help_text='Ordering on Django Subscriptions Home Page'),
        ),
    ]
