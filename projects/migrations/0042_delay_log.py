# Generated by Django 4.2.4 on 2024-01-11 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_project_attn_email_project_attn_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delay_Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='date')),
                ('typ', models.CharField(blank=True, choices=[('Related PCO', 'Related PCO'), ('Related RFI', 'Related RFI'), ('Other Traders', 'Other Traders')], default='Other Traders', max_length=50, null=True, verbose_name='Select status')),
                ('dely_log_num', models.CharField(blank=True, max_length=50, null=True, verbose_name='Delay Number')),
                ('status', models.CharField(blank=True, choices=[('Open', 'Open'), ('Close', 'Close')], default='Close', max_length=50, null=True, verbose_name='Select status')),
                ('dly_rslov', models.DateField(blank=True, null=True, verbose_name='Delay Resolve date')),
                ('fnl_impct', models.IntegerField(blank=True, null=True, verbose_name='Final Impact (Working Days)')),
                ('totl_impct', models.IntegerField(blank=True, null=True, verbose_name='Total Project Impact(Working Days)')),
                ('dly_ntc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.delay_notice', verbose_name='Select Delay Notice')),
            ],
        ),
    ]
