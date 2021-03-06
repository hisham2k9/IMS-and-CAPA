# Generated by Django 3.0.3 on 2020-03-06 10:33

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hicdata', '0033_auto_20200306_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vap',
            old_name='dateofincident',
            new_name='dateofrecognition',
        ),
        migrations.AlterField(
            model_name='clabsi',
            name='comorbidities',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('DM', 'DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'), ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'), ('Immunosuppressed', 'Immunosuppressed'), ('Sepsis', 'Sepsis'), ('Malnourished', 'Malnourished'), ('Surgical Intervention', 'Surgical Invervention')], max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='clabsi',
            name='criteria',
            field=models.TextField(blank=True, choices=[('Appropriate indication for central line insertion', 'Appropriate indication for central line insertion'), ('Followed sterile technique', 'Followed sterile technique'), ('Hand Hygiene before and after handling', 'Hand Hygiene before and after handling'), ('PPE, Sterile gloves, steril gown, Mask used during insertion', 'PPE, Sterile gloves, steril gown, Mask used during insertion'), ('Proper site cleaning (with 70% Isopropyl alcohol or 2% Cholorohexidine', 'Proper site cleaning (with 70% Isopropyl alcohol or 2% Cholorohexidine'), ('Anticeptic Dressing used', 'Anticeptic Dressing used'), ('Hub cleaning after use', 'Hub cleaning after use'), ('unused injection port kept closed?', 'unused injection port kept closed?'), ('Aseptic technique followed before each use?', 'Aseptic technique followed before each use?'), ('Review of insertion site done daily', 'Review of insertion done daily'), ('Staffing level', 'Staffing level'), ('Antibiotic prescribed as per culture report', 'Antibiotic prescribed as per culture report'), ('Antibiotic prescribed as per antibiotic policy', 'Antibiotic prescribed as per antibiotic policy')], max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='clabsi',
            name='signssymptoms',
            field=models.CharField(blank=True, choices=[('Fever', 'Fever'), ('Leukocytosis', 'Leukocytosis'), ('Abcess', 'Abcess'), ('Apnoea', 'Apnoea'), ('Bradycardia', 'Bradycardia'), ('Pain', 'Pain'), ('Tenderness', 'Tenderness'), ('Purulent drainage', 'Purulant drainage'), ('Hypotherma', 'Hypothermia'), ('Vomiting', 'Vomiting'), ('Lethargy', 'Lethargy')], max_length=300, null=True),
        ),
    ]
