# Generated by Django 5.0 on 2023-12-31 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0032_updatecashin_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatecashout',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
