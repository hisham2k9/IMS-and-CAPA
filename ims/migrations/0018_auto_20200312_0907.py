# Generated by Django 3.0.3 on 2020-03-12 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0017_auto_20200311_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignimages',
            name='apost',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel'),
        ),
        migrations.AddField(
            model_name='assignimages',
            name='assimage',
            field=models.ImageField(blank=True, null=True, upload_to='assign_images'),
        ),
        migrations.AddField(
            model_name='closureimages',
            name='cloimage',
            field=models.ImageField(blank=True, null=True, upload_to='closure_images'),
        ),
        migrations.AddField(
            model_name='closureimages',
            name='cpost',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel'),
        ),
        migrations.AddField(
            model_name='investigationimages',
            name='invimage',
            field=models.ImageField(blank=True, null=True, upload_to='investigation_images'),
        ),
        migrations.AddField(
            model_name='investigationimages',
            name='ipost',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel'),
        ),
        migrations.AddField(
            model_name='submissionimages',
            name='spost',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel'),
        ),
        migrations.AddField(
            model_name='submissionimages',
            name='subimage',
            field=models.ImageField(blank=True, null=True, upload_to='submission_images'),
        ),
        migrations.AddField(
            model_name='validationimages',
            name='valimage',
            field=models.ImageField(blank=True, null=True, upload_to='validation_images'),
        ),
        migrations.AddField(
            model_name='validationimages',
            name='vpost',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel'),
        ),
    ]
