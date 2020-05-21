from django.contrib.auth.models import User, Group
from .models import actionplanmodel
from django.shortcuts import render, HttpResponseRedirect,get_object_or_404, redirect

class permissions():
    
    def edit_perm(self,request, pk=0):

        obj=get_object_or_404(actionplanmodel,pk=pk)
        switch1=getattr(obj, 'task_assign_switch')
        switch2=getattr(obj, 'status_change_switch')
        switch3=getattr(obj, 'completion_switch')
        switch4=getattr(obj, 'verified_switch')
        taskactor=getattr(obj, 'task_assigned_to')
        taskmaker=getattr(obj, 'task_assign_username')
        
        if request.user==taskmaker:
            if switch1==False and switch2==False:
                return True
        
        if request.user==taskactor:
            if switch2==False and switch3==False:
                return True
            elif switch3==False and switch4==False:
                return True
            else:
                return False
            
        if request.user.groups.filter(name='Super_Validators').exists():
            if switch1==False and switch2==False:
                return True
            elif switch3==True and switch4==False:
                return True
            else:
                return False
        if request.user.groups.filter(name='admins').exists():
            return True
            
    def delete_perm(self,request, pk=0):
        obj=get_object_or_404(actionplanmodel,pk=pk)
        switch1=getattr(obj, 'task_assign_switch')
        switch2=getattr(obj, 'status_change_switch')
        switch3=getattr(obj, 'completion_switch')
        switch4=getattr(obj, 'verified_switch')
        taskactor=getattr(obj, 'task_assigned_to')
        taskmaker=getattr(obj, 'task_assign_username')
        
        if request.user.groups.filter(name='Super_Validators').exists():
            return True
        if request.user.groups.filter(name='admins').exists():
            return True
    
    def create_perm(self,request):
        
        if request.user.groups.filter(name='Super_Validators').exists():
            return True
        if request.user.groups.filter(name='admins').exists():
            return True
        

#edit option

#if task asssigned swith true and user = investigation return true
#if completion is true and user = supervalidator return true
#



        # obj=get_object_or_404(actionplanmodel,pk=pk)
        # switch1=getattr(obj, 'submit_confirm_switch')
        # switch2=getattr(obj, 'assign_qa_comments_confirm_switch')
        # switch3=getattr(obj, 'investigation_confirm_switch')
        # switch4=getattr(obj, 'validation_confirm_switch')
        # switch5=getattr(obj, 'closure_confirm_switch')
        # investigator=getattr(obj, 'qa_assign_to')
        # submitter=getattr(obj, 'submission_confirm_user')
        
        
        
        
        # def post(self, request):
    #     #assigns request.post to imssubmission form
    #     ##this logic verifies if saved form has come for edit or new form.
    #     ptform,formset=resources.editornew(request)
        
    #     #submit or save
    #     if 'submission' in request.POST:
    #         if ptform.is_valid() and formset.is_valid():
    #             #dealing with pt form
    #             pt_instance=ptform.save()
    #             pk=pt_instance.id
    #             formsetsave=resources.validateformset(formset,imssubmissionfiles , pt_instance)
    #         else:
    #             context={}
    #             detailform=imssubmissiondetailsform(request.POST)
    #             context['ptform']=ptform
    #             context['detailform']=detailform 
    #             context['formset']=formset
    #             template='ims/imssubmission.html'
    #             return render(request, template, context) 
                
                
    #         instance=get_object_or_404(imsmodel, pk=pk)
    #         detailform=imssubmissiondetailsform(request.POST, instance=instance)
    #         if detailform.is_valid():   
    #             detail_instance=detailform.save(commit=False)
    #             detail_instance.submit_confirm_switch=True
    #             detail_instance.report_to='quality'
    #             detail_instance.submission_confirm_user=request.user
    #             detail_instance.submission_update_timestamp=datetime.datetime.now()
    #             detail_instance.save()
    #             messages.info(request, 'Your form is successfully submitted')
    #         else:
    #             context={}
    #             detailform=imssubmissiondetailsform(request.POST)
    #             context['ptform']=ptform
    #             context['detailform']=detailform 
    #             context['formset']=formset
    #             template='ims/imssubmission.html'
    #             return render(request, template, context) 
            
    #        # context=resources.imslistcontext(request)
    #         return HttpResponseRedirect('imsview')
                
                
    #     elif 'save' in request.POST:
    #         if ptform.is_valid() and formset.is_valid():
    #             pt_instance=ptform.save()
    #             pk=pt_instance.id
    #             formsetsave=resources.validateformset(formset,imssubmissionfiles , pt_instance)
    #         else:
    #             context={}
    #             detailform=imssubmissiondetailsform(request.POST)
    #             context['ptform']=ptform
    #             context['detailform']=detailform 
    #             context['formset']=formset
    #             template='ims/imssubmission.html'
    #             return render(request, template, context) 
            
    #         instance=get_object_or_404(imsmodel, pk=pk)
    #         detailform=imssubmissiondetailsform(request.POST, instance=instance)
            
    #         if detailform.is_valid():
    #             detail_instance=detailform.save(commit=False)
    #             detail_instance.submit_confirm_switch=False
    #             detail_instance.report_to='quality'
    #             detail_instance.submission_confirm_user=request.user
    #             detail_instance.submission_update_timestamp=datetime.datetime.now()
    #             detail_instance.save()
    #             messages.info(request,'Your form is saved')
    #         else:
    #             context={}
    #             detailform=imssubmissiondetailsform(request.POST)
    #             context['ptform']=ptform
    #             context['detailform']=detailform 
    #             context['formset']=formset
    #             template='ims/imssubmission.html'
    #             return render(request, template, context) 
            
    #         return HttpResponseRedirect('imsview')