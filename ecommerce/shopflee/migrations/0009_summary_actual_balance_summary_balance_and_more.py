# Generated by Django 5.0 on 2023-12-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0008_alter_summary_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='actual_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='summary',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='summary',
            name='planned_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
