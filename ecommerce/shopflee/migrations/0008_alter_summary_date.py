# Generated by Django 5.0 on 2023-12-13 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0007_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
