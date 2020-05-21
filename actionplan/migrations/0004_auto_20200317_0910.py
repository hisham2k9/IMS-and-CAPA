# Generated by Django 3.0.3 on 2020-03-17 03:40

import actionplan.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actionplan', '0003_auto_20200316_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionplanmodel',
            name='task_assign_username',
            field=models.ForeignKey(default='admin', on_delete=models.SET(actionplan.models.get_sentinel_user), related_name='assign_by_user', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='Assign By'),
        ),
    ]
