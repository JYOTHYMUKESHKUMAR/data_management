# Generated by Django 5.0 on 2023-12-31 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0034_remove_updatecashin_processed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatecashin',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='updatecashout',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
