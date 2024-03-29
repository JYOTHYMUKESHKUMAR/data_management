# Generated by Django 5.0 on 2024-02-22 08:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cash_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_cash_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_actual_cash_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_actual_cash_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'Dashboard',
                'verbose_name_plural': 'Dashboard',
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('cash_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cash_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('actual_cash_in', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('actual_cash_out', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('actual_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('planned_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UpdateCashIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_source', models.CharField(max_length=250)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Scheduled', 'Scheduled')], default='update', max_length=50)),
                ('remark', models.TextField(blank=True)),
                ('cash_in', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('processed', models.BooleanField(default=False)),
                ('projects', models.CharField(default='', max_length=250)),
                ('division', models.CharField(choices=[('catalyst', 'Catalyst'), ('oil_and_gas', 'Oil and Gas'), ('general_chemicals', 'General Chemicals'), ('overhead', 'Overhead')], default='update', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UpdateCashOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_source', models.CharField(max_length=250)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='update', max_length=50)),
                ('remark', models.TextField(blank=True)),
                ('cash_out', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('processed', models.BooleanField(default=False)),
                ('priority_level', models.CharField(choices=[('urgent', 'Urgent'), ('important', 'Important'), ('normal', 'Normal')], default='normal', max_length=20)),
                ('projects', models.CharField(default='', max_length=250)),
                ('division', models.CharField(choices=[('catalyst', 'Catalyst'), ('oil_and_gas', 'Oil and Gas'), ('general_chemicals', 'General Chemicals'), ('overhead', 'Overhead')], default='update', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('available', models.BooleanField(default=True)),
                ('date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='product')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashflow.category')),
            ],
        ),
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('action_description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashflow_user_action_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
