# Generated by Django 4.2.4 on 2023-10-24 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_project_prjct_mngr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('Construction Phase', 'Construction Phase'), ('Pre-Construction', 'Pre-Construction'), ('Close out phase', 'Close out phase'), ('Upcoming/Estimating pahse', 'Upcoming/Estimating pahse'), ('Complete', 'Complete')], default='Pre-Construction', max_length=50, null=True),
        ),
    ]