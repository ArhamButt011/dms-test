# Generated by Django 4.2.4 on 2024-03-07 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BIM', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bim',
            name='bimRequirement',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
