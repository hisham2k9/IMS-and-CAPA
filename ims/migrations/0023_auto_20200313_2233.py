# Generated by Django 3.0.3 on 2020-03-13 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0022_auto_20200313_1440'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imsvalidationfiles',
            old_name='valdata',
            new_name='valdate',
        ),
        migrations.AlterField(
            model_name='imssubmissionfiles',
            name='subdate',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
