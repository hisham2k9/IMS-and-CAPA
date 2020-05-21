from django.db import models
from django.forms import ModelForm
from django import forms
from django.core.exceptions import FieldError
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.forms import DateTimeInput
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime
from multiselectfield import MultiSelectField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

class CustomAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)
        
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class actionplanmodel(models.Model):
    #first step
    datetime_creation=models.DateTimeField(default=datetime.datetime.now, editable=False)
    task_name=models.CharField(max_length=100)
    task_desc=models.TextField(null=True, blank=True)
    task_assigned_by=models.CharField(max_length=100)
    task_assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='actionassign_to_user', verbose_name='Assign To',
                                   to_field='username'       #gives integrity error
                                   )
    target_date=models.DateField(default=datetime.date.today)
    
    #hidden field
    task_assign_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='assign_by_user', verbose_name='Assign By   ',
                                   to_field='username'       #gives integrity error
                                   )
    task_assigned_date=models.DateField(default=datetime.date.today)
    task_assign_switch=models.BooleanField(default=False)
    
    #second step+
    status_choices=[('Deferred','Deferred'),('In Progress','In Progress'),('Waiting for Someone','Waiting for Someone')]
     
    status=models.CharField(max_length=50, choices=status_choices)  #default deferred other option: in progress, waiting for someone
    status_desc=models.TextField(null=True, blank=True)
    #hiddenfield
    status_change_datetime=models.DateTimeField(default=datetime.datetime.now)
    status_change_switch=models.BooleanField(default=False)
    status_change_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='statuschanger', verbose_name='Status Changed by',
                                   to_field='username'       #gives integrity error
                                   )
    
    #third step #completion
    completion_desc=models.TextField(null=True, blank=True)
    completion_date=models.DateField(default=datetime.date.today)
    completion_user=models.CharField(max_length=100,null=True, blank=True)
    
    #hiddenfield
    completed_datetimelog=models.DateTimeField(default=datetime.datetime.now)
    completion_switch=models.BooleanField(default=False)
    completion_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='completionusername', verbose_name='Completed by',
                                   to_field='username'       #gives integrity error
                                   )
    #fourthstep
    verified_comments=models.TextField(null=True, blank=True)
    verified_date=models.DateField(default=datetime.date.today)
    
    #hiddenfield
    verified_datetimelog=models.DateTimeField(default=datetime.datetime.now)
    verified_switch=models.BooleanField(default=False)
    verified_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='verifiedusername', verbose_name='Verified by',
                                   to_field='username'       #gives integrity error
                                   )

class actionplancreationform(ModelForm):
    task_name=forms.CharField(required=True,max_length=200, widget=forms.TextInput(attrs={'class':'form-control',
                                                                                        'placeholder':'Task...'})
                            ,label='Action Plan')  #name of person involved
    task_desc=forms.CharField(required=True,max_length=500, widget=forms.Textarea(attrs={'class':'form-control',
                                                                                        'placeholder':'Task Description....'})
                            ,label='Action Plan Details')  #name of person involved
    task_assigned_by=forms.CharField(required=True,max_length=200, widget=forms.TextInput(attrs={'class':'form-control',
                                                                                        'placeholder':'Name...'})
                            ,label='Action Plan Created By:')
    
   # task_assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
   #                                default='admin',related_name='actionassign_to_user', verbose_name='Assign To',
   #                                to_field='username'       #gives integrity error
   #                                )
    
    target_date=forms.DateField(widget=AdminDateWidget())
    
    #hidden field
    task_assign_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
                                   default='admin',related_name='assign_by_user', verbose_name='Assign To',
                                   to_field='username'       #gives integrity error
                                   )
    task_assigned_date=forms.DateField(initial=datetime.date.today, widget=forms.HiddenInput())
    task_assign_switch=forms.BooleanField(required=False, initial=False,widget=forms.HiddenInput())
    
    class Meta:
        model=actionplanmodel
        fields=['task_name','task_assigned_by','task_desc','task_assigned_to','target_date',
                'task_assigned_date','task_assign_switch'
                ]
        
class actionplanstatusform(ModelForm):
     
    status=forms.CharField(required=True,max_length=50, 
                              widget=forms.Select(attrs={'class':'form-control'},choices=actionplanmodel.status_choices),
                              label='Status')
    status_desc=forms.CharField(required=True,max_length=500, widget=forms.Textarea(attrs={'class':'form-control',
                                                                                        'placeholder':'Status Description....'}),
                                                                                    label='Status Description')
    
    #hiddenfield
    status_change_datetime=forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())
    status_change_switch=forms.BooleanField(required=False, initial=False,widget=forms.HiddenInput())
    
    class Meta:
        model = actionplanmodel
        fields=['status','status_desc','status_change_datetime', 'status_change_switch' ]

class actionplancompletionform(ModelForm):
    completion_user=forms.CharField(required=True,max_length=200, widget=forms.TextInput(attrs={'class':'form-control',
                                                                                        'placeholder':'Full name'})
                            ,label='Task Completed by')  #name of person involved
    completion_date=forms.DateField(widget=AdminDateWidget())
    completion_desc=forms.CharField(required=True,max_length=500, widget=forms.Textarea(attrs={'class':'form-control',
                                                                                        'placeholder':'Task Description....'}),
                                                                                    label='Task Completion Description')
    
    #hiddenfield
    completed_datetimelog=forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())
    completion_switch=forms.BooleanField(required=False, initial=False,widget=forms.HiddenInput())
    
    class Meta:
        model=actionplanmodel
        fields=['completion_user','completion_date', 'completion_desc','completed_datetimelog','completion_switch' ]
    # completion_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
    #                                default='admin',related_name='completionusername', verbose_name='Completed by',
    #                                to_field='username'       #gives integrity error
    #                                )
    
class actionplanverificationform(ModelForm):
    
    #fourthstep
    verified_comments=forms.CharField(required=True,max_length=500, widget=forms.Textarea(attrs={'class':'form-control',
                                                                                        'placeholder':'Any comments....'}),
                                                                                    label='Comments')
    verified_date=forms.DateField(widget=AdminDateWidget())
    
    #hiddenfield
    verified_datetimelog=forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())
    verified_switch=forms.BooleanField(required=False, initial=False,widget=forms.HiddenInput())
    # verified_username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user), 
    #                                default='admin',related_name='verifiedusername', verbose_name='Verified by',
    #                                to_field='username'       #gives integrity error
    #                                )
       
    class Meta:
        model=actionplanmodel
        fields=['verified_comments','verified_date','verified_datetimelog','verified_switch']