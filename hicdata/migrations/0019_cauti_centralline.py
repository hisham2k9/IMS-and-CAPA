# Generated by Django 3.0.3 on 2020-03-01 04:55

from django.db import migrations
import hicdata.models


class Migration(migrations.Migration):

    dependencies = [
        ('hicdata', '0018_remove_cauti_centralline'),
    ]

    operations = [
        migrations.AddField(
            model_name='cauti',
            name='centralline',
            field=hicdata.models.DeviceDetailsField(blank=True, null=True),
        ),
    ]
