# Generated by Django 4.2.4 on 2023-11-28 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0026_alter_dms_dertory_last_name_gc_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimating',
            name='status',
            field=models.CharField(blank=True, choices=[('Working', 'Working'), ('Pending', 'Pending'), ('Won', 'Won'), ('Lost', 'Lost')], default='Working', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='gc_detail',
            name='estimating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gc_details', to='Estimating.estimating'),
        ),
    ]
