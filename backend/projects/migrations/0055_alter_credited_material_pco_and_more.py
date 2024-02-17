# Generated by Django 4.2.4 on 2024-02-04 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0054_labor_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credited_material',
            name='pco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credited_materials', to='projects.pco', verbose_name='PCO'),
        ),
        migrations.AlterField(
            model_name='debited_material',
            name='pco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='debited_materials', to='projects.pco', verbose_name='PCO'),
        ),
        migrations.AlterField(
            model_name='labor',
            name='pco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='labor', to='projects.pco', verbose_name='PCO'),
        ),
        migrations.AlterField(
            model_name='miscellaneous',
            name='pco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='miscellaneous', to='projects.pco', verbose_name='PCO'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='pco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='projects.pco', verbose_name='PCO'),
        ),
    ]