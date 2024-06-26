# Generated by Django 4.2.4 on 2024-01-29 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0051_delay_notice_pco_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfi_log',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project', verbose_name='Select'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='detail',
            field=models.CharField(max_length=5000, verbose_name='Add Qualification'),
        ),
    ]
