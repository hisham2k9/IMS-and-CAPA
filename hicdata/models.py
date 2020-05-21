from django.db import models
from django.forms import ModelForm
from django import forms
from accounts.models import Departments
from accounts.models import Doctors
from accounts.models import Locations
from django.core.exceptions import FieldError
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime  #admindate
from multiselectfield import MultiSelectField
#import SelectMultipleField
#from .hicforms import CAUTIFORM
# Create your models here.

##################### MODEL ONE ##########################################################
###CAUTI form and model form   ###################################################
#######################################################################################

import pickle

from django.http import HttpResponse
from django import forms
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt


class DeviceWidget(forms.widgets.MultiWidget):
    CHOICES=[('No', 'No'),('Yes','Yes')]
    def __init__(self, attrs=None):
        widgets = [forms.Select(choices= DeviceWidget.CHOICES),
                   AdminDateWidget(attrs={'placeholder': 'Date of Insertion'}),
                   AdminDateWidget(attrs={'placeholder': 'Date of Removal'}),
                   forms.TextInput(attrs={'placeholder': 'inserted By'})]
        super(DeviceWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        #print('value', value)
        if value:
            value=value.replace('(','')
            value=value.replace(')','')
            value=list(value.split(','))
            return value
        else:
            print(value)
            return []   #if nothing, return an empty list

    
class DeviceField(forms.fields.MultiValueField):
    widget = DeviceWidget

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=50,required=False),
                       forms.fields.DateField(required=False),
                       forms.fields.DateField(required=False),
                       forms.fields.CharField(max_length=50,required=False)]
        super(DeviceField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        if values:
            values=tuple(values)                                       
            return values
        else:
            values=[None,None,None,None]
            values=tuple(values)
            return values
            

################################################################################
class TrackerWidget(forms.widgets.MultiWidget):
    CHOICES=[('No', 'No'),('Yes','Yes')]
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={'placeholder':'Ward Name'}),
                   AdminDateWidget(attrs={'placeholder': 'From Date'}),
                   AdminDateWidget(attrs={'placeholder': 'To Date'}),
                   forms.NumberInput(attrs={'placeholder': 'Number of days',})]
        super(TrackerWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        #print('value', value)
        if value:
            value=value.replace('(','')
            value=value.replace(')','')
            value=list(value.split(','))
            return value
        else:
            return []

    
class TrackerField(forms.fields.MultiValueField):
    widget = TrackerWidget

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=50,required=False),
                       forms.fields.DateField(required=False),
                       forms.fields.DateField(required=False),
                       forms.fields.IntegerField(required=False)]
        super(TrackerField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        ## compress list to single object                                               
        ## eg. date() >> u'31/12/2012'
        if values:
            values=tuple(values) 
            #print(values)                                      
            return values
        else:
            values=[None,None,None,None]
            values=tuple(values)
            return values







##special field as created in postgres
class DeviceDetailsField(models.Field):
    def db_type(self, connection):
        return 'devicedetails'
##special field as created in postgres
class DeviceDetailField(models.Field):
    def db_type(self, connection):
        return 'devicedetails'

##special field as created in postgres
class PatientTrackerField(models.Field):
    def db_type(self, connection):
        return 'patienttracker'

##sentinal user code
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class CAUTI(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    YNCHOICES=[('No', 'No'),('Yes','Yes')]
    
    PositiveChoice=[('Negative','Negative'), ('Positive','Positive'), ('Not Sent', 'Not Sent')]

    
    ComorbiditiesChoices=[('DM','DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'),
                          ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'),
                          ('Immunosuppressed','Immunosuppressed'),('Sepsis', 'Sepsis'),('Malnourished', 'Malnourished'),
                          ('Surgical Intervention', 'Surgical Invervention')]
    CriteriaChoices=[('Appropriate Foley Catheterization', 'Appropriate Foley Catheterization'),
                     ('Followed sterile technique','Followed sterile technique'),
                     ('Urobag not touching floor','Urobag not touching floor'),
                     ('urine flow not obstructed','urine flow not obstructed'),
                     ('Meatal Care given','Meatal Care given'),('Catheter Fixed to thigh','Catheter Fixed to thigh'),
                     ('Hand Hygiene before and after catheter handling','Hand Hygiene before and after catheter handling'),
                     ('Reviewed need of catheter removal', 'Reviewed need of catheter removal'),
                     ('Breaks in closed system','Breaks in closed system'),('Staffing level','Staffing level'),
                     ('Urine sent for routine examination','Urine sent for routine examination')
                     ]
    
    SignssymptomsChoices=[('Fever','Fever'),('Urgency','Urgency'),('Frequency','Frequency'),('Dysuria','Dysuria'),
                          ('Suprapubic tenderness', 'Suprapubic tenderness'),('Abcess','Abcess'),('Apnoea','Apnoea'),
                          ('Bradycardia','Bradycardia'),('Costovertebral ankle pain', 'Costobertebral ankle pain'),
                          ('Purulent drainage','Purulant drainage'),('Hypotherma','Hypothermia'),('Vomiting','Vomiting'),
                          ('Lethargy','Lethargy')]
    
    UrinecultureChoices=[('')]
    
    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofincident=models.DateField(default=datetime.date.today)
    
    ## device details
    dateofadmission=models.DateField(default=datetime.date.today)
    dateofdischarge=models.DateField(null=True, blank = True)
    centralline=DeviceDetailsField(null=True, blank=True)
    urinarycatheter=DeviceDetailsField(null=True, blank=True)
    ventilated=DeviceDetailsField(null=True, blank=True)
    tracheostomy=DeviceDetailsField(null=True, blank=True)
    perpheralline=DeviceDetailsField(null=True, blank=True)
    
    comorbidities=MultiSelectField(max_length=300, choices= ComorbiditiesChoices, null=True, blank=True)  ##give choices in forms
    
    criteria=MultiSelectField(max_length=500,choices=CriteriaChoices, null = True, blank=True)  ##give choices in forms
    
    signssymptoms=MultiSelectField(max_length=300, choices= SignssymptomsChoices,null=True, blank=True)  ##give choices in forms
    
    
    ##Urine culture report content
    urineculture=models.CharField(max_length=10,null=True, blank=True)
    urineculture_verify=models.DateField(null=True, blank=True)
    urineculture_pus=models.IntegerField(null=True, blank=True)
    urineculture_organism=models.CharField(max_length=100, null=True, blank=True)
    urineculture_sensitivity=models.CharField(max_length=200, null=True, blank=True)
    urineculture_antibiotic=models.CharField(max_length=100, null=True, blank=True)
    
    
    ##blood culture report
    bloodinfection_report=models.CharField(max_length=50, null= True, blank=True)
    bloodinfection_organism=models.CharField(max_length=50, null= True, blank=True)
    bloodinfection_sentivity=models.CharField(max_length=200, null=True, blank = True)
    
    root_cause=models.TextField(null=True, blank=True)
    
    report_by=models.CharField(max_length=100)
    #patient tracking table
    patienttrack=PatientTrackerField(null=True, blank=True)
    patienttrack1=PatientTrackerField(null=True, blank=True)
    patienttrack2=PatientTrackerField(null=True, blank=True)
    patienttrack3=PatientTrackerField(null=True, blank=True)
    patienttrack4=PatientTrackerField(null=True, blank=True)
    patienttrack5=PatientTrackerField(null=True, blank=True)
    
    
    
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=6)
    
    def __str__(self):
        return "{}{}".format(self.pt_id, self.pt_name)
    
    
class CAUTIForm(ModelForm):
    
    PositiveChoice=[('Negative','Negative'), ('Positive','Positive'), ('Not Sent', 'Not Sent')]

    
    ComorbiditiesChoices=[('DM','DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'),
                          ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'),
                          ('Immunosuppressed','Immunosuppressed'),('Sepsis', 'Sepsis'),('Malnourished', 'Malnourished'),
                          ('Surgical Intervention', 'Surgical Invervention')]
    CriteriaChoices=[('Appropriate Foley Catheterization', 'Appropriate Foley Catheterization'),
                     ('Followed sterile technique','Followed sterile technique'),
                     ('Urobag not touching floor','Urobag not touching floor'),
                     ('urine flow not obstructed','urine flow not obstructed'),
                     ('Meatal Care given','Meatal Care given'),('Catheter Fixed to thigh','Catheter Fixed to thigh'),
                     ('Hand Hygiene before and after catheter handling','Hand Hygiene before and after catheter handling'),
                     ('Reviewed need of catheter removal', 'Reviewed need of catheter removal'),
                     ('Breaks in closed system','Breaks in closed system'),('Staffing level','Staffing level'),
                     ('Urine sent for routine examination','Urine sent for routine examination')
                     ]
    
    SignssymptomsChoices=[('Fever','Fever'),('Urgency','Urgency'),('Frequency','Frequency'),('Dysuria','Dysuria'),
                          ('Suprapubic tenderness', 'Suprapubic tenderness'),('Abcess','Abcess'),('Apnoea','Apnoea'),
                          ('Bradycardia','Bradycardia'),('Costovertebral ankle pain', 'Costobertebral ankle pain'),
                          ('Purulent drainage','Purulant drainage'),('Hypotherma','Hypothermia'),('Vomiting','Vomiting'),
                          ('Lethargy','Lethargy')]
    
    UrinecultureChoices=[('')]
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
    
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department')
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor')
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location')
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(),label='Date of Admission: ')
    dateofdischarge=forms.DateField(required=False,widget=AdminDateWidget(),label='Date of Discharge: ')
    centralline=DeviceField(required=False, label= 'Central Line Device? ')
    urinarycatheter=DeviceField(required=False, label='Urinary Catheter? ')
    ventilated=DeviceField(required=False, label='Intubation/Venti?      ')
    tracheostomy=DeviceField(required=False, label='Tracheostomy?        ')
    perpheralline=DeviceField(required=False, label='Peripheral Line?    ')
    comorbidities=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ComorbiditiesChoices, required=False, 
                                            label='Comorbidities: (Check applicable)')
    criteria=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CriteriaChoices, required=False,
                                       label='Criteria: (Check applicable)')
    signssymptoms=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SignssymptomsChoices, required=False,
                                            label='Signs and Symptoms (Check Applicable)')
    
    urineculture=forms.CharField(widget=forms.Select(choices=PositiveChoice,attrs={'class':'form-control'}),required=False,
                                 label='Urine sent for culture?')
    urineculture_verify=forms.DateField(widget= AdminDateWidget(),required=False,label="Verified date:")
    urineculture_pus=forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control'}),required=False,
                                        label="Number of pus cells:")
    urineculture_organism=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                          label='Organism isolated')
    urineculture_sensitivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Sensitivity pattern:')
    urineculture_antibiotic=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Antibiotic started:')
    
    
    bloodinfection_report=forms.CharField(widget=forms.Select(choices=PositiveChoice,attrs={'class':'form-control'}),
                                          required=False,label='Blood culture Report:')
    bloodinfection_organism=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Blood culture organism:')
    bloodinfection_sentivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Sensitivity pattern:')
    
    root_cause=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required=False, label= 'Root Cause Analysis')
    
    patienttrack=TrackerField(required=False, label= "Patient Tracker Location 1")
    patienttrack1=TrackerField(required=False,label= "Patient Tracker Location 2")
    patienttrack2=TrackerField(required=False,label= "Patient Tracker Location 3")
    patienttrack3=TrackerField(required=False, label= "Patient Tracker Location 4")
    patienttrack4=TrackerField(required=False, label= "Patient Tracker Location 5")
    patienttrack5=TrackerField(required=False, label= "Patient Tracker Location 6")
    
    class Meta:
        model=CAUTI

        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofincident':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }
        exclude=['username','timestamp']


        
        labels={'pt_id': 'Patient UHID','pt_name':'Patient Name','pt_location':'Patient Location',
                'pt_gender': 'Patient Gender', 'pt_department': 'Department', 'dateofincident': 'Date of Incident', 
                'Inserted?':'Inserted?'}
    
##################################################################################################################
##################################################################################################################

################ MODEL TWO ###################################################
###Antibiotic resistance Model and Form#######################################

class Antibiotic(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadministration=models.DateField(default=datetime.date.today)
    
    ###
    dateofadmission=models.DateField(default=datetime.date.today)
    dateofdischarge=models.DateField(null=True, blank=True)
    pt_diagnosis=models.CharField(max_length=200, null=True, blank = True)
    emperical_prescription=models.CharField(max_length=20,null=True, blank = True)
    antibiotic_name=models.CharField(max_length=60,null=True, blank = True)
    antibiotic_policy=models.CharField(max_length=30,null=True, blank = True)   #was according to antibiotic policy?
    cultures_taken=models.CharField(max_length=30,null=True, blank = True)     ##was cultures taken for indication b4 prescription?
    cultures_desc=models.TextField(null=True, blank = True)   ##if yes give desc.
    changes_made=models.TextField(null=True, blank=True)
    escalation_antibiotic=models.CharField(max_length=100,null=True, blank = True) 
    deescalation_antibiotic=models.CharField(max_length=100,null=True, blank=True)
    pt_type=models.CharField(max_length=20,null=True, blank = True)
    central_line=models.CharField(max_length=100,null=True, blank=True)
    remarks=models.TextField(null=True, blank=True)
    
    
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class AntibioticForm(ModelForm):
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')

        
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    
    
    ##
    dateofadmission=forms.DateField(widget=AdminDateWidget(),label='Date of Admission: ')
    dateofdischarge=forms.DateField(required=False,widget=AdminDateWidget(),label='Date of Discharge: ')
    
    pt_diagnosis=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Clinical Diagnosis'})
                                  ,label='Clinical Diagnosis of the patient')
    emperical_prescription=forms.CharField(widget=forms.Select(choices= CAUTI.YNCHOICES, attrs={'class':'form-control'})
                                  ,label='Was the Antibiotic prescribed emperically?',required=False)
    antibiotic_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Antibiotic given?'})
                                  ,label='Name of Antibiotic Given: ',required=False)
    antibiotic_policy=forms.CharField(widget=forms.Select(choices= CAUTI.YNCHOICES, attrs={'class':'form-control'})
                                  ,label='Was the Antibiotic choice as per Antibiotic Policy? ',required=False)
    cultures_taken=forms.CharField(required=False,widget=forms.Select(choices= CAUTI.YNCHOICES, attrs={'class':'form-control'})
                                  ,label='Were Indicated cultures taken before the antibiotic administration? (if yes give details in next field)')
    cultures_desc=forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Specifiy reason if yes in previous Field'})
                                   ,label='Cultures Taken Description: ')   ##if yes give desc.
    changes_made=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Changes made on culture report?'}),
                                                       label='Were any changes made in the antibiotic administration based on culture report?')
    escalation_antibiotic=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Escalation of Antibiotics'})
                                  ,label='Escalation of Antibiotics: ')
    deescalation_antibiotic=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'De-escalation of Antibiotics'})
                                  ,label='De-escalation of Antibiotics: ')
    pt_type=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Patient Type'})
                                  ,label='Patient Type: ')
    central_line=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Central Line'})
                                  ,label='Central Line: ')
    remarks=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Remarks'}),
                                                       label='Remarks')
    
    
    class Meta:
        model=Antibiotic
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofadministration':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp', 'username']

        
        labels={'pt_id': 'Patient UHID','pt_name':'Patient Name','pt_location':'Patient Location',
                'pt_gender': 'Patient Gender', 'pt_department': 'Department', 'dateofadministration': 'Date of Administration of Antibiotic: '}
        

####################################################################################################

####################   MODEL THREEE ################################################################
####################CLABSI Model and form###########################################################
####################################################################################################
class CLABSI(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    PositiveChoice=[('Negative','Negative'), ('Positive','Positive'), ('Not Sent', 'Not Sent')]

    
    ComorbiditiesChoices=[('DM','DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'),
                          ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'),
                          ('Immunosuppressed','Immunosuppressed'),('Sepsis', 'Sepsis'),('Malnourished', 'Malnourished'),
                          ('Surgical Intervention', 'Surgical Invervention')]
    CriteriaChoices=[('Appropriate indication for central line insertion', 'Appropriate indication for central line insertion'),
                     ('Followed sterile technique','Followed sterile technique'),
                     ('Hand Hygiene before and after handling','Hand Hygiene before and after handling'),
                     ('PPE, Sterile gloves, steril gown, Mask used during insertion','PPE, Sterile gloves, steril gown, Mask used during insertion'),
                     ('Proper site cleaning (with 70% Isopropyl alcohol or 2% Cholorohexidine','Proper site cleaning (with 70% Isopropyl alcohol or 2% Cholorohexidine'),
                     ('Anticeptic Dressing used','Anticeptic Dressing used'),
                     ('Hub cleaning after use','Hub cleaning after use'),('unused injection port kept closed?','unused injection port kept closed?'),
                     ('Aseptic technique followed before each use?','Aseptic technique followed before each use?'),
                     ('Review of insertion site done daily', 'Review of insertion done daily'),
                     ('Staffing level','Staffing level'),
                     ('Antibiotic prescribed as per culture report','Antibiotic prescribed as per culture report'),
                     ('Antibiotic prescribed as per antibiotic policy', 'Antibiotic prescribed as per antibiotic policy')
                     ]
    
    SignssymptomsChoices=[('Fever','Fever'),('Leukocytosis','Leukocytosis'),('Abcess','Abcess'),('Apnoea','Apnoea'),
                          ('Bradycardia','Bradycardia'),('Pain', 'Pain'),('Tenderness', 'Tenderness'),
                          ('Purulent drainage','Purulant drainage'),('Hypotherma','Hypothermia'),('Vomiting','Vomiting'),
                          ('Lethargy','Lethargy')]
    
    UrinecultureChoices=[('')]


    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofrecognition=models.DateField(default=datetime.date.today)
    
    
    ##
    ## device details
    dateofadmission=models.DateField(default=datetime.date.today)
    dateofdischarge=models.DateField(null=True, blank = True)
    centralline=DeviceDetailsField(null=True, blank=True)
    urinarycatheter=DeviceDetailsField(null=True, blank=True)
    ventilated=DeviceDetailsField(null=True, blank=True)
    tracheostomy=DeviceDetailsField(null=True, blank=True)
    perpheralline=DeviceDetailsField(null=True, blank=True)
    
    comorbidities=MultiSelectField(max_length=300, choices=ComorbiditiesChoices, null=True, blank=True)  ##give choices in forms
    
    criteria=MultiSelectField(max_length=500, choices=CriteriaChoices,null = True, blank=True)  ##give choices in forms
    
    signssymptoms=MultiSelectField(max_length=300, choices=SignssymptomsChoices, null=True, blank=True)  ##give choices in forms
    
    
    ##culture report content
    culture=models.CharField(max_length=10,null=True, blank=True, choices=PositiveChoice)
    culture_verify=models.DateField(null=True, blank=True)
    culture_pus=models.IntegerField(null=True, blank=True)
    culture_sensitivity=models.CharField(max_length=200, null=True, blank=True)
    culture_antibiotic=models.CharField(max_length=100, null=True, blank=True)
    
    
    ##secondary infection
    secondary_report=models.CharField(max_length=50, null= True, blank=True)
    secondary_organism=models.CharField(max_length=50, null= True, blank=True)
    secondary_sentivity=models.CharField(max_length=200, null=True, blank = True)
    
    root_cause=models.TextField(null=True, blank=True)
    
    report_by=models.CharField(max_length=100)
    #patient tracking table
    patienttrack=PatientTrackerField(null=True, blank=True)
    patienttrack1=PatientTrackerField(null=True, blank=True)
    patienttrack2=PatientTrackerField(null=True, blank=True)
    patienttrack3=PatientTrackerField(null=True, blank=True)
    patienttrack4=PatientTrackerField(null=True, blank=True)
    patienttrack5=PatientTrackerField(null=True, blank=True)
    
    
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class CLABSIForm(ModelForm):
    
    PositiveChoice=[('Negative','Negative'), ('Positive','Positive'), ('Not Sent', 'Not Sent')]

    
    ComorbiditiesChoices=[('DM','DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'),
                          ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'),
                          ('Immunosuppressed','Immunosuppressed'),('Sepsis', 'Sepsis'),('Malnourished', 'Malnourished'),
                          ('Surgical Intervention', 'Surgical Invervention')]
    CriteriaChoices=[('Appropriate indication for central line insertion', 'Appropriate indication for central line insertion'),
                     ('Followed sterile technique','Followed sterile technique'),
                     ('Hand Hygiene before and after handling','Hand Hygiene before and after handling'),
                     ('PPE, Sterile gloves, steril gown, Mask used during insertion','PPE, Sterile gloves, steril gown, Mask used during insertion'),
                     ('Proper site cleaning (with 70% Isopropyl alcohol or 2% Cholorohexidine','Proper site cleaning (with 70% Isopropyl alcohol or 2% Cholorohexidine'),
                     ('Anticeptic Dressing used','Anticeptic Dressing used'),
                     ('Hub cleaning after use','Hub cleaning after use'),('unused injection port kept closed?','unused injection port kept closed?'),
                     ('Aseptic technique followed before each use?','Aseptic technique followed before each use?'),
                     ('Review of insertion site done daily', 'Review of insertion done daily'),
                     ('Staffing level','Staffing level'),
                     ('Antibiotic prescribed as per culture report','Antibiotic prescribed as per culture report'),
                     ('Antibiotic prescribed as per antibiotic policy', 'Antibiotic prescribed as per antibiotic policy')
                     ]
    
    SignssymptomsChoices=[('Fever','Fever'),('Leukocytosis','Leukocytosis'),('Abcess','Abcess'),('Apnoea','Apnoea'),
                          ('Bradycardia','Bradycardia'),('Pain', 'Pain'),('Tenderness', 'Tenderness'),
                          ('Purulent drainage','Purulant drainage'),('Hypotherma','Hypothermia'),('Vomiting','Vomiting'),
                          ('Lethargy','Lethargy')]
    
    UrinecultureChoices=[('')]
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')

        
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(),label='Date of Admission: ')
    dateofdischarge=forms.DateField(required= False, widget=AdminDateWidget(),label='Date of Discharge: ')
    
    centralline=DeviceField(required=False, label= 'Central Line Device? ')
    urinarycatheter=DeviceField(required=False, label='Urinary Catheter? ')
    ventilated=DeviceField(required=False, label='Intubation/Venti?      ')
    tracheostomy=DeviceField(required=False, label='Tracheostomy?        ')
    perpheralline=DeviceField(required=False, label='Peripheral Line?    ')
    comorbidities=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ComorbiditiesChoices, required=False, 
                                            label='Comorbidities: (Check applicable)')
    criteria=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CriteriaChoices, required=False,
                                       label='Criteria: (Check applicable)')
    signssymptoms=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SignssymptomsChoices, required=False,
                                            label='Signs and Symptoms (Check Applicable)')
    
    culture=forms.CharField(widget=forms.Select(choices=PositiveChoice,attrs={'class':'form-control'}),required=False,
                                 label='Was the culture sent?')
    culture_verify=forms.DateField(widget= AdminDateWidget(),required=False,label="Culture Verified date:")
    culture_pus=forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control'}),required=False,
                                        label="Culture: Number of pus cells:")
    culture_sensitivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Culture: Sensitivity pattern:')
    culture_antibiotic=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Culture: Antibiotic started:')
    
    
    secondary_report=forms.CharField(widget=forms.Select(choices=PositiveChoice,attrs={'class':'form-control'}),
                                          required=False,label='Any suspected secondary infection:')
    secondary_organism=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Secondary Infection: Positive culture report')
    secondary_sentivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Secondary Infection: Sensitivity pattern:')
    
    root_cause=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required=False, label= 'Root Cause Analysis')
    
    patienttrack=TrackerField(required=False, label= "Patient Tracker Location 1")
    patienttrack1=TrackerField(required=False,label= "Patient Tracker Location 2")
    patienttrack2=TrackerField(required=False,label= "Patient Tracker Location 3")
    patienttrack3=TrackerField(required=False, label= "Patient Tracker Location 4")
    patienttrack4=TrackerField(required=False, label= "Patient Tracker Location 5")
    patienttrack5=TrackerField(required=False, label= "Patient Tracker Location 6")
    class Meta:
        model=CLABSI
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofrecognition':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp', 'username']

        
        labels={'pt_id': 'Patient UHID', 'pt_name':'Patient Name','pt_location':'Patient Location',
                'pt_gender': 'Patient Gender', 'pt_department': 'Department', 'dateofrecognition': 'Date of Recognition'}
        
####################################################################################################
        

########################## MODEL FOUR  ##############################################################
##################### BODY FLUID EXPOSURE ###########################################################
class BodyFluidExposure(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


    staff_id=models.IntegerField()
    staff_name=models.CharField(max_length=100)
    incident_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    staff_gender=models.CharField(max_length=50, choices=CHOICES)
    staff_age=models.IntegerField()
    staff_desig=models.CharField(max_length=100)
    staff_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofincident=models.DateField(default=datetime.date.today)
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class BodyFluidExposureForm(ModelForm):
    
    staff_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Employee ID eg: 182029'}), 
                             label='Staff ID')
    staff_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Staff Age')

        
    staff_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
   
    incident_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    class Meta:
        model=BodyFluidExposure
        fields=['staff_id', 'staff_name',
                 'incident_location', 'staff_gender','staff_age', 
                'staff_department', 'dateofincident', 'report_by']
        widgets={'staff_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'staff_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'incident_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'staff_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'staff_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'staff_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofincident':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp']

        
        labels={'staff_id': 'Staff UHID','staff_name':'Staff Name','incident_location':'Incident Location',
                'staff_gender': 'Staff Gender', 'staff_department': 'Department', 'dataofincident': 'Date of Incident'}
        

######################################################################################################
        

########################## MODEL FIVE  ################################################################
##################### VENTILATOR ASSOCIATED PNEMONIA ##################################################

class VAP(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    
    PositiveChoice=[('Negative','Negative'), ('Positive','Positive'), ('Not Sent', 'Not Sent')]

    
    ComorbiditiesChoices=[('DM','DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'),
                          ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'),
                          ('Immunosuppressed','Immunosuppressed'),('Sepsis', 'Sepsis'),('Malnourished', 'Malnourished'),
                          ('Surgical Intervention', 'Surgical Invervention'), ('Obesity', 'Obesity'),
                        ('Lung Disease', 'Lung Disease')]
    
    CriteriaChoices=[('Appropriate indication for intubation and mechanical ventilation', 'Appropriate indication for intubation and mechanical ventilation'),
                     ('Followed sterile technique','Followed sterile technique'),
                     ('Hand Hygiene before and after handling','Hand Hygiene before and after handling'),
                     ('Head elavation greater than 30 degrees','Head elavation greater than 30 degrees'),
                     ('Daily sedationo vacation', 'Daily sedation vacation'),
                     ('Ventilation tube changed due to any malfunctioning?','Ventilation tube changed due to any malfunctioning?'),
                     ('Ventilation tube changed due to due to soiled with secretion?','Ventilation tube changed due to soiled with secretion?'),
                     ('Humidifier change within 24-48 hourss','Humidifier change within 24-48 hourss'),
                     ('Peptic ulcer disease prophyaxis','Peptic ulcer disease prophyaxis'),
                     ('DVT prophylaxis', 'DVT Prophylaxis'),
                     ('Adequate and regular suctioning', 'Adequate and regualr suctioning'),
                     ('Chest physiotherapy', 'Chest physiotherapy'),
                     ('Cuff pressure monitoring 22-24 cm H2O', 'Cuff pressure monitoring 22-24 cm H2O'),
                     ('Cuff pressure monitoring less than 22cm H2O', 'Cuff pressure monitoring < 22 cm H2O'),
                     ('VAP case definition fulfilled', 'VAP case definition fullfilled'),
                     ('Attempt made at waning the pateint out of ventilator', 'Attempt made at weaning patient out of ventilator'),
                     ('Adequete Staffing level', 'Adequete staffing level'),
                     ('Culture sent?', 'Culture sent?'),
                     ('Any suspencted secondary blood stream infection?', 'Any suspencted secondary blood stream infection?')
                     ]
    
    SignssymptomsChoices=[('Fever','Fever'),('Leukocytosis','Leukocytosis'),('Positive culture report','Positive culture report'),('Apnoea','Apnoea'),
                          ('Bradycardia','Bradycardia')
                          ]
    
    UrinecultureChoices=[('')]
    

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofrecognition=models.DateField(default=datetime.date.today)  ##changed from date of incident
    
    ##
    dateofadmission=models.DateField(default=datetime.date.today)
    dateofdischarge=models.DateField(null=True, blank=True)
    centralline=DeviceDetailsField(null=True, blank=True)
    urinarycatheter=DeviceDetailsField(null=True, blank=True)
    ventilated=DeviceDetailsField(null=True, blank=True)
    tracheostomy=DeviceDetailsField(null=True, blank=True)
    perpheralline=DeviceDetailsField(null=True, blank=True)
    
    comorbidities=MultiSelectField(max_length=300, choices=ComorbiditiesChoices, null=True, blank=True)  ##give choices in forms
    
    criteria=MultiSelectField(max_length=500, choices=CriteriaChoices,null = True, blank=True)  ##give choices in forms
    
    signssymptoms=MultiSelectField(max_length=300, choices=SignssymptomsChoices, null=True, blank=True)  ##give choices in forms
    
    xrayfindings=models.CharField(max_length=100, null=True, blank=True)
    
    ##culture report content
    
    culture=models.CharField(max_length=10,null=True, blank=True)
    culture_verify=models.DateField(null=True, blank=True)
    culture_organism=models.CharField(max_length=150,null=True, blank=True)
    culture_sensitivity=models.CharField(max_length=200, null=True, blank=True)
    culture_antibiotic=models.CharField(max_length=100, null=True, blank=True)
    
    
    ##secondary infection
    secondary_report=models.CharField(max_length=50, null= True, blank=True)
    secondary_organism=models.CharField(max_length=50, null= True, blank=True)
    secondary_sentivity=models.CharField(max_length=200, null=True, blank = True)
    
    root_cause=models.TextField(null=True, blank=True)
    
    report_by=models.CharField(max_length=100)
    #patient tracking table
    patienttrack=PatientTrackerField(null=True, blank=True)
    patienttrack1=PatientTrackerField(null=True, blank=True)
    patienttrack2=PatientTrackerField(null=True, blank=True)
    patienttrack3=PatientTrackerField(null=True, blank=True)
    patienttrack4=PatientTrackerField(null=True, blank=True)
    patienttrack5=PatientTrackerField(null=True, blank=True)
    
    
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class VAPForm(ModelForm):
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')

        
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    
    
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(),label='Date of Admission: ')
    dateofdischarge=forms.DateField(required= False, widget=AdminDateWidget(),label='Date of Discharge: ')
    
    centralline=DeviceField(required=False, label= 'Central Line Device? ')
    urinarycatheter=DeviceField(required=False, label='Urinary Catheter? ')
    ventilated=DeviceField(required=False, label='Intubation/Venti?      ')
    tracheostomy=DeviceField(required=False, label='Tracheostomy?        ')
    perpheralline=DeviceField(required=False, label='Peripheral Line?    ')
    
    comorbidities=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=VAP.ComorbiditiesChoices, required=False, 
                                            label='Comorbidities: (Check applicable)')
    criteria=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=VAP.CriteriaChoices, required=False,
                                       label='Criteria: (Check applicable)')
    signssymptoms=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=VAP.SignssymptomsChoices, required=False,
                                            label='Signs and Symptoms (Check Applicable)')
    
    xrayfindings=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='X-ray Findings Initial: ')
    
    
    culture=forms.CharField(widget=forms.Select(choices=VAP.PositiveChoice,attrs={'class':'form-control'}),required=False,
                                 label='Was the culture sent?')
    culture_verify=forms.DateField(widget= AdminDateWidget(),required=False,label="Culture Verified date:")
    culture_organism=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False,
                                        label="Organism isolated")
    culture_sensitivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Culture: Sensitivity pattern:')
    culture_antibiotic=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Culture: Antibiotic started:')
    
    
    secondary_report=forms.CharField(widget=forms.Select(choices=VAP.PositiveChoice,attrs={'class':'form-control'}),
                                          required=False,label='Any suspected secondary infection:')
    secondary_organism=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Secondary Infection: Positive culture report')
    secondary_sentivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Secondary Infection: Sensitivity pattern:')
    
    root_cause=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required=False, label= 'Root Cause Analysis')
    
    patienttrack=TrackerField(required=False, label= "Patient Tracker Location 1")
    patienttrack1=TrackerField(required=False,label= "Patient Tracker Location 2")
    patienttrack2=TrackerField(required=False,label= "Patient Tracker Location 3")
    patienttrack3=TrackerField(required=False, label= "Patient Tracker Location 4")
    patienttrack4=TrackerField(required=False, label= "Patient Tracker Location 5")
    patienttrack5=TrackerField(required=False, label= "Patient Tracker Location 6")
    class Meta:
        model=VAP
        
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofrecognition':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp', 'username']

        
        labels={'pt_id': 'Patient UHID', 'pt_name':'Patient Name','pt_location':'Patient Location',
                'pt_gender': 'Patient Gender', 'pt_department': 'Department', 'dateofrecognition': 'Date of Recognition'}
        


########################################################################################################


########################## MODEL SIX  ###################################################################
##################### VENTILATOR ASSOCIATED EVENTS ######################################################

class VAE(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    
    PositiveChoice=[('Negative','Negative'), ('Positive','Positive'), ('Not Sent', 'Not Sent')]

    
    ComorbiditiesChoices=[('DM','DM'), ('HTN', 'HTN'), ('CAD', 'CAD'), ('Renal Disease', 'Renal Disease'),
                          ('Malignancy', 'Malignancy'), ('Asthma', 'Asthma'), ('Liver Disease', 'Liver Disease'),
                          ('Immunosuppressed','Immunosuppressed'),('Sepsis', 'Sepsis'),('Malnourished', 'Malnourished'),
                          ('Surgical Intervention', 'Surgical Invervention'), ('Obesity', 'Obesity'),
                        ('Lung Disease', 'Lung Disease')]
    
    CriteriaChoices=[('Appropriate indication for intubation and mechanical ventilation', 'Appropriate indication for intubation and mechanical ventilation'),
                     ('Followed sterile technique','Followed sterile technique'),
                     ('Hand Hygiene before and after handling','Hand Hygiene before and after handling'),
                     ('Head elavation greater than 30 degrees','Head elavation greater than 30 degrees'),
                     ('Daily sedationo vacation', 'Daily sedation vacation'),
                     ('Ventilation tube changed due to any malfunctioning?','Ventilation tube changed due to any malfunctioning?'),
                     ('Ventilation tube changed due to due to soiled with secretion?','Ventilation tube changed due to soiled with secretion?'),
                     ('Humidifier change within 24-48 hourss','Humidifier change within 24-48 hourss'),
                     ('Peptic ulcer disease prophyaxis','Peptic ulcer disease prophyaxis'),
                     ('DVT prophylaxis', 'DVT Prophylaxis'),
                     ('Adequate and regular suctioning', 'Adequate and regualr suctioning'),
                     ('Chest physiotherapy', 'Chest physiotherapy'),
                     ('Cuff pressure monitoring 22-24 cm H2O', 'Cuff pressure monitoring 22-24 cm H2O'),
                     ('Cuff pressure monitoring less than 22cm H2O', 'Cuff pressure monitoring < 22 cm H2O'),
                     ('VAE case definition fulfilled', 'VAE case definition fullfilled'),
                     ('Attempt made at waning the pateint out of ventilator', 'Attempt made at weaning patient out of ventilator'),
                     ('Adequete Staffing level', 'Adequete staffing level'),
                     ('Culture sent?', 'Culture sent?'),
                     ('Any suspencted secondary blood stream infection?', 'Any suspencted secondary blood stream infection?')
                     ]
    
    SignssymptomsChoices=[('Fever','Fever'),('Leukocytosis','Leukocytosis'),('Positive culture report','Positive culture report'),('Apnoea','Apnoea'),
                          ('Bradycardia','Bradycardia')
                          ]
    
    UrinecultureChoices=[('')]
    

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofrecognition=models.DateField(default=datetime.date.today)
    
    #
    dateofadmission=models.DateField(default=datetime.date.today)
    dateofdischarge=models.DateField(null=True, blank=True)
    centralline=DeviceDetailsField(null=True, blank=True)
    urinarycatheter=DeviceDetailsField(null=True, blank=True)
    ventilated=DeviceDetailsField(null=True, blank=True)
    tracheostomy=DeviceDetailsField(null=True, blank=True)
    perpheralline=DeviceDetailsField(null=True, blank=True)
    
    comorbidities=MultiSelectField(max_length=300, choices=ComorbiditiesChoices, null=True, blank=True)  ##give choices in forms
    
    criteria=MultiSelectField(max_length=500, choices=CriteriaChoices,null = True, blank=True)  ##give choices in forms
    
    signssymptoms=MultiSelectField(max_length=300, choices=SignssymptomsChoices, null=True, blank=True)  ##give choices in forms
    
    xrayfindings=models.CharField(max_length=100, null=True, blank=True)
    
    ##culture report content
    
    culture=models.CharField(max_length=10,null=True, blank=True)
    culture_verify=models.DateField(null=True, blank=True)
    culture_organism=models.CharField(max_length=150,null=True, blank=True)
    culture_sensitivity=models.CharField(max_length=200, null=True, blank=True)
    culture_antibiotic=models.CharField(max_length=100, null=True, blank=True)
    
    
    ##secondary infection
    secondary_report=models.CharField(max_length=50, null= True, blank=True)
    secondary_organism=models.CharField(max_length=50, null= True, blank=True)
    secondary_sentivity=models.CharField(max_length=200, null=True, blank = True)
    
    root_cause=models.TextField(null=True, blank=True)
    
    report_by=models.CharField(max_length=100)
    #patient tracking table
    patienttrack=PatientTrackerField(null=True, blank=True)
    patienttrack1=PatientTrackerField(null=True, blank=True)
    patienttrack2=PatientTrackerField(null=True, blank=True)
    patienttrack3=PatientTrackerField(null=True, blank=True)
    patienttrack4=PatientTrackerField(null=True, blank=True)
    patienttrack5=PatientTrackerField(null=True, blank=True)
    
    
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class VAEForm(ModelForm):
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')

        
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(),label='Date of Admission: ')
    dateofdischarge=forms.DateField(required= False, widget=AdminDateWidget(),label='Date of Discharge: ')
    
    centralline=DeviceField(required=False, label= 'Central Line Device? ')
    urinarycatheter=DeviceField(required=False, label='Urinary Catheter? ')
    ventilated=DeviceField(required=False, label='Intubation/Venti?      ')
    tracheostomy=DeviceField(required=False, label='Tracheostomy?        ')
    perpheralline=DeviceField(required=False, label='Peripheral Line?    ')
    
    comorbidities=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=VAE.ComorbiditiesChoices, required=False, 
                                            label='Comorbidities: (Check applicable)')
    criteria=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=VAE.CriteriaChoices, required=False,
                                       label='Criteria: (Check applicable)')
    signssymptoms=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=VAE.SignssymptomsChoices, required=False,
                                            label='Signs and Symptoms (Check Applicable)')
    
    xrayfindings=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='X-ray Findings Initial: ')
    
    
    culture=forms.CharField(widget=forms.Select(choices=VAE.PositiveChoice,attrs={'class':'form-control'}),required=False,
                                 label='Was the culture sent?')
    culture_verify=forms.DateField(widget= AdminDateWidget(),required=False,label="Culture Verified date:")
    culture_organism=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),required=False,
                                        label="Organism isolated")
    culture_sensitivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Culture: Sensitivity pattern:')
    culture_antibiotic=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Culture: Antibiotic started:')
    
    
    secondary_report=forms.CharField(widget=forms.Select(choices=VAE.PositiveChoice,attrs={'class':'form-control'}),
                                          required=False,label='Any suspected secondary infection:')
    secondary_organism=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                            label='Secondary Infection: Positive culture report')
    secondary_sentivity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,
                                             label='Secondary Infection: Sensitivity pattern:')
    
    root_cause=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required=False, label= 'Root Cause Analysis')
    
    patienttrack=TrackerField(required=False, label= "Patient Tracker Location 1")
    patienttrack1=TrackerField(required=False,label= "Patient Tracker Location 2")
    patienttrack2=TrackerField(required=False,label= "Patient Tracker Location 3")
    patienttrack3=TrackerField(required=False, label= "Patient Tracker Location 4")
    patienttrack4=TrackerField(required=False, label= "Patient Tracker Location 5")
    patienttrack5=TrackerField(required=False, label= "Patient Tracker Location 6")
    
    class Meta:
        model=VAE
        
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 #'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofincident':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['username','timestamp']
        error_messages = {
            'pt_id': { 'required':'Please enter UHID',},
            'pt_name':{'required':'Please enter name'},
            'pt_location':{'required':'Please enter location'},
            'pt_gender':{'required':'Please enter Patient gender'},
            'pt_doctor':{'required':'Please enter doctor name'},
            'pt_department':{'required':'Please enter department'},
            'dateofrecogntion':{'required':'Please enter date'},
            'report_by':{'required':'Please enter reporter name'},
            
            }
        

        
        labels={'pt_id': 'Patient UHID', 'pt_name':'Patient Name',
                'pt_gender': 'Patient Gender', 'dateofrecognition': 'Date of Recognition'}
        
##############################################################################################################

########################## MODEL SEVEN  ######################################################################
##################### SURGICAL SITE INFECTION ################################################################

class SSI(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    surgery_name=models.CharField(max_length=100)
    surgery_date=models.DateTimeField(default=datetime.date.today)
    surgery_loc=models.ForeignKey(Locations,on_delete=models.SET_NULL, to_field='loc_name', null=True, blank=True,
                                  related_name='OT_list')
    dateofnotification=models.DateField(default=datetime.date.today)
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class SSIForm(ModelForm):
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
        
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    surgery_loc=forms.ModelChoiceField(queryset=Locations.objects.filter(loc_name__contains='OT'),
                                     widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    class Meta:
        model=SSI
        fields=['pt_id', 'pt_name','pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_department',
                'surgery_name','surgery_date','surgery_loc', 'dateofnotification', 'report_by']
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'surgery_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: CABG'}),
                 'surgery_date':AdminDateWidget(),
                 'surgery_loc':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg:C OT'}),
                 'dateofnotification':AdminDateWidget(),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp']

        
        labels={'pt_id': 'Patient UHID', 'pt_name':'Patient Name','pt_location':'Patient Location', 
                'surgery_name': 'Name of the Surgery', 'surgery_loc': 'Surgery Location',   
                'pt_gender': 'Patient Gender', 'pt_department': 'Department', 'dateofnotification': 'Date of Notification'}


#########################################################################################################

########################## MODEL EIGHT  #################################################################
##################### THROMBOPHLEBITIS ################################################################

class Thrombophlebitis(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofincident=models.DateField(default=datetime.date.today)
    Incidentdetails=models.TextField(null=True, blank = True)
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class ThrombophlebitisForm(ModelForm):
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')

        
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    class Meta:
        model=Thrombophlebitis
        fields=['pt_id', 'pt_name','pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_department', 'dateofincident',
                'Incidentdetails', 'report_by']
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofincident':AdminDateWidget(),
                 'Incidentdetails':forms.Textarea(attrs={'class':'form-control'}),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp']

        
        labels={'pt_id': 'Patient UHID', 'pt_name':'Patient Name','pt_location':'Patient Location',
                'pt_gender': 'Patient Gender', 'pt_department': 'Department', 'dataofincident': 'Date of Incident',
                'Incidentdetails':'Incident Details'}
        
##########################################################################################################

########################## MODEL NINE  ###################################################################
##################### NEEDLE STICK INJURY ################################################################

class NSI(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


    staff_id=models.IntegerField()
    staff_name=models.CharField(max_length=100)
    staff_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', null=True, blank=True)
    staff_gender=models.CharField(max_length=50, choices=CHOICES)
    staff_age=models.IntegerField()
    dateofincident=models.DateField(default=datetime.date.today)
    Incidentdetails=models.TextField(null=True, blank = True)
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank = True, null=True)
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),default=6)
    
class NSIForm(ModelForm):
    
    staff_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':' eg: 182029'}), 
                             label='Staff ID')
    staff_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Staff Age')

        
    
    staff_location=forms.ModelChoiceField(queryset=Locations.objects.all(), 
                                           widget=forms.Select(attrs={'class':'form-control'}),
                                           label = 'Location', empty_label=('Unselected'))
    class Meta:
        model=NSI
        fields=['staff_id', 'staff_name','staff_location', 'staff_gender','staff_age', 'dateofincident',
                'Incidentdetails', 'report_by']
        widgets={'staff_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'staff_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'staff_location':forms.Select(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'staff_gender':forms.Select(choices= CAUTI.CHOICES, attrs={'class': 'form-control'}),
                 'staff_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'dateofincident':AdminDateWidget(),
                 'Incidentdetails':forms.Textarea(attrs={'class':'form-control'}),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }

        exclude=['timestamp']

        
        labels={'staff_id': 'Staff ID', 'Staff_name':'Staff Name','staff_location':'Staff ward/ICU',
                'staff_gender': 'Staff Gender', 'staff_age': 'Staff Age', 'dataofincident': 'Date of Incident',
                'Incidentdetails':'Incident Details', 'report_by': 'Report By'}
        


