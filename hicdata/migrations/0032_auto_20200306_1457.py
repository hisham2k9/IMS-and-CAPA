# Generated by Django 3.0.3 on 2020-03-06 09:27

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hicdata', '0031_auto_20200306_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cauti',
            name='comorbidities',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('DM', 'DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'), ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'), ('Immunosuppressed', 'Immunosuppressed'), ('Sepsis', 'Sepsis'), ('Malnourished', 'Malnourished'), ('Surgical Intervention', 'Surgical Invervention')], max_length=300, null=True),
        ),
    ]
