# Generated by Django 5.0 on 2023-12-13 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0004_alter_summary_actual_cash_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='cash_in',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='summary',
            name='cash_out',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
