# Generated by Django 5.0 on 2023-12-20 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0024_remove_summary_available_balance'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AvailableBalance',
        ),
    ]
