# Generated by Django 4.2.4 on 2023-10-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0015_rename_jon_title_dms_dertory_job_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimating',
            name='bidder_phone',
        ),
        migrations.AlterField(
            model_name='estimating',
            name='bidder_address',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Bidder Address'),
        ),
    ]
