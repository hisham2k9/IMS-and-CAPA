# Generated by Django 3.0.3 on 2020-03-12 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0019_auto_20200312_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='imsassignfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assfile', models.FileField(blank=True, null=True, upload_to='assign_files')),
                ('apost', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='imsclosurefiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clofile', models.FileField(blank=True, null=True, upload_to='closure_files')),
                ('cpost', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='imsinvestigationfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invfile', models.FileField(blank=True, null=True, upload_to='investigation_files')),
                ('ipost', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='imssubmissionfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subfile', models.FileField(blank=True, null=True, upload_to='submission_files')),
                ('spost', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='imsvalidationfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valfile', models.FileField(blank=True, null=True, upload_to='validation_files')),
                ('vpost', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ims.imsmodel')),
            ],
        ),
        migrations.RemoveField(
            model_name='closureimages',
            name='cpost',
        ),
        migrations.RemoveField(
            model_name='investigationimages',
            name='ipost',
        ),
        migrations.RemoveField(
            model_name='submissionimages',
            name='spost',
        ),
        migrations.RemoveField(
            model_name='validationimages',
            name='vpost',
        ),
        migrations.DeleteModel(
            name='assignimages',
        ),
        migrations.DeleteModel(
            name='closureimages',
        ),
        migrations.DeleteModel(
            name='investigationimages',
        ),
        migrations.DeleteModel(
            name='submissionimages',
        ),
        migrations.DeleteModel(
            name='validationimages',
        ),
    ]
