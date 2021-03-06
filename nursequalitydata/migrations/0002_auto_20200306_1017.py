# Generated by Django 3.0.3 on 2020-03-06 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nursequalitydata', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intubation',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='pressureinjury',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='reintubation',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='restraintinjury',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='returntoicu',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
        migrations.RenameField(
            model_name='tracheostomy',
            old_name='pt_sex',
            new_name='pt_gender',
        ),
    ]
