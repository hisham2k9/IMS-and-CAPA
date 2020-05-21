from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.views.generic import View, ListView
from .models import actionplanmodel,actionplancreationform,actionplanstatusform, actionplancompletionform,actionplanverificationform
import datetime
from .permissions import permissions
from django.contrib import messages

# Create your views here.
class resources:
    
    def actionplanverificationmethod(verificationform,request):
        context={}
        pk=request.POST['primkey']
        if 'submission' in request.POST: 
            if verificationform.is_valid():
                verification_instance=verificationform.save(commit=False)
                verification_instance.verified_switch=True
                verification_instance.verified_username=request.user
                verification_instance.verified_datetimelog=datetime.datetime.now()
                verification_instance.save()
                messages.info(request,'Your form is successfully submitted')
                return HttpResponseRedirect('actionplanview')
            else:
                print(verificationform.errors)
                obj=get_object_or_404(actionplanmodel, pk=pk)
                creationForm=actionplancreationform(instance=obj)
                statusform=actionplanstatusform(instance=obj)
                completionform=actionplancompletionform(instance=obj)
                verificationform=actionplanverificationform(request.POST)
                
                #adding previous data to formset
                context['formname']='Verification'
                context['creationForm']=creationForm
                context['statusform']=statusform
                context['completionform']=completionform
                context['verificationform']=verificationform
                
                context['pk']=pk
                template='actionplan/actionplanverification.html'
                return render(request, template, context)
        else: #handles reject the action plan
            if verificationform.is_valid():
                verification_instance=verificationform.save(commit=False)
                verification_instance.verified_switch=False
                verification_instance.completion_switch=False
                verification_instance.verified_username=request.user
                verification_instance.verified_datetimelog=datetime.datetime.now()
                verification_instance.save()
                messages.info(request,'Your form is successfully submitted')
                return HttpResponseRedirect('actionplanview')
            else:
                print(verificationform.errors)
                obj=get_object_or_404(actionplanmodel, pk=pk)
                creationForm=actionplancreationform(instance=obj)
                statusform=actionplanstatusform(instance=obj)
                completionform=actionplancompletionform(instance=obj)
                verificationform=actionplanverificationform(request.POST)
                
                #adding previous data to formset
                context['formname']='Verification'
                context['creationForm']=creationForm
                context['statusform']=statusform
                context['completionform']=completionform
                context['verificationform']=verificationform
                
                context['pk']=pk
                template='actionplan/actionplanverification.html'
                return render(request, template, context)
        
    def actionplancompletionmethod(completionform, request):
        context={}
        pk=request.POST['primkey']
        if 'submission' in request.POST: 
            if completionform.is_valid():
                completion_instance=completionform.save(commit=False)
                completion_instance.completion_switch=True
                completion_instance.completion_username=request.user
                completion_instance.completed_datetimelog=datetime.datetime.now()
                completion_instance.save()
                messages.info(request,'Your form is successfully submitted')
                return HttpResponseRedirect('actionplanview')
            else:
                print(completionform.errors)
                obj=get_object_or_404(actionplanmodel, pk=pk)
                creationForm=actionplancreationform(instance=obj)
                statusform=actionplanstatusform(instance=obj)
                completionform=actionplancompletionform(request.POST)
                
                #adding previous data to formset
                context['formname']='Status Update'
                context['creationForm']=creationForm
                context['statusform']=statusform
                context['completionform']=completionform
                
                context['pk']=pk
                template='actionplan/actionplancompletion.html'
                return render(request, template, context)
        else: #handles defer the action plan
            obj=get_object_or_404(actionplanmodel, pk=pk)
            obj.status_change_switch=False
            obj.save()
            messages.info(request,'Your Action Plan successfully deferred')
            return HttpResponseRedirect('actionplanview')
    
    def actionplanstatusmethod(statusform, request):
        context={}
        pk=request.POST['primkey']
        if 'submission' in request.POST: 
            if statusform.is_valid():
                status_instance=statusform.save(commit=False)
                if status_instance.status=='In Progress':
                    status_instance.status_change_switch=True
                else:
                    status_instance.status_change_switch=False 
                status_instance.status_change_username=request.user
                status_instance.status_change_datetime=datetime.datetime.now()
                status_instance.save()
                messages.info(request,'Your form is successfully submitted')
                return HttpResponseRedirect('actionplanview')
            else:
                obj=get_object_or_404(actionplanmodel, pk=pk)
                creationForm=actionplancreationform(instance=obj)
                statusform=actionplanstatusform(request.POST)
                #adding previous data to formset
                context['formname']='Status Update'
                context['statusform']=statusform
                context['creationForm']=creationForm
                context['pk']=pk
                template='actionplan/actionplanstatus.html'
                return render(request, template, context)
    
    def formfinder(request,pk=0):
        context={}
        #finding assign obj from pk
        obj=get_object_or_404(actionplanmodel, pk=pk)
        
        #assigning switches for finding form
        switch1=getattr(obj, 'task_assign_switch')
        switch2=getattr(obj, 'status_change_switch')
        switch3=getattr(obj, 'completion_switch')
        switch4=getattr(obj, 'verified_switch')
        
        #checking stage from switches to find from
        if switch1==False and switch2==False:
            creationform=actionplancreationform(instance=obj)
            context['creationform']=creationform
            context['pk']=pk
            
            template='actionplan/actionplancreation.html'
            
        if switch1==True and switch2==False:
            creationForm=actionplancreationform(instance=obj)
            statusform=actionplanstatusform(instance=obj)
            
            
            #adding previous data to formset
            context['formname']='Status Update'
            context['statusform']=statusform
            context['creationForm']=creationForm
            context['pk']=pk
            template='actionplan/actionplanstatus.html'
            
            
        elif switch2==True and switch3==False:
            #provide completion form here...
            creationForm=actionplancreationform(instance=obj)
            statusform=actionplanstatusform(instance=obj)
            completionform=actionplancompletionform(instance=obj)

            
            #adding previous context
            context['formname']='Completion Details'
            context['creationForm']=creationForm
            context['statusform']=statusform
            context['completionform']=completionform
            context['pk']=pk
            template='actionplan/actionplancompletion.html'
            
        elif switch3==True and switch4==False or True:
            #provide verification form form here
            creationForm=actionplancreationform(instance=obj)
            statusform=actionplanstatusform(instance=obj)
            completionform=actionplancompletionform(instance=obj)
            verificationform=actionplanverificationform(instance=obj)
            
            #add previous content
            context['formname']='Verification'
            context['creationForm']=creationForm
            context['statusform']=statusform
            context['completionform']=completionform
            context['verificationform']=verificationform
            context['pk']=pk
            template='actionplan/actionplanverification.html'
            
        
        return context, template
    
    def editornew(request):
        if 'primkey' in request.POST:
            pk=request.POST['primkey']
            instance=get_object_or_404(actionplanmodel, pk=pk)
            form=actionplancreationform(request.POST, instance=instance)
        else:    
            form=actionplancreationform(request.POST)
        return form
    
    def actionplanlistcontext(request,**kwargs):
        context={}
        if 'max' in kwargs.keys():
            max=kwargs['max']
        else:
            max=50
        context['modellist']=actionplanmodel.objects.all().order_by('-datetime_creation')[:max]
        querystatus=resources.get_progress(request, context['modellist'])
        context['querystatus']=querystatus
        
        count_planned=actionplanmodel.objects.filter(task_assign_switch=True).filter(
        task_assigned_date__lte=datetime.datetime.today(),
        task_assigned_date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).count()
        count_finished=actionplanmodel.objects.filter(verified_switch=True).filter(
        task_assigned_date__lte=datetime.datetime.today(),
        task_assigned_date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).count()
        count_progress=actionplanmodel.objects.filter(task_assign_switch=True).filter(verified_switch=False).filter(
        task_assigned_date__lte=datetime.datetime.today(),
        task_assigned_date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).count()
        context['count_planned']=count_planned
        context['count_finished']=count_finished
        context['count_progress']=count_progress
        
        return context

    #progress column of index table algorithm comes from this method
    def get_progress(request,mobjects):
        # function takes in queryset , assigns progress to a list, and zips the qs and list and returns zipped data
        status=[]  ##for getting a llist of model of staus updates
        editlist=[]
        deletelist=[]
        for l in mobjects:
            if l.task_assign_switch==True:
                if l.status_change_switch==True:
                    if l.completion_switch==True:
                        if l.verified_switch==True:
                            status.append('Completed and Verified')

                        else:
                            status.append('Action Completed')
                    else:
                        #print what is the status update field of model
                        status.append(l.status)
                else:
                    if l.status!= 'In Progress' and l.status !='':
                        status.append(l.status)
                    else: 
                        status.append('Action Plan Assigned')
            else:
                status.append('Action Plan Created')
        
            EditPermission=permissions.edit_perm(1, request, pk=l.pk) 
            editlist.append(EditPermission)
            
            DeletePermission=permissions.delete_perm(1, request, pk=l.pk)
            deletelist.append(DeletePermission)   
            
            ##end of loop
        CreatePermission=permissions.create_perm(1,request)            
        querystatus=zip(status, mobjects, editlist, deletelist)
        
        return querystatus

def actionplanedit(request,pk=0):
    #this function handles get and post of edit request of all forms
    
    context={} 
    if request.method=="POST":

        pk=request.POST['primkey']
        #finding assign obj from pk
        instance=get_object_or_404(actionplanmodel, pk=pk)
        #checks for the unique switch of the form from model to recognise the form
        if 'status_change_switch' in request.POST:
            statusform=actionplanstatusform(request.POST, instance=instance) 
            response=resources.actionplanstatusmethod(statusform,request)
            return response
        elif 'completion_switch' in request.POST:
            completionform=actionplancompletionform(request.POST, instance=instance)
            response=resources.actionplancompletionmethod(completionform, request)
            return response
        elif 'verified_switch' in request.POST:
            verificationform=actionplanverificationform(request.POST, instance=instance)
            response=resources.actionplanverificationmethod(verificationform,request)
            return response
    #uses formfinder method to assign form
    if request.method=="GET":
        context,template=resources.formfinder(request,pk)
        return render(request, template, context)
    

def actionplandelete(request, pk):
    #handles delete of object on request
    context={}
    Deleteobj=get_object_or_404(actionplanmodel, pk=pk)
    #Deleteobj.delete()
    context['modellist']=actionplanmodel.objects.all().order_by('-datetime_creation')[:50]
    querystatus=resources.get_progress(request, context['modellist'])
    context['querystatus']=querystatus
    return HttpResponseRedirect( 'actionplanview',context)

class actionplanview(View):
    
    #this is the main view showing the list of records and create new record (handled by get request)
    #post request handles the file submission and save for submission form from  model and submission files model

    def get(self,request, _create='nil'):
        context={}
        if _create != 'nil':   #if a create request
            creationform=actionplancreationform
            context['creationform']=creationform
            template='actionplan/actionplancreation.html'
        else:
            context=resources.actionplanlistcontext(request)
            template='actionplan/actionplanlist.html'                
        return render(request, template, context)
    
    def post(self, request):
        
        creationform=resources.editornew(request)
        
        if 'submission' in request.POST:
            if creationform.is_valid():
                print('is valid')
                #dealing withform
                actionplan_instance=creationform.save(commit=False)
                actionplan_instance.task_assign_username=request.user
                actionplan_instance.task_assigned_date=datetime.date.today()
                actionplan_instance.task_assign_switch=True
                actionplan_instance.save()
                pk=actionplan_instance.id
                return HttpResponseRedirect('actionplanview')
            else:
    
                print(creationform.errors)
                context={}
                creationform=actionplancreationform(request.POST)
                context['creationform']=creationform
                template='actionplan/actionplancreation.html'
                return render(request, template, context) 
        else:
            if creationform.is_valid():
                print('is valid')
                #dealing withform
                actionplan_instance=creationform.save(commit=False)
                actionplan_instance.task_assign_username=request.user
                actionplan_instance.task_assigned_date=datetime.date.today()
                actionplan_instance.task_assign_switch=False
                actionplan_instance.save()
                pk=actionplan_instance.id
                return HttpResponseRedirect('actionplanview')
            else:
                print('hello notvalid')
                print(creationform.errors)
                context={}
                creationform=actionplancreationform(request.POST)
                context['creationform']=creationform
                template='actionplan/actionplancreation.html'
                return render(request, template, context) 
            
        
    