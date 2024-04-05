# Generated by Django 4.2.4 on 2024-01-08 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0037_alter_gc_detail_gc_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Qualification',
        ),
        migrations.RemoveField(
            model_name='proposalservice',
            name='service',
        ),
        migrations.AddField(
            model_name='proposalservice',
            name='services',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Services'),
        ),
        migrations.AlterField(
            model_name='estimating',
            name='estimator',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('job_title__name', 'Estimator'), ('job_title__name', 'Estimating Manager'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estimations_as_estimator', to='Estimating.dms_dertory', verbose_name='Estimator'),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]