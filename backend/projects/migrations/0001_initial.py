# Generated by Django 4.2.4 on 2023-09-01 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cmpny_Name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prjct_Name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.company')),
            ],
        ),
        migrations.CreateModel(
            name='Project_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drctry_Name', models.CharField(max_length=255, verbose_name='Folder Name')),
                ('prnt_ID', models.PositiveIntegerField(blank=True, null=True, verbose_name='Folder Parent ID')),
                ('file_Name', models.CharField(blank=True, max_length=100, null=True, verbose_name='File Name')),
                ('output_Table_Name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Table Name')),
                ('prjct_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
