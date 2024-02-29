# Generated by Django 5.0 on 2023-12-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0019_delete_availablebalance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]