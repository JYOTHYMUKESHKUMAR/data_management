# Generated by Django 5.0 on 2024-01-18 09:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopflee', '0040_delete_dashboardsummaryrelation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='updatecashout',
            name='priority_level',
            field=models.CharField(choices=[('urgent', 'Urgent'), ('important', 'Important'), ('normal', 'Normal')], default='normal', max_length=20),
        ),
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('action_description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
