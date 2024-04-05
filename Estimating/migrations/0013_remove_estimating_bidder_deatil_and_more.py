# Generated by Django 4.2.4 on 2023-10-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estimating', '0012_estimating_bidder_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimating',
            name='bidder_deatil',
        ),
        migrations.AddField(
            model_name='estimating',
            name='bidder_address',
            field=models.CharField(max_length=5000, null=True, verbose_name='Bidder Address'),
        ),
        migrations.AddField(
            model_name='estimating',
            name='bidder_phone',
            field=models.IntegerField(blank=True, null=True, verbose_name='Bidder Phone Number'),
        ),
        migrations.AlterField(
            model_name='estimating',
            name='bidder_mail',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='add the bidder Mail'),
        ),
    ]