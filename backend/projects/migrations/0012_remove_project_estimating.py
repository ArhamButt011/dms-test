# Generated by Django 4.2.4 on 2023-10-24 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_rename_scope_project_proposal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='estimating',
        ),
    ]
