# Generated by Django 3.0.3 on 2020-02-25 15:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import nursequalitydata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracheostomy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('pt_name', models.CharField(max_length=100)),
                ('pt_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('pt_age', models.IntegerField()),
                ('pt_diagnosis', models.CharField(max_length=200)),
                ('dateofadmission', models.DateField(default=datetime.date.today)),
                ('datetime_tracheostomy', models.DateTimeField(default=django.utils.timezone.now)),
                ('comments', models.TextField(blank=True, null=True)),
                ('report_by', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('loc_tracheostory', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tracheostomy_loc', to='accounts.Locations', to_field='loc_name')),
                ('pt_department', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Departments', to_field='dept_name')),
                ('pt_doctor', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Doctors', to_field='doc_name')),
                ('pt_location', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Locations', to_field='loc_name')),
                ('username', models.ForeignKey(null=True, on_delete=models.SET(nursequalitydata.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnToICU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('pt_name', models.CharField(max_length=100)),
                ('pt_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('pt_age', models.IntegerField()),
                ('pt_diagnosis', models.CharField(max_length=200)),
                ('dateofadmission', models.DateField(default=datetime.date.today)),
                ('datetime_transfer_out', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetime_return', models.DateTimeField(default=django.utils.timezone.now)),
                ('reason_return', models.TextField()),
                ('report_by', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('pt_department', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Departments', to_field='dept_name')),
                ('pt_doctor', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Doctors', to_field='doc_name')),
                ('pt_location', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Locations', to_field='loc_name')),
                ('transfer_to', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='TransferWard', to='accounts.Locations', to_field='loc_name')),
                ('username', models.ForeignKey(null=True, on_delete=models.SET(nursequalitydata.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RestraintInjury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('pt_name', models.CharField(max_length=100)),
                ('pt_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('pt_age', models.IntegerField()),
                ('pt_diagnosis', models.CharField(max_length=200)),
                ('dateofadmission', models.DateField(default=datetime.date.today)),
                ('indicationof_restraint', models.CharField(max_length=200)),
                ('datetime_restraintstart', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetime_restraintremoval', models.DateTimeField(default=django.utils.timezone.now)),
                ('obtain_consent', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50)),
                ('maintain_observation', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50)),
                ('injury', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50)),
                ('injury_details', models.TextField(blank=True, null=True)),
                ('report_by', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('pt_department', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Departments', to_field='dept_name')),
                ('pt_doctor', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Doctors', to_field='doc_name')),
                ('pt_location', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Locations', to_field='loc_name')),
                ('username', models.ForeignKey(null=True, on_delete=models.SET(nursequalitydata.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reintubation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('pt_name', models.CharField(max_length=100)),
                ('pt_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('pt_age', models.IntegerField()),
                ('pt_diagnosis', models.CharField(max_length=200)),
                ('dateofadmission', models.DateField(default=datetime.date.today)),
                ('datetime_intubation', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetime_extubation', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetime_reintubation', models.DateTimeField(default=django.utils.timezone.now)),
                ('reason_reintubation', models.TextField()),
                ('report_by', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('loc_intubation', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='IntubationLocation1', to='accounts.Locations', to_field='loc_name')),
                ('pt_department', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Departments', to_field='dept_name')),
                ('pt_doctor', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Doctors', to_field='doc_name')),
                ('pt_location', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Locations', to_field='loc_name')),
                ('username', models.ForeignKey(null=True, on_delete=models.SET(nursequalitydata.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PressureInjury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('pt_name', models.CharField(max_length=100)),
                ('pt_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('pt_age', models.IntegerField()),
                ('pt_diagnosis', models.CharField(max_length=200)),
                ('dateofadmission', models.DateField(default=datetime.date.today)),
                ('dateofobservation', models.DateField(default=datetime.date.today)),
                ('loc_ulcer', models.CharField(max_length=200)),
                ('grade', models.IntegerField()),
                ('hapu_dapu_out', models.CharField(max_length=50)),
                ('outcome', models.TextField()),
                ('remarks', models.TextField()),
                ('report_by', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('pt_department', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Departments', to_field='dept_name')),
                ('pt_doctor', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Doctors', to_field='doc_name')),
                ('pt_location', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Locations', to_field='loc_name')),
                ('username', models.ForeignKey(null=True, on_delete=models.SET(nursequalitydata.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Intubation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('pt_name', models.CharField(max_length=100)),
                ('pt_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50)),
                ('pt_age', models.IntegerField()),
                ('pt_diagnosis', models.CharField(max_length=200)),
                ('dateofadmission', models.DateField(default=datetime.date.today)),
                ('datetime_intubation', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetime_extubation', models.DateTimeField(default=django.utils.timezone.now)),
                ('comments', models.TextField()),
                ('transferchoice', models.CharField(blank=True, choices=[('Transfer-Out', 'Transfer-Out'), ('Death', 'Death')], default='Not Given', max_length=50, null=True)),
                ('report_by', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('loc_intubation', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='IntubationLocation', to='accounts.Locations', to_field='loc_name')),
                ('pt_department', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Departments', to_field='dept_name')),
                ('pt_doctor', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Doctors', to_field='doc_name')),
                ('pt_location', models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.Locations', to_field='loc_name')),
                ('username', models.ForeignKey(null=True, on_delete=models.SET(nursequalitydata.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
