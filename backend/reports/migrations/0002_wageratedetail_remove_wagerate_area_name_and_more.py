# Generated by Django 4.2.4 on 2024-02-01 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WageRateDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Area name')),
                ('st_amount', models.FloatField(blank=True, null=True, verbose_name='ST Amount')),
                ('ot_amount', models.FloatField(blank=True, null=True, verbose_name='OT Amount')),
                ('dt_amount', models.FloatField(blank=True, null=True, verbose_name='DT Amount')),
            ],
        ),
        migrations.RemoveField(
            model_name='wagerate',
            name='area_name',
        ),
        migrations.RemoveField(
            model_name='wagerate',
            name='dt_amount',
        ),
        migrations.RemoveField(
            model_name='wagerate',
            name='ot_amount',
        ),
        migrations.RemoveField(
            model_name='wagerate',
            name='st_amount',
        ),
        migrations.AlterField(
            model_name='wagerate',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Add Title'),
        ),
        migrations.DeleteModel(
            name='WageRateTitle',
        ),
        migrations.AddField(
            model_name='wageratedetail',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.wagerate', verbose_name='Add Title'),
        ),
    ]