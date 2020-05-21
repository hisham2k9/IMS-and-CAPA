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
from django.utils import timezone
from django.forms import DateTimeInput
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime  #admindate


# Create your models here.


##for custom admin datetime split am pm
class CustomAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)

##for sentinal user deleted user data
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


# class DateInput(forms.DateInput):
#     input_type='date'

# class BootstrapDateTimePickerInput(DateTimeInput):
#     template_name = 'widgets/bootstrap_datetimepicker.html'

#     def get_context(self, name, value, attrs):
#         datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
#         if attrs is None:
#             attrs = dict()
#         attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
#         attrs['class'] = 'form-control datetimepicker-input'
#         context = super().get_context(name, value, attrs)
#         context['widget']['datetimepicker_id'] = datetimepicker_id
#         return context

##################### MODEL ONE ##########################################################
###Return to ICU form and model form   ###################################################
#######################################################################################

class ReturnToICU(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name')
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_diagnosis=models.CharField(max_length=200)
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadmission=models.DateField(default=datetime.date.today)
    datetime_transfer_out=models.DateTimeField(default=timezone.now)
    transfer_to=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', related_name='TransferWard')
    datetime_return=models.DateTimeField(default=timezone.now)
    reason_return=models.TextField()
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), null=True)
    
class ReturnToICUForm(ModelForm):

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
    transfer_to=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       label='Transfer To Ward:', empty_label=('Unselected'))
    
  #  datetime_transfer_out = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'dateinput form-control hasDatepicker'}))
    datetime_transfer_out=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label ='Date and time of Transfer out')
    datetime_return =forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Return ')    
    
    class Meta:
        model=ReturnToICU
        fields=[ 'pt_id','pt_name', 'pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_diagnosis',
                'pt_department','dateofadmission','datetime_transfer_out','transfer_to',
                 'datetime_return','reason_return', 'report_by']
        widgets={'pt_id':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}),
                 'pt_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_location':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'pt_gender':forms.Select(choices= ReturnToICU.CHOICES, attrs={'class': 'form-control'}),
                 'pt_age':forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}),
                 'pt_doctor':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}),
                 'pt_diagnosis':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: CAD'}),
                 'pt_department':forms.Select(attrs={'class':'form-control'}),
                 'dateofadmission':AdminDateWidget(),
                 'datetime_transfer_out':CustomAdminSplitDateTime(),  
                 'transfer_to':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}),
                 'datetime_return':forms.TextInput(attrs={'class':'form-control'}), 
                 'reason_return':forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Eg:Pt condition worsen'}),
                 'report_by':forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"})
                 }
        exclude=['timestamp']


        
        labels={'pt_id': 'Patient UHID','pt_name':'Patient Name','pt_location':'Patient Location',
                'pt_gender': 'Patient Gender', 'pt_age':'Patient Age', 'pt_department': 'Department', 
                'pt_diagnosis':'Diagnosis of Patient','dateofadmission':'Date of Admission',
                'datetime_transfer_out':'Date and Time of Transfer out','transfer_to': 'Transfer To Ward:',
                'datetime_return':'Date and Time of Return:','report_by': 'Report By'}
        
#########################################################################################################################


##################### MODEL TWO ##########################################################
###Intubation form and model form   ###################################################
#######################################################################################

class Intubation(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    Transferchoices=[('Transfer-Out', 'Transfer-Out'), ('Death', 'Death')]

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name')  ##present location
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_diagnosis=models.CharField(max_length=200)
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadmission=models.DateField(default=datetime.date.today)
    loc_intubation=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name', related_name='IntubationLocation')
    datetime_intubation=models.DateTimeField(default=timezone.now)
    datetime_extubation=models.DateTimeField(default=timezone.now)
    comments=models.TextField()
    transferchoice=models.CharField(max_length=50, choices=Transferchoices, default='Not Given', null=True, blank=True)
    report_by=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), null=True)
    
class IntubationForm(ModelForm):
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Eg: Ajay Philip'}),
                            label='Patient Name')
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    pt_gender=forms.CharField(max_length=50, widget=forms.Select(choices= ReturnToICU.CHOICES, attrs={'class': 'form-control'}),
                           label='Patient Gender')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_diagnosis=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}),label='Diagnosis')
    
    
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(), label="Date of Admission")
    
    loc_intubation=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       label='Location of Intubation:', empty_label=('Unselected'))
    
    datetime_intubation=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label ='Date and time of Intubation')
    
    datetime_extubation =forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Extubation')
    
    transferchoice=forms.CharField(max_length=50,widget=forms.Select(
        choices=Intubation.Transferchoices,attrs={'class':'form-control'}), label='Transfer-Out OR Death')
    
    comments=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='Comments')
    
    report_by=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nurse Name'}), 
                              label='Report By') 
       
    
    class Meta:
        model=Intubation
        fields=[ 'pt_id','pt_name', 'pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_diagnosis',
                'pt_department','dateofadmission','loc_intubation','datetime_intubation','datetime_extubation',
                 'comments', 'report_by']

        exclude=['timestamp']
        
        
#########################################################################################################################


##################### MODEL THREE ##########################################################
###Reintubation form and model form   ###################################################
#######################################################################################

class Reintubation(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name')  ##present location
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors, on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_diagnosis=models.CharField(max_length=200)
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadmission=models.DateField(default=datetime.date.today)
    loc_intubation=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown',
                                      to_field='loc_name',related_name='IntubationLocation1')  #'intubationLocation'1', since relatedname is already used

    datetime_intubation=models.DateTimeField(default=timezone.now)
    datetime_extubation=models.DateTimeField(default=timezone.now)
    datetime_reintubation=models.DateTimeField(default=timezone.now)
    
    reason_reintubation=models.TextField()
    report_by=models.CharField(max_length=100)
    
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), null=True)
    
class ReintubationForm(ModelForm):
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Eg: Ajay Philip'}),
                            label='Patient Name')
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    pt_gender=forms.CharField(max_length=50, widget=forms.Select(choices= ReturnToICU.CHOICES, attrs={'class': 'form-control'}),
                           label='Patient Gender')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_diagnosis=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}),label='Diagnosis')
    
    
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(), label="Date of Admission")
    
    loc_intubation=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       label='Location', empty_label=('Unselected'))
    
    datetime_intubation=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label ='Date and time of Intubation')
    
    datetime_extubation =forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Extubation')
    datetime_reintubation=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Re-Intubation')
    
    comments=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='Comments')
    
    report_by=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nurse Name'}), 
                              label='Report By') 
       
    
    class Meta:
        model=Reintubation
        fields=[ 'pt_id','pt_name', 'pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_diagnosis',
                'pt_department','dateofadmission','loc_intubation','datetime_intubation','datetime_extubation',
                 'datetime_reintubation','comments', 'report_by']

        exclude=['timestamp']
        
#########################################################################################################################


##################### MODEL FOUR ##########################################################
###Pressure Injury form and model form   ###################################################
#######################################################################################

class PressureInjury(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name')  ##present location
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors,on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_diagnosis=models.CharField(max_length=200)
    pt_department=models.ForeignKey(Departments,on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadmission=models.DateField(default=datetime.date.today)
    dateofobservation=models.DateField(default=datetime.date.today)
    loc_ulcer=models.CharField(max_length=200)
    grade=models.IntegerField()
    hapu_dapu_out=models.CharField(max_length=50)
    outcome=models.TextField()
    remarks=models.TextField()
    
    report_by=models.CharField(max_length=100)
    
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), null=True)
    
class PressureInjuryForm(ModelForm):
    
    GradeChoices=[(1,1),(2,2),(3,3),(4,4)]
    HapuDapuChoices=[('HAPU','HAPU'),('DAPU','DAPU'),('Outside','Outside')]
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Eg: Ajay Philip'}),
                            label='Patient Name')
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    pt_gender=forms.CharField(max_length=50, widget=forms.Select(choices= ReturnToICU.CHOICES, attrs={'class': 'form-control'}),
                           label='Patient Gender')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_diagnosis=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}),label='Diagnosis')
    
    
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(), label="Date of Admission")
    
    dateofobservation=forms.DateField(widget=AdminDateWidget(), label="Date of Observation")
    
    loc_ulcer=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ulcer Location'}),
                            label='Location of Ulcer')
    
    grade=forms.IntegerField(min_value=0, max_value=100,
                             widget=forms.Select(choices=GradeChoices,attrs={'class' : 'form-control'}), 
                             label='Grade of Pressure Injury')
    
    hapu_dapu_out=forms.CharField(max_length=50, widget=forms.Select(choices= HapuDapuChoices, attrs={'class': 'form-control'}),
                           label='HAPU/DAPU/Outside')
    
    outcome=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='Outcome:')
    
    remarks=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='Remarks')
    
    report_by=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nurse Name'}), 
                              label='Report By') 
       
    
    class Meta:
        model=PressureInjury
        fields=[ 'pt_id','pt_name', 'pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_diagnosis',
                'pt_department','dateofadmission','dateofobservation','loc_ulcer','grade',
                'hapu_dapu_out','outcome','remarks', 'report_by']

        exclude=['timestamp']
        
#########################################################################################################################


##################### MODEL FIVE ##########################################################
####### Tracheostomy form and model form   ###################################################
###########################################################################################

class Tracheostomy(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name')  ##present location
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors,on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_diagnosis=models.CharField(max_length=200)
    pt_department=models.ForeignKey(Departments, on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadmission=models.DateField(default=datetime.date.today)
    loc_tracheostory=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name',
                                       related_name='tracheostomy_loc')
    datetime_tracheostomy=models.DateTimeField(default=timezone.now)
    comments=models.TextField(null=True, blank= True)
    
    report_by=models.CharField(max_length=100)
    
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), null=True)
    
class TracheostomyForm(ModelForm):
    
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Eg: Ajay Philip'}),
                            label='Patient Name')
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    pt_gender=forms.CharField(max_length=50, widget=forms.Select(choices= ReturnToICU.CHOICES, attrs={'class': 'form-control'}),
                           label='Patient Gender')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_diagnosis=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}),label='Diagnosis')
    
    
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(), label="Date of Admission")
    
    loc_tracheostory=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Tracheostomy done from:', empty_label=('Unselected'))
    
    
    datetime_tracheostomy=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Tracheostomy')
    comments=forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}), label='Comments')
    
    report_by=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nurse Name'}), 
                              label='Report By') 
       
    
    class Meta:
        model=Tracheostomy
        fields=[ 'pt_id','pt_name', 'pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_diagnosis',
                'pt_department','dateofadmission','loc_tracheostory','datetime_tracheostomy',
                'comments', 'report_by']

        exclude=['timestamp']
        
        
#########################################################################################################################


##################### MODEL SIX ##########################################################
####### Tracheostomy form and model form   ###################################################
###########################################################################################

class RestraintInjury(models.Model):
    CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    YesNo=[('Yes', 'Yes'), ('No', 'No')]

    pt_id=models.CharField(max_length=20)
    pt_name=models.CharField(max_length=100)
    pt_location=models.ForeignKey(Locations,on_delete=models.SET_DEFAULT,default='Unknown', to_field='loc_name')  ##present location
    pt_gender=models.CharField(max_length=50, choices=CHOICES)
    pt_age=models.IntegerField()
    pt_doctor=models.ForeignKey(Doctors,on_delete=models.SET_DEFAULT,default='Unknown', to_field='doc_name')
    pt_diagnosis=models.CharField(max_length=200)
    pt_department=models.ForeignKey(Departments,on_delete=models.SET_DEFAULT,default='Unknown', to_field='dept_name')
    dateofadmission=models.DateField(default=datetime.date.today)
    indicationof_restraint=models.CharField(max_length=200)
    datetime_restraintstart=models.DateTimeField(default=timezone.now)
    datetime_restraintremoval=models.DateTimeField(default=timezone.now)
    obtain_consent=models.CharField(max_length=50, choices=YesNo)
    maintain_observation=models.CharField(max_length=50, choices=YesNo)
    injury=models.CharField(max_length=50, choices=YesNo)
    
    injury_details=models.TextField(null=True, blank= True)
    
    report_by=models.CharField(max_length=100)
    
    timestamp=models.DateTimeField(auto_now_add= True,blank=True, null=True )
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), null=True)
    
class RestraintInjuryForm(ModelForm):
    
    
    pt_id=forms.IntegerField(min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient UHID')
    pt_name=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Eg: Ajay Philip'}),
                            label='Patient Name')
    pt_location=forms.ModelChoiceField(queryset=Locations.objects.all(),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                        label = 'Location', empty_label=('Unselected'))
    pt_gender=forms.CharField(max_length=50, widget=forms.Select(choices= ReturnToICU.CHOICES, attrs={'class': 'form-control'}),
                           label='Patient Gender')
    pt_age=forms.IntegerField(min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Patient Age')
    pt_doctor=forms.ModelChoiceField(queryset=Doctors.objects.all(),
                                      widget=forms.Select(attrs={'class':'form-control'}),
                                      label = 'Doctor', empty_label=('Unselected'))
    pt_diagnosis=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}),label='Diagnosis')
    
    
    pt_department=forms.ModelChoiceField(queryset=Departments.objects.all(),
                                        widget=forms.Select(attrs={'class':'form-control'}),
                                         label = 'Department', empty_label=('Unselected'))
    
    dateofadmission=forms.DateField(widget=AdminDateWidget(), label="Date of Admission")
    
    indicationof_restraint=forms.CharField(max_length=200, widget=forms.TextInput
                            (attrs={'class':'form-control', 'placeholder':'Please provide indication details'}),
                            label='Indication of Restraint')
    
    
    datetime_restraintstart=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Restrain Start:')
    
    datetime_restraintremoval=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label='Date and Time of Restrain End:')
    
    
    obtain_consent=forms.CharField(max_length=50, widget=forms.Select(choices=RestraintInjury.YesNo,
                                                                      attrs={'class':'form-control'}),label='Obtain Consent?')
    
    
    maintain_observation=forms.CharField(max_length=50, widget=forms.Select(choices=RestraintInjury.YesNo,
                                                                      attrs={'class':'form-control'}),
                                         label='Obtain Observation Chart?')
    
    injury=forms.CharField(max_length=50, widget=forms.Select(choices=RestraintInjury.YesNo,
                                                                      attrs={'class':'form-control'}),
                                         label='Injury?')
        
    
    injury_details=forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':
        "Please provide comments if 'yes' for injury"}), label='Injury Details')
    
    report_by=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nurse Name'}), 
                              label='Report By') 
       
    
    class Meta:
        model=RestraintInjury
        fields=[ 'pt_id','pt_name', 'pt_location', 'pt_gender','pt_age', 'pt_doctor','pt_diagnosis',
                'pt_department','dateofadmission','indicationof_restraint','datetime_restraintstart',
                'datetime_restraintremoval','obtain_consent','maintain_observation','injury',
                'injury_details', 'report_by']

        exclude=['timestamp']
