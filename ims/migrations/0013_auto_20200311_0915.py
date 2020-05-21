# Generated by Django 3.0.3 on 2020-03-11 03:45

from django.conf import settings
from django.db import migrations, models
import ims.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ims', '0012_auto_20200311_0905'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='transferimages',
            new_name='assignimages',
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='assign_qa_comments_user',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='assign_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imsmodel',
            name='qa_assign_to',
            field=models.ForeignKey(default=1, on_delete=models.SET(ims.models.get_sentinel_user), related_name='assign_to_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
