# Generated by Django 5.1.6 on 2025-03-07 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('subscriptions', '0002_alter_subscription_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='groups',
            field=models.ManyToManyField(to='auth.group'),
        ),
    ]
