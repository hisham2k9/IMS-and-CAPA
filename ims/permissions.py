from django.contrib.auth.models import User, Group
from .models import imsmodel
from django.shortcuts import render, HttpResponseRedirect,get_object_or_404, redirect

    #EDIT PERMISSIONS
    #if user is validator and switch1 true, switch 2 false, can assign.
    #if user is validator and switch3 true and switch 4 false, can validate.
    
    #if user is closer, can edit, when switch 4 is true, and switch 5 is false....

    
    #if user equal to investigator, can edit if switch 2 is true and switch 3 is false...
    #if user equal to submitter, can edit if switch 1 is false....
    
    #DELETE PERMISSIONS
    ##Delete
    #if user is admin.. can edit, delete all incident...
    #if user is closer, can delete when switch 4 is true 
class permissions():

    def edit_perm(self,request, pk=0):
        
        obj=get_object_or_404(imsmodel,pk=pk)
        switch1=getattr(obj, 'submit_confirm_switch')
        switch2=getattr(obj, 'assign_qa_comments_confirm_switch')
        switch3=getattr(obj, 'investigation_confirm_switch')
        switch4=getattr(obj, 'validation_confirm_switch')
        switch5=getattr(obj, 'closure_confirm_switch')
        investigator=getattr(obj, 'qa_assign_to')
        submitter=getattr(obj, 'submission_confirm_user')
        
        if request.user.groups.filter(name='QA_Validators').exists():
            if switch1==True and switch2==False:
                return True
            elif switch3==True and switch4==False:
                return True
            else:
                return False  
        if request.user.groups.filter(name='Super_Validators').exists():
            if switch4==True and switch5==False:
                return True
            elif switch4==True and switch5==True:
                return True
        
        if request.user==investigator:
            if switch2==True and switch3==False:
                return True
        if request.user==submitter:
            if switch1==False and switch2==False:
                return True
        if request.user.groups.filter(name='admins').exists():
            return True
        else:
            return False

    def delete_perm(self,request, pk=0):
        obj=get_object_or_404(imsmodel,pk=pk)
        switch1=getattr(obj, 'submit_confirm_switch')
        switch2=getattr(obj, 'assign_qa_comments_confirm_switch')
        switch3=getattr(obj, 'investigation_confirm_switch')
        switch4=getattr(obj, 'validation_confirm_switch')
        switch5=getattr(obj, 'closure_confirm_switch')
        investigator=getattr(obj, 'qa_assign_to')
        submitter=getattr(obj, 'submission_confirm_user')
        
        if request.user.groups.filter(name='admins').exists():
            return True
        if request.user.groups.filter(name='Super_Validators').exists():
            if switch4==True:
                return True
            
        if request.user==submitter:
            if switch1==False and switch2==False:
                return True
        

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.info(request, 'Access denied')
                return HttpResponseRedirect('imshome')
        return wrapper_func
    return decorator
            
            
    
    
    
    
    