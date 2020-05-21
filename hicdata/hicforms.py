from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class CAUTIFORM1(forms.Form):
    Pt_id = forms.IntegerField(min_value=9999,  max_value=999999, label = "Patient UHID",error_messages={'required': 'please enter UHID',
                                                                                                         'max_length': 'Please enter valid UHID',
                                                                                                         'min_length': 'Please enter valid UHID'},
                               widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}))
    pt_name = forms.CharField(max_length=100, label= 'Patient Name',
                              widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}))
    pt_location =forms.CharField(max_length=50, label= 'Ward/ICU Location',
                              widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Joy Mathew'}))
    CHOICES=[('Male', 'Male'),('Female', 'Female'),('Other', 'Other')]
    pt_sex=forms.ChoiceField(label='Patient Age', widget=forms.Select(attrs={'class': 'form-control'}),choices=CHOICES)
    pt_age=forms.IntegerField(min_value=0, max_value=200, label="Patient Age",
                              widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':"Patient's age"}))
    pt_doctor=forms.CharField(max_length=100, label= 'Doctor Name',
                              widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Eg: Dr John'}))
    pt_department=forms.CharField(max_length=100, label= 'Department Name',
                              widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Cardiology'}))
    dateofadmninstration=forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}), label='Date of Administration')

    report_by=forms.CharField(max_length=100, label= 'Reported By',
                              widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': "Nurse's Name"}))
   # report_by=

