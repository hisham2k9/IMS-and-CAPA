# Generated by Django 3.0.3 on 2020-02-29 10:53

from django.db import migrations
import hicdata.models


class Migration(migrations.Migration):

    dependencies = [
        ('hicdata', '0006_remove_cauti_central_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='cauti',
            name='centralline',
            field=hicdata.models.DeviceDetailsField(blank=True, null=True),
        ),
    ]
