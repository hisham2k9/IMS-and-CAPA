# Generated by Django 3.0.3 on 2020-03-06 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hicdata', '0026_auto_20200303_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='antibiotic',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='bodyfluidexposure',
            old_name='staff_sex',
            new_name='staff_gender',
        ),
        migrations.RenameField(
            model_name='cauti',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='clabsi',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='nsi',
            old_name='staff_sex',
            new_name='staff_gender',
        ),
        migrations.RenameField(
            model_name='ssi',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='thrombophlebitis',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='vae',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='vap',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
    ]
