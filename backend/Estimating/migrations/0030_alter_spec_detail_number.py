# Generated by Django 4.2.4 on 2023-12-04 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0029_proposal_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spec_detail',
            name='number',
            field=models.CharField(max_length=250, verbose_name='Add Number'),
        ),
    ]