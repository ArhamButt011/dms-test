# Generated by Django 4.2.4 on 2024-03-06 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0074_alter_delay_log_typ'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='badging',
            field=models.BooleanField(default=False),
        ),
    ]