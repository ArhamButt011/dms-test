# Generated by Django 4.2.4 on 2024-01-24 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0043_rfi_atchd_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delay_log',
            name='dely_log_num',
        ),
        migrations.RemoveField(
            model_name='delay_log',
            name='totl_impct',
        ),
    ]