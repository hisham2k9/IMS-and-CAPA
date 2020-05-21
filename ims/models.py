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
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime
from multiselectfield import MultiSelectField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
#from .formatChecker import ContentTypeRestrictedFileField
from django.core.exceptions import ValidationError

#############
##for custom admin datetime split am pm
class CustomAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)

##for sentinal user deleted user data
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

###
##incident managesystem report model

class imsmodel(models.Model):
    
    ###choices tuple lists
    gender_choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    anaesthesia_surgery_choices=[('Complications of Anaesthesia', 'Complications of Anaesthesia'),
                                 ('Intubation Related', 'Intubation related'),
                                 ('Accidental extubation', 'Accidental Extubation'),
                                 ('Wrong patient or wrong site-side', 'Wrong patient or wrong site-side'),
                                 ('Acute MI within 48 hours of surgery', 'Acute MI within 48 hours of surgery'),
                                 ('Sponge or Instrument or Needle left in situ', 'Sponge or Instrument or Needle left in situ'),
                                 ('Retained Foreign body removal', 'Retained foreign body removal'),
                                 ('Death in OT or within 48 hours of surgery ', 'Death in OT or within 48 hours of surgery'),
                                 ]
    communication_related_choices=[('Lab speciment improperly prepared/collected', 'Lab specimen improperly prepared'),
                                   ('Sample improperly labelled', 'Sample improperly labelled')
                                   ]
    
    consent_related_choices=[('Consent not obtained or documented', 'Consent not obtained or documented'),
                             ('Inadequete consent', 'Inadequete consent'),
                             ]
    
    emergency_related_choices=[('Patient left against medical advice', 'Patient left against medical advice'),
                                 ('Reports and patients documents misplaced', 'Reports and patients documents misplaced'),
                                 ]
    
    safety_falls_related_choices=[('Patient fall', 'Patient fall'),
                        ('Self Inflicted injury', 'Self Inflicted injury'),
                        ('Visitor Falls or Injury', 'Visitor Falls or Injury'),
                        ('Assault on patient  or Staff', 'Assault on patient or Staff'),
                        ('Needle stick Injury', 'Needle stick Injury'),
                        ('Hazardous Material Spillage', 'Hazardous Material Spillage'),
                        ]
    
    diagnosis_related_choices=[('Management of care', 'Management of care'),
                                ('Delay in starting treatment', 'Delay in starting treatment'),
                                ('Patient not seen by Doctor', 'Patient not seen by Doctor'),
                                ('Repeat blood sample withdrawal', 'Repeat blood sample withdrawal'),
                                ]
    
    transfusion_related_choices=[('Variance in use of blood and blood products', 'Variance in use of blood and blood products'),
                                ('Transfusion stopped due to reaction', 'Transfusion stopped due to reaction'),
                                ]
    
    equipment_related_choices=[('Equipment not available', 'Equipment not available'),
                                ('Equipment malfunctioned', 'Equipment malfunctioned'),
                                ]
    
    medication_variance_choices=[('Prescription error', 'Prescription error'),
                                ('Indenting error', 'Indenting error'),
                                ('Dispensing error','Dispensing error'),
                                ('Administration error (Violation of any of the rights)','Administration error (Violation of any of the rights)'),
                                ('Drug given to patient with known allergy.','Drug given to patient with known allergy.'),
                                ]
    
    misc_choices=[('Security related', 'Security related'),
                  ('Theft of personal property', 'Theft of personal property'),
                  ('Infrastructure failure or collapse', 'Infrastrucure failure or collapse')
                  ]
    
    management_of_care_choices=[('Non availability of doctor on call','Non availability of doctor on call')
                                ]
    
    contributing_factors_choices=[('Language Barrier','Language Barrier'),
                                  ('Hearing problems','Hearing problems'),
                                  ('Limited Vision','Limited Vision'),
                                  ('Obesity','Obesity'),
                                  ('Seizures','Seizures'),
                                  ('Intoxication','Intoxication'),
                                  ('Physical handicaps','Physical handicaps'),
                                  ]
    pt_condition_choices=[('Well Oriented','Well Oriented'),
                            ('Confused','Confused'),
                            ('Sedated','Sedated'),
                            ('Drowsy','Drowsy'),
                            ('Hyperactive','Hyperactive'),
                            ('Uncooperative','Uncooperative'),
                            ('Violent','Violent'),
                            ]
    action_taken_choices=[('Informed Consultant or HOD', 'Informed Consultant or HOD'),
                          ('Event recorded in the file','Event recorded in the file'),
                          ('Seen by attending physician','Seen by attending physician'),
                          ]
    
    severity_score_choices=[('No harm or No treatment','No harm or No treatment'),
                            ('Insignificant harm or minimal treatment','Insignificant harm or minimal treatment'),
                            ('Significant Physical intervention/Residual effect possible', 'Significant Physical intervention/Residual effect possible'),
                            ('Major or extensive intervention/Residual effect','Major or extensive intervention/Residual effect'),
                            ('Major potentially life threatening disability or residual effects','Major potentially life threatening disability or residual effects'),
                            ('Death Imminent or predictable','Death Imminent or predictable'),
                            ('Resultant Death', 'Resultant Death'),
                            ]
    
    pt_id=models.CharField(max_length=20) #emp or pt id
    pt_name=models.CharField(max_length=100)  #name of person involved
    pt_gender=models.CharField(max_length=50, choices=gender_choices) 
    pt_age=models.IntegerField(null=True, blank=True)
    
    datetime_creation=models.DateTimeField(default=datetime.datetime.now)
    
    pt_room=models.CharField(max_length=100) #room number or place
    pt_department=models.CharField(max_length=100)  #dept name
    pt_doctor=models.CharField(max_length=100, null=True, blank=True)  ##physician/hod involved
    
    datetime_occurance=models.DateTimeField(default=datetime.datetime.now)
    place_occurance=models.CharField(max_length=100) ##place of occurance
    
    #####EVent occurance multiselect
    anaesthesia_surgery=MultiSelectField(max_length=300, choices= anaesthesia_surgery_choices, null=True, blank=True) 
    anaesthesia_surgery_others=models.CharField(max_length=200, null=True, blank = True)
    
    communication_related=MultiSelectField(max_length=300, choices= communication_related_choices, null=True, blank=True) 
    communication_others=models.CharField(max_length=200, null=True, blank = True)
    
    consent_related=MultiSelectField(max_length=300, choices= consent_related_choices, null=True, blank=True)
    consent_related_others=models.CharField(max_length=200, null=True, blank=True)
    
    emergency_related=MultiSelectField(max_length=300, choices=emergency_related_choices, null=True, blank=True)
    emergency_related_others=models.CharField(max_length=200, null=True, blank=True)
    
    safety_falls_related=MultiSelectField(max_length=300, choices=safety_falls_related_choices, null=True, blank=True)
    safety_falls_related_others=models.CharField(max_length=200, null=True, blank=True)
    
    diagnosis_related=MultiSelectField(max_length=300, choices=diagnosis_related_choices, null=True, blank=True)
    diagnosis_related_others=models.CharField(max_length=200, null=True, blank=True)
    
    transfusion_related=MultiSelectField(max_length=300, choices=transfusion_related_choices, null=True, blank=True)
    transfusion_related_others=models.CharField(max_length=200, null=True, blank=True)
    
    equipment_related=MultiSelectField(max_length=300, choices=equipment_related_choices, null=True, blank=True)
    equipment_related_others=models.CharField(max_length=200, null=True, blank=True)
    
    medication_variance=MultiSelectField(max_length=300, choices=medication_variance_choices, null=True, blank=True)
    medication_variance_others=models.CharField(max_length=200, null=True, blank=True)
    
    misc=MultiSelectField(max_length=300, choices=misc_choices, null=True, blank=True)
    misc_others=models.CharField(max_length=200, null=True, blank=True)
    
    management_of_care=MultiSelectField(max_length=300, choices=management_of_care_choices, null=True, blank=True)
    management_of_care_others=models.CharField(max_length=200, null=True, blank=True)
    
    contributing_factors=MultiSelectField(max_length=300, choices=contributing_factors_choices, null=True, blank=True)
    contributing_factors_others=models.CharField(max_length=200, null=True, blank=True)
    
    pt_condition=MultiSelectField(max_length=300, choices=pt_condition_choices, null=True, blank=True)
    pt_condition_others=models.CharField(max_length=200, null=True, blank=True)
    
    action_taken=MultiSelectField(max_length=300, choices=action_taken_choices, null=True, blank=True)
    action_taken_others=models.CharField(max_length=200, null=True, blank=True)
    
    severity_score=MultiSelectField(max_length=300, choices=severity_score_choices, null=True, blank=True)
    severity_score_others=models.CharField(max_length=200, null=True, blank=True)
    
    narration=models.TextField(null=True, blank=True)
    
    relevant_info=models.TextField(null=True, blank=True)

    report_to=models.CharField(max_length=100)
    
    
    
    ##ADD image upload
    
    #HIDDEN INFORMATION
    submission_confirm_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1)
    submission_update_timestamp=models.DateTimeField(default=datetime.datetime.now)
    submit_confirm_switch=models.BooleanField(default=False)
    
    ##first form ends here........................
    
    ##Stage 2:reaches QMS
    
    assign_comments_qa=models.TextField(null=True, blank = True)
    assign_comments_qa_by=models.CharField(max_length=100 , null=True, blank=True)
    qa_assign_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='assign_to_user', verbose_name='Assign To',
                                   to_field='username'       #gives integrity error
                                   )
    #ADD image data
    
    ##hiddenfields
    
    assign_qa_comments_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1, related_name='assign_user')
    assign_qa_comments_update_timestamp=models.DateTimeField(default=datetime.datetime.now)
    assign_qa_comments_confirm_switch=models.BooleanField(default=False)
    
    
    #STAGE 3: hod contents
    
    investigation_comments_hod=models.TextField(null=True, blank=True)
    investigation_by=models.CharField(max_length=100,null=True, blank=True)
    ##ADD IMAGESS
    
    ##hidden fields
    investigation_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1, related_name='investigator')
    investigation_update_timestamp=models.DateTimeField(default=datetime.datetime.now)
    investigation_confirm_switch=models.BooleanField(default=False)
    
    
    ##STAGE 4: validation confirm
    
    validation_comments_qa=models.TextField(null=True, blank=True)
    validation_final_type=models.CharField(max_length=100,null=True, blank=True, default="Not Assigned") #final grouping.. to appear to table
    validation_final_reason=models.CharField(max_length=100, null=True, blank=True, default="Not Assigned") #final reason... to appear to table
    validation_qa_by=models.CharField(max_length=100, null=True, blank=True)
    #add images upload
    
    ##hidden fields
    validation_confirm_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1, related_name='validator')
    validation_confirm_update_timestamp=models.DateTimeField(default=datetime.datetime.now)
    validation_confirm_switch=models.BooleanField(default=False)
    
    
    ##STAGE 5: CQO comments
    
    corrective_action=models.CharField(max_length=200,null=True, blank=True)
    comments_cqo=models.TextField(null=True, blank=True)

    closure_by=models.CharField(max_length=100,null=True, blank=True)
    ##add image data
    
    ##hidden fields
    closure_confirm_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1,related_name='closure_person')
    closure_update_timestamp=models.DateTimeField(default=datetime.datetime.now)
    closure_confirm_switch=models.BooleanField(default=False)
    
    def __str__(self):
        return "{} - {}".format(self.pt_id, self.pt_name)
    
class imssubmissionfiles(models.Model):
    post = models.ForeignKey(imsmodel, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='submission_files', null=True, blank=True)
    date=models.DateTimeField(default=None, null=True, blank=True)
    
    def __str__(self):
        return "{} - {}".format(self.post, self.file)

class imsassignfiles(models.Model):
    post = models.ForeignKey(imsmodel,on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='assign_files', null=True, blank=True)
    date=models.DateTimeField(default=None, null=True, blank=True)
    
class imsinvestigationfiles(models.Model):
    post = models.ForeignKey(imsmodel, on_delete=models.CASCADE,default=None)
    file = models.FileField(upload_to='investigation_files', null=True, blank=True)
    date=models.DateTimeField(default=None, null=True, blank=True)
    
class imsvalidationfiles(models.Model):
    post = models.ForeignKey(imsmodel, on_delete=models.CASCADE,default=None)
    file = models.FileField(upload_to='validation_files', null=True, blank=True)
    date=models.DateTimeField(default=None, null=True, blank=True)
    
class imsclosurefiles(models.Model):
    post = models.ForeignKey(imsmodel, on_delete=models.CASCADE,default=None)
    file = models.FileField(upload_to='closure_files', null=True, blank=True)
    date=models.DateTimeField(default=None, null=True, blank=True)
    


class imssubmissionform(ModelForm):
    
    pt_id=forms.IntegerField(required=True,min_value=99999, max_value=999999,
                             error_messages  ={'min_value': 'Please enter a valid UHID','max_value':'Please enter a valid UHID'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'UHID eg: 182029'}), 
                             label='Patient or Employee ID') #emp or pt id
    pt_name=forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class':'form-control',
                                                                                        'placeholder':'Eg: Sudarshan'})
                            ,label='Name of the person')  #name of person involved
    pt_gender=forms.CharField(required=True,max_length=50, 
                              widget=forms.Select(attrs={'class':'form-control'},choices=imsmodel.gender_choices),
                              label='Gender') 
    
    pt_age=forms.IntegerField(required=True,min_value=0, max_value=200,
                             error_messages  ={'min_value': 'Please enter a age','max_value':'Please enter a valid age'},
                             widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'EG: 60'}), 
                             label='Age')
    
    datetime_creation=forms.SplitDateTimeField(initial=datetime.datetime.now, label ='Date and time', disabled=True)
    
    #datetime_update=models.DateTimeField(auto_now=True)
    
    pt_room=forms.CharField(required=True,max_length=100,
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: 7506'}),
                             label='Room of Incident') #room number or place
    
    pt_department=forms.CharField(required=True,max_length=100,
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Housekeeping'}),
                             label='Department of Incident') #room number or place
    
    pt_doctor=forms.CharField(required=True,max_length=100,
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Dr Sadashivan'}),
                             label='Doctor (physician/HOD):')  ##physician/hod involved
    
    datetime_occurance=forms.SplitDateTimeField(widget=CustomAdminSplitDateTime(), label ='Date and time of Occurance')
    place_occurance=forms.CharField(max_length=100) ##place of occurance
    
    
    
    class Meta:
        model=imsmodel
        
        fields=['pt_id', 'pt_name','pt_gender','pt_age','datetime_creation','pt_room',
                'pt_department','pt_doctor','datetime_occurance','place_occurance'
                ]
    
class imssubmissiondetailsform(ModelForm):  
    
    #####EVent occurance multiselect
    
    test=forms.CharField(widget=forms.HiddenInput(),disabled=True, required=False)
    anaesthesia_surgery=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.anaesthesia_surgery_choices,
                                             required=False,
                                       label='Anaesthesia/Surgery Criteria: (Select applicable)')
    
    anaesthesia_surgery_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Anaesthesia/Surgey):')
    
    communication_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.communication_related_choices,
                                             required=False,
                                       label='Communication related Criteria: (Select applicable)')
    communication_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Communication):')
    
    consent_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.consent_related_choices,
                                             required=False,
                                       label='Consent related Criteria: (Select applicable)')
    consent_related_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Consent):')
    
    emergency_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.emergency_related_choices,
                                             required=False,
                                       label='Emergency Related Criteria: (Select applicable)')
    
    emergency_related_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Emergency Dept.):')
    
    
    safety_falls_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.safety_falls_related_choices,
                                             required=False,
                                       label='Safety/Falls related Criteria: (Select applicable)')
    safety_falls_related_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Safety/Falls):')
    
    diagnosis_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.diagnosis_related_choices,
                                             required=False,
                                       label='Diagnosis/Treatment Related Criteria: (Select applicable)')
    diagnosis_related_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Diagnosis/Safety):')
    
    transfusion_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.transfusion_related_choices,
                                             required=False,
                                       label='Transfusion Related Criteria: (Select applicable)')
    transfusion_related_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (transfusion related):')
    
    
    equipment_related=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.equipment_related_choices,
                                             required=False,
                                       label='Equipment Related Criteria: (Select applicable)')
    equipment_related_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details(others):')
    
    medication_variance=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.medication_variance_choices,
                                             required=False,
                                       label='Medication Variances Criteria: (Select applicable)')
    medication_variance_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Medication Variances):')
    
    misc=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.misc_choices,
                                             required=False,
                                       label='Miscellaneous Criteria: (Select applicable)')
    misc_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Miscellaneous):')
    
    management_of_care=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.management_of_care_choices,
                                             required=False,
                                       label='Management of Care Criteria: (Select applicable)')
    management_of_care_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details(Management of care):')
    
    contributing_factors=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.contributing_factors_choices,
                                             required=False,
                                       label='Contributing Factors Criteria: (Select applicable)')
    contributing_factors_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details (Contributing factors):')
    
    pt_condition=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.pt_condition_choices,
                                             required=False,
                                       label='Patient condition(before incident): (Select applicable)')
    pt_condition_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details(Patient Condition):')
    
    action_taken=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.action_taken_choices,
                                             required=False,
                                       label='Action Taken: (Select applicable)')
    action_taken_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details(Actions taken):')
    
    severity_score=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'selectmulti'}), choices=imsmodel.severity_score_choices,
                                             required=False,
                                       label='Severity Score: (Select applicable)')
    severity_score_others=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: other details'}),
                                               label='Other details(severity score):')
    
    narration=forms.CharField(required=False,
                                               widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Eg: A narration of incident....'}),
                                               label='A narrative description of the occurance')
    
    relevant_info=forms.CharField(required=False,
                                               widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Eg: A Relevalnt Information....'}),
                                               label='Any other relevant information about the occurance')
    
    report_to=forms.CharField(widget=forms.HiddenInput(),max_length=100, initial='Quality')
    
    
    
    ##ADD image upload
    
    #HIDDEN INFORMATION
    #submission_confirm_user=forms.CharField(widget=forms.HiddenInput(), required=False)
    submission_update_timestamp=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now,
                                                    label='Submitted on')
    submit_confirm_switch=forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False,
                                             label='Submit Confirm')
    
    class Meta:
        model=imsmodel
        
        fields=['test',
            'anaesthesia_surgery','anaesthesia_surgery_others','communication_related',
                'communication_others','consent_related','consent_related_others','emergency_related',
                'emergency_related_others','safety_falls_related','safety_falls_related_others',
                'diagnosis_related','diagnosis_related_others','transfusion_related','transfusion_related_others',
                'equipment_related','equipment_related_others','medication_variance','medication_variance_others',
                'misc','misc_others','management_of_care','management_of_care_others',
                'contributing_factors','contributing_factors_others','pt_condition','pt_condition_others',
                'action_taken','action_taken_others','severity_score','severity_score_others',
                'narration','relevant_info','report_to','submission_update_timestamp',
                'submit_confirm_switch'
                ]
    
    
class imsassignform(ModelForm):
    
    assign_comments_qa=forms.CharField(required=False,
                                               widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Comments.....'}),
                                               label='Comments from Quality Department:')
    assign_comments_qa_by=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Staff Name'}),
                                               label='Comments By: ')
    #qa_assign_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1,related_name='assign_to_user')
    #ADD image data
    
    ##hiddenfields
    
    
    
    #assign_qa_comments_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1, related_name='assign_user')
    assign_qa_comments_update_timestamp=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now,
                                                            label='Assignment made on')
    assign_qa_comments_confirm_switch=forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False,
                                                         label="Assignation Confirm")
    
    class Meta:
        model=imsmodel
        fields=['assign_comments_qa','assign_comments_qa_by','qa_assign_to',
                'assign_qa_comments_update_timestamp','assign_qa_comments_confirm_switch' ]
        
        ##giving label for qa_assign_to separately since its coming from meta
        label={'qa_assign_to':'Assign Investigation To: '}
    
class imsinvestigationform(ModelForm):
    investigation_comments_hod=forms.CharField(required=False,
                                               widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Description.....'}),
                                               label='Investigation Description: ')
    investigation_by=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Staff Name'}),
                                               label='Investigation By: ')
    ##ADD IMAGESS
    
    ##hidden fields
    #investigation_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1, related_name='investigator')
    investigation_update_timestamp=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now,
                                                       label='Investigation submitted on')
    investigation_confirm_switch=forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False,
                                                    label='Investigation Submit Confirm')
    
    class Meta:
        model =imsmodel
        fields=['investigation_comments_hod','investigation_by','investigation_update_timestamp',
                'investigation_confirm_switch']

class imsvalidateform(ModelForm):
    
    validation_comments_qa=forms.CharField(required=False,
                                               widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Comments....'}),
                                               label='Validation Description: ')
    validation_final_type=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Communication Error'}),
                                               label='Type of Incident ')
    validation_final_reason=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Lack of proper training'}),
                                               label='Reason for the incident ')
    validation_qa_by=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Staff Name'}),
                                               label='Comments by: ')
    #add images upload
    
    ##hidden fields
    #validation_confirm_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1, related_name='validator')
    validation_confirm_update_timestamp=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now,
                                                       label='Validation done on')
    validation_confirm_switch=forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False,
                                                    label='Validation confirmed on')
    
    class Meta:
        model=imsmodel
        fields=['validation_comments_qa','validation_final_type','validation_final_reason','validation_qa_by',
                'validation_confirm_update_timestamp','validation_confirm_switch']
        
class imsclosureform(ModelForm):
    
    comments_cqo=forms.CharField(required=False,
                                               widget=forms.Textarea(attrs={'class':'form-control','placeholder':'CQO Comments....'}),
                                               label='Comments from CQO ')
    corrective_action=forms.CharField(required=False,max_length=200, 
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Action taken'}),
                                               label='Corrective Action ')

    closure_by=forms.CharField(required=False,
                                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Staff Name'}),
                                               label='Incident Closure Made By: ')
    ##add image data
    
    ##hidden fields
    #closure_confirm_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), default=1,related_name='closure_person')
    closure_update_timestamp=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now,
                                                       label='Closure confirmed on')
    closure_confirm_switch=forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False,
                                                    label='Closure confirmed')
    
    class Meta:
        model=imsmodel
        fields=['comments_cqo','corrective_action','closure_by','closure_update_timestamp','closure_confirm_switch']
    
def file_size(value): # add this to some file where you can import it from
    limit =1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')
    
class imssubmissionfileform(ModelForm):
    file=forms.FileField(label='Submission File', required=False, 
                              widget=forms.ClearableFileInput(attrs={'id':'file'}),validators=[file_size])
    class Meta:
        model=imssubmissionfiles
        fields=['file']     

class imsassignfileform(ModelForm):
    file=forms.FileField(label='Attachment file', required=False,widget=forms.ClearableFileInput(attrs={'id':'file'}),validators=[file_size])
    class Meta:
        model=imsassignfiles
        fields=['file']      

class imsinvestigationfileform(ModelForm):
    file=forms.FileField(label='Investigation File', required=False,widget=forms.ClearableFileInput(attrs={'id':'file'}),validators=[file_size])
    class Meta:
        model=imsinvestigationfiles
        fields=['file']

class imsvalidationfileform(ModelForm):
    file=forms.FileField(label='Validation File', required=False,widget=forms.ClearableFileInput(attrs={'id':'file'}),validators=[file_size])
    class Meta:
        model=imsvalidationfiles
        fields=['file']       
 
class imsclosurefileform(ModelForm):
    file=forms.FileField(label='Closure Files', required=False,widget=forms.ClearableFileInput(attrs={'id':'file'}),validators=[file_size])
    class Meta:
        model=imsclosurefiles
        fields=['file']        

class imsadminlog(models.Model):
    adminname=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='adminname', verbose_name='Admin Name',
                                   to_field='username'       #gives integrity error
                                   )
    
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='access_given_to', verbose_name='Access User',
                                   to_field='username'       #gives integrity error
                                   )
    rightsupdate=models.CharField(max_length=100, null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)


    