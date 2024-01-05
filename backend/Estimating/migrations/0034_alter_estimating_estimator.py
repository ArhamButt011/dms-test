# Generated by Django 4.2.4 on 2024-01-05 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0033_alter_company_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimating',
            name='estimator',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('job_title__name', 'Estimator'), ('job_title_name', 'Estimating Manager'), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estimations_as_estimator', to='Estimating.dms_dertory', verbose_name='Estimator'),
        ),
    ]