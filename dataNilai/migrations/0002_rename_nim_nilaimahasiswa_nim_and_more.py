# Generated by Django 5.1 on 2025-01-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataNilai', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nilaimahasiswa',
            old_name='nim',
            new_name='NIM',
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='ANT',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='BED',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='ELK',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='FOR',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='IKA',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='IKM',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='IPD',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='KDK',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='KJW',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='MAT',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='MOI',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='MPK',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='OBG',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='OT2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='RAD',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='SRM',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nilaimahasiswa',
            name='THTKL',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
