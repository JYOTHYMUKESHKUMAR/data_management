# Generated by Django 5.0 on 2024-02-22 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0002_rename_division_updatecashin_cost_center_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='updatecashin',
            old_name='projects',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='updatecashout',
            old_name='projects',
            new_name='project',
        ),
    ]
