# Generated by Django 4.2.4 on 2023-10-24 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0022_alter_proposal_estimating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dms_dertory',
            name='job_title',
        ),
        migrations.AddField(
            model_name='dms_dertory',
            name='job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Estimating.role', verbose_name='Role'),
        ),
    ]
