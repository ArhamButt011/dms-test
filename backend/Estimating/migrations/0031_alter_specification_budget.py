# Generated by Django 4.2.4 on 2023-12-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0030_alter_spec_detail_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specification',
            name='budget',
            field=models.FloatField(verbose_name='Scope of Work Price'),
        ),
    ]
