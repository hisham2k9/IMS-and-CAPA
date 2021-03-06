# Generated by Django 3.0.3 on 2020-03-09 11:05

from django.conf import settings
from django.db import migrations, models
import ims.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ims', '0004_auto_20200309_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imsmodel',
            name='closure_confirm_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='closure_person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='investigation_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='investigator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='qa_transfer_to',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='transfer_to_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='submission_confirm_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='transfer_qa_comments_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='transfer_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='validation_confirm_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='validator', to=settings.AUTH_USER_MODEL),
        ),
    ]
