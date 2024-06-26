# Generated by Django 4.2.4 on 2023-10-05 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0009_rename_prjct_name_estimating_prjct_name'),
        ('accounts', '0002_user_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dprtmnt_name', models.CharField(max_length=250, verbose_name='Add the department name ')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='direct_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Direct'),
        ),
        migrations.AddField(
            model_name='user',
            name='locaton',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='Estimating.company', verbose_name='company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_Name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.department', verbose_name='Department '),
        ),
    ]
