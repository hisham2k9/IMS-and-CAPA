# Generated by Django 3.0.3 on 2020-03-11 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0008_auto_20200309_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imsmodel',
            old_name='transfer_comments_qa',
            new_name='assign_comments_qa',
        ),
    ]
