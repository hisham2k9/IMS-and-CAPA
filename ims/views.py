from django.shortcuts import render, HttpResponseRedirect,get_object_or_404, redirect
from django import forms
from .models import imsmodel
from .models import imssubmissionform,imssubmissiondetailsform,imsassignform,imsinvestigationform,imsvalidateform, imsclosureform
from django.contrib import messages
from django.views.generic import View, ListView
import datetime
from .permissions import permissions
from .chartdata import chartdata
from django.forms import modelformset_factory #for images formfactory
from django.template import RequestContext
from .models import imssubmissionfiles,imsassignfiles,imsinvestigationfiles, imsvalidationfiles,imsclosurefiles,imsadminlog
from .models import imssubmissionfileform, imsassignfileform, imsinvestigationfileform, imsvalidationfileform, imsclosurefileform
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, F,ExpressionWrapper, DateField, Avg
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .permissions import allowed_users
# Create your views here.

class resources:
    
    def editornew(request):
        FileFormSet = modelformset_factory(imssubmissionfiles,form=imssubmissionfileform,  max_num=3,extra=3)
        if 'primkey' in request.POST:
            pk=request.POST['primkey']
            instance=get_object_or_404(imsmodel, pk=pk)
            form=imssubmissionform(request.POST, instance=instance)
            formset = FileFormSet(request.POST, request.FILES,
                                queryset=imssubmissionfiles.objects.filter(post=pk))
        else:    
            form=imssubmissionform(request.POST)
            formset = FileFormSet(request.POST, request.FILES,
                                queryset=imssubmissionfiles.objects.none())
        return form,formset
    
    def validateformset(formset, model, instance):
        if formset.is_valid:
            for form in formset:
                if form.is_valid():
                    
                    form=form.cleaned_data
                    print('test')
                    if 'file' in form:
                        file=form['file']
                        file=model(post=instance, file=file, date=datetime.datetime.now())
                        file.save()
            if model.objects.filter(post=instance).count()>3:
                to_keep=model.objects.filter(post=instance).order_by('-date')[:3]
                model.objects.filter(post=instance).exclude(pk__in=to_keep).delete()
            return True
        else:
            return False
    
    ##this function returns correct form for imsedit get request
    def formfinder(request,pk=0):
        context={}
        #finding assign obj from pk
        obj=get_object_or_404(imsmodel, pk=pk)
        
        #assigning switches for finding form
        switch1=getattr(obj, 'submit_confirm_switch')
        switch2=getattr(obj, 'assign_qa_comments_confirm_switch')
        switch3=getattr(obj, 'investigation_confirm_switch')
        switch4=getattr(obj, 'validation_confirm_switch')
        switch5=getattr(obj, 'closure_confirm_switch')
        
        #checking stage from switches to find from
        if switch1==False and switch2==False:
            ptform=imssubmissionform(instance=obj)
            detailform=imssubmissiondetailsform(instance=obj)
            FileFormSet = modelformset_factory(imssubmissionfiles,form=imssubmissionfileform,extra=3, max_num=3)
            formset = FileFormSet(queryset=imssubmissionfiles.objects.filter(post=pk))
            context['ptform']=ptform
            context['detailform']=detailform
            context['formset']=formset
            context['pk']=pk
            
            template='ims/imssubmission.html'
            
        if switch1==True and switch2==False:
            assignform=imsassignform(instance=obj)
            pt_ViewForm=imssubmissionform(instance=obj)
            detail_ViewForm=imssubmissiondetailsform(instance=obj)
            subfiles=imssubmissionfiles.objects.filter(post=obj)
            
            #adding previous data to formset
            context['formname']='Assignation Form'
            context['pt_Viewform']=pt_ViewForm
            context['detail_Viewform']=detail_ViewForm
            context['subfiles']=subfiles
            
            #adding new forms
            FileFormSet = modelformset_factory(imsassignfiles,
                                        form=imsassignfileform, max_num=3,extra=3)
            formset = FileFormSet(queryset=imsassignfiles.objects.filter(post=pk))
            context['assignform']=assignform
            context['formset']=formset
            context['pk']=pk
            template='ims/imsassign.html'
            
            
        elif switch2==True and switch3==False:
            #provide investigation form here...
            pt_ViewForm=imssubmissionform(instance=obj)
            detail_ViewForm=imssubmissiondetailsform(instance=obj)
            assign_ViewForm=imsassignform(instance=obj)
            investigation_form=imsinvestigationform(instance=obj)
            subfiles=imssubmissionfiles.objects.filter(post=obj)
            assfiles=imsassignfiles.objects.filter(post=obj)
            
            #adding previous context
            context['formname']='Investigation Form'
            context['pt_Viewform']=pt_ViewForm
            context['detail_Viewform']=detail_ViewForm
            context['assign_Viewform']=assign_ViewForm
            context['subfiles']=subfiles
            context['assfiles']=assfiles
            
            ##adding new files
            FileFormSet = modelformset_factory(imsinvestigationfiles,
                                        form=imsinvestigationfileform, max_num=3,extra=3)
            formset = FileFormSet(queryset=imsinvestigationfiles.objects.filter(post=pk))
            
            context['investigation_form']=investigation_form
            context['formset']=formset
            context['pk']=pk
            template='ims/imsinvestigation.html'
            
        elif switch3==True and switch4==False:
            #provide validation form here
            pt_ViewForm=imssubmissionform(instance=obj)
            detail_ViewForm=imssubmissiondetailsform(instance=obj)
            assign_ViewForm=imsassignform(instance=obj)
            investigation_form=imsinvestigationform(instance=obj)
            validation_form=imsvalidateform(instance=obj)
            subfiles=imssubmissionfiles.objects.filter(post=obj)
            assfiles=imsassignfiles.objects.filter(post=obj)
            invfiles=imsinvestigationfiles.objects.filter(post=obj)
            
            #add previous content
            context['formname']='Validation Form'
            context['pt_Viewform']=pt_ViewForm
            context['detail_Viewform']=detail_ViewForm
            context['assign_Viewform']=assign_ViewForm
            context['investigation_form']=investigation_form
            context['subfiles']=subfiles
            context['assfiles']=assfiles
            context['invfiles']=invfiles
            
            ##adding new files
            FileFormSet = modelformset_factory(imsvalidationfiles,
                                        form=imsvalidationfileform,  max_num=3,extra=3)
            formset = FileFormSet(queryset=imsvalidationfiles.objects.filter(post=pk))
            
            context['validation_form']=validation_form
            context['formset']=formset
            context['pk']=pk
            template='ims/imsvalidation.html'
            pass
        elif switch4==True and switch5==False:
            #provide closure form here
            pt_ViewForm=imssubmissionform(instance=obj)
            detail_ViewForm=imssubmissiondetailsform(instance=obj)
            assign_ViewForm=imsassignform(instance=obj)
            investigation_form=imsinvestigationform(instance=obj)
            validation_form=imsvalidateform(instance=obj)
            closure_form=imsclosureform(instance=obj)
            subfiles=imssubmissionfiles.objects.filter(post=obj)
            assfiles=imsassignfiles.objects.filter(post=obj)
            invfiles=imsinvestigationfiles.objects.filter(post=obj)
            valfiles=imsvalidationfiles.objects.filter(post=obj)
            
            #adding previous context
            context['formname']='Closure Form'
            context['pt_Viewform']=pt_ViewForm
            context['detail_Viewform']=detail_ViewForm
            context['assign_Viewform']=assign_ViewForm
            context['investigation_form']=investigation_form
            context['validation_form']=validation_form
            context['subfiles']=subfiles
            context['assfiles']=assfiles
            context['invfiles']=invfiles
            context['valfiles']=valfiles
            
            ##adding new files
            FileFormSet = modelformset_factory(imsclosurefiles,
                                        form=imsclosurefileform,  max_num=3,extra=3)
            formset = FileFormSet(queryset=imsclosurefiles.objects.filter(post=pk))
            
            context['closure_form']=closure_form
            context['formset']=formset
            context['pk']=pk
            template='ims/imsclosure.html'
            
        elif switch4==True and switch5==True:
            #provide closure form here
            pt_ViewForm=imssubmissionform(instance=obj)
            detail_ViewForm=imssubmissiondetailsform(instance=obj)
            assign_ViewForm=imsassignform(instance=obj)
            investigation_form=imsinvestigationform(instance=obj)
            validation_form=imsvalidateform(instance=obj)
            closure_form=imsclosureform(instance=obj)
            subfiles=imssubmissionfiles.objects.filter(post=obj)
            assfiles=imsassignfiles.objects.filter(post=obj)
            invfiles=imsinvestigationfiles.objects.filter(post=obj)
            valfiles=imsvalidationfiles.objects.filter(post=obj)
            clofiles=imsclosurefiles.objects.filter(post=obj)
            
            context['formname']='Closure Form'
            context['pt_Viewform']=pt_ViewForm
            context['detail_Viewform']=detail_ViewForm
            context['assign_Viewform']=assign_ViewForm
            context['investigation_form']=investigation_form
            context['validation_form']=validation_form
            context['subfiles']=subfiles
            context['assfiles']=assfiles
            context['invfiles']=invfiles
            context['valfiles']=valfiles
            
            FileFormSet = modelformset_factory(imsclosurefiles,
                                        form=imsclosurefileform,  max_num=3,extra=3)
            formset = FileFormSet(queryset=imsclosurefiles.objects.filter(post=pk))
            context['closure_form']=closure_form
            context['formset']=formset
            context['clofiles']=clofiles
            
            context['pk']=pk
            template='ims/imsclosure.html'
        
        return context, template
    
    #post request of all edit gets handled in following 4 methods
    def imsclosuremethod(closure_form,formset, request):
        pk=request.POST['primkey']
        if 'submission' in request.POST:
            
            if closure_form.is_valid() and formset.is_valid():
                closure_instance=closure_form.save(commit=False)
                closure_instance.closure_confirm_switch=True
                closure_instance.closure_confirm_user=request.user
                closure_instance.closure_update_timestamp=datetime.datetime.now()
                closure_instance.save()
                validate=resources.validateformset(formset, imsclosurefiles, closure_instance)
                messages.info(request,'Your form is successfully submitted')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
                        
        else:      #handles reject
            if closure_form.is_valid()and formset.is_valid():
                closure_instance=closure_form.save(commit=False)
                closure_instance.validation_confirm_switch=False
                closure_instance.closure_confirm_switch=False
                closure_instance.closure_confirm_user=request.user
                closure_instance.closure_update_timestamp=datetime.datetime.now()
                closure_instance.save()
                validate=resources.validateformset(formset, imsclosurefiles, closure_instance)
                messages.info(request,'Your form is successfully turned down')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
                
        return HttpResponseRedirect('imsview')
            
    def imsvalidationmethod(validation_form,formset, request):
        pk=request.POST['primkey']
        if 'submission' in request.POST:
            
            if validation_form.is_valid() and formset.is_valid():
                validation_instance=validation_form.save(commit=False)
                validation_instance.validation_confirm_switch=True
                validation_instance.validation_confirm_user=request.user
                validation_instance.validation_confirm_update_timestamp=datetime.datetime.now()
                validation_instance.save()
                validate=resources.validateformset(formset, imsvalidationfiles, validation_instance)
                messages.info(request,'Your form is successfully submitted')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
        
        else:      #handles reject
            if validation_form.is_valid() and formset.is_valid():
                validation_instance=validation_form.save(commit=False)
                validation_instance.validation_confirm_switch=False
                validation_instance.investigation_confirm_switch=False
                validation_instance.validation_confirm_user=request.user
                validation_instance.validation_confirm_update_timestamp=datetime.datetime.now()
                validation_instance.save()
                validate=resources.validateformset(formset, imsvalidationfiles, validation_instance)
                messages.info(request,'Your form is successfully turned down')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
        return HttpResponseRedirect('imsview')
    
    def imsinvestigationmethod(investigation_form,formset, request):
        pk=request.POST['primkey']
        if 'submission' in request.POST:
            if investigation_form.is_valid() and formset.is_valid():
                investigation_instance=investigation_form.save(commit=False)
                investigation_instance.investigation_confirm_switch=True
                investigation_instance.investigation_user=request.user
                investigation_instance.investigation_update_timestamp=datetime.datetime.now()
                investigation_instance.save()
                validate=resources.validateformset(formset, imsinvestigationfiles, investigation_instance)
                messages.info(request,'Your form is successfully submitted')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
        else:      #handles reject
            if investigation_form.is_valid() and formset.is_valid():
                investigation_instance=investigation_form.save(commit=False)
                investigation_instance.assign_qa_comments_confirm_switch=False
                investigation_instance.investigation_confirm_switch=False
                investigation_instance.investigation_user=request.user
                investigation_instance.investigation_update_timestamp=datetime.datetime.now()
                investigation_instance.save()
                validate=resources.validateformset(formset, imsinvestigationfiles, investigation_instance)
                messages.info(request,"Investigation request turned down successfully")  
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
        
        return HttpResponseRedirect('imsview')
    
    ##end of method##############################################
            
    def imsassignmethod(assignform,formset, request):
        pk=request.POST['primkey']
        if 'submission' in request.POST: 
            if assignform.is_valid() and formset.is_valid():
                assign_instance=assignform.save(commit=False)
                assign_instance.assign_qa_comments_confirm_switch=True
                assign_instance.assign_qa_comments_user=request.user
                assign_instance.assign_qa_comments_update_timestamp=datetime.datetime.now()
                assign_instance.save()
                validate=resources.validateformset(formset, imsassignfiles, assign_instance)
                messages.info(request,'Your form is successfully submitted')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
            
        
        else:      #handles reject
            if assignform.is_valid() and formset.is_valid():
                assign_instance=assignform.save(commit=False)
                assign_instance.assign_qa_comments_confirm_switch=False
                assign_instance.submit_confirm_switch=False
                assign_instance.assign_qa_comments_user=request.user
                assign_instance.assign_qa_comments_update_timestamp=datetime.datetime.now()
                assign_instance.save()
                context=resources.imslistcontext(request)
                validate=resources.validateformset(formset, imsassignfiles, assign_instance)
                messages.info(request, 'incident rejected')
            else:
                messages.info(request, 'Upload size too big!')
                return redirect('imsedit',pk=pk )
        return HttpResponseRedirect('imsview')
    
    #context of index view of ims app is generated here....
    def imslistcontext(request,**kwargs):
        context={}
        if 'max' in kwargs.keys():
            max=kwargs['max']
        else:
            max=50
        context['modellist']=imsmodel.objects.all().order_by('-datetime_creation')[:max]
        querystatus=resources.get_progress(request, context['modellist'])
        context['querystatus']=querystatus
        
        count_raised=imsmodel.objects.filter(submit_confirm_switch=True).filter(
        datetime_creation__date__lte=datetime.datetime.today(),
        datetime_creation__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).count()
        count_closed=imsmodel.objects.filter(closure_confirm_switch=True).filter(
        datetime_creation__date__lte=datetime.datetime.today(),
        datetime_creation__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).count()
        count_progress=imsmodel.objects.filter(submit_confirm_switch=True).filter(closure_confirm_switch=False).filter(
        datetime_creation__date__lte=datetime.datetime.today(),
        datetime_creation__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)).count()
        context['count_raised']=count_raised
        context['count_closed']=count_closed
        context['count_progress']=count_progress
        
        return context
    
    
    #progress column of index table algorithm comes from this method
    def get_progress(request,mobjects):
        # function takes in queryset , assigns progress to a list, and zips the qs and list and returns zipped data
        status=[]  ##for getting a llist of model of staus updates
        editlist=[]
        deletelist=[]
        for l in mobjects:
            if l.submit_confirm_switch==True:
                if l.assign_qa_comments_confirm_switch==True:
                    if l.investigation_confirm_switch==True:
                        if l.validation_confirm_switch==True:
                            if l.closure_confirm_switch==True:
                                status.append('Incident Closed')
                            else:
                                status.append('Investigation Validated')
                        else:
                            status.append('Incident Investigated')
                    else:
                        status.append('Under Investigation')
                else:
                    status.append('Incident Submitted')
            else:
                status.append('Incident Saved')
        
            EditPermission=permissions.edit_perm(1, request, pk=l.pk) 
            editlist.append(EditPermission)
            
            DeletePermission=permissions.delete_perm(1, request, pk=l.pk)
            deletelist.append(DeletePermission)   
            
            ##end of loop
                    
        querystatus=zip(status, mobjects, editlist, deletelist)
        
        return querystatus

    def datename(qs):
        #this methods converts any value in qs to str month , or if timedelta, then into intdays
        
        monthname={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',7:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        dic={} #dict
        ls=[] #initial tolist conversion
        for items in qs:
            for value in items.values():
                if type(value)==datetime.datetime:
                    k=value.strftime("%b %y")
                    ls.append(k)
                elif type(value)==datetime.timedelta:
                    v=value.days
                    ls.append(v)
                else:
                    v=value
                    ls.append(v)
            dic={ls[i]:ls[i+1] for i in range(0, len(ls),2)}
        return dic

def imsarchive(request):
    
    context={}
    context=resources.imslistcontext(request)
    
    if request.method=='POST':
        print(request.POST)
        fromdate=request.POST['FromDate']
        todate=request.POST['ToDate']
        todate = datetime.datetime.strptime(todate, '%Y-%m-%d').date() ##converting str date to datetime object
        fromdate = datetime.datetime.strptime(fromdate, '%Y-%m-%d').date()
        difference=todate-fromdate  #createing timedelta object for difference
        
        context['modellist']=imsmodel.objects.all().filter(datetime_creation__date__lte=todate,
                                                                            datetime_creation__date__gt=todate-difference)
        
        template='ims/imsarchive.html'
        return render(request, template, context)
    
    if request.method=='GET':
        template='ims/imsarchive.html'
        return render(request, template, context)


@allowed_users(allowed_roles=['Super_Validators','admins'])
def imsadmin(request):
    
    
    #assign group to variables
    validatorgroup=Group.objects.get(name='QA_Validators')
    supergroup= Group.objects.get(name='Super_Validators')
    
    # validators and admin lists
    validators=User.objects.filter(groups__name='QA_Validators')
    admins=User.objects.filter(groups__name='Super_Validators')
    userlist=User.objects.all()
    loglist=imsadminlog.objects.order_by('-timestamp').all()[:10]
    
    context={}
    
    context['userlist']=userlist
    context['validators']=validators
    context['admins']=admins
    context['loglist']=loglist
    if request.method=='POST':
        #getting username string from post request
        givenusername=request.POST['user']
        #geting user object from usermodel
        userobj=User.objects.get(username=givenusername)
        admintext='Quality Admin, Closure'
        validtext='Validate and Assign'
        
        #adding assignments
        if 'QA_Validators' in request.POST:
            if 'Super_Validators' in request.POST:
                #adding user to group
                validatorgroup.user_set.add(userobj)
                supergroup.user_set.add(userobj)
                updatetext=admintext + ' , ' + validtext
            else:
                validatorgroup.user_set.add(userobj)
                supergroup.user_set.remove(userobj)
                updatetext=validtext
        elif 'Super_Validators' in request.POST:
            supergroup.user_set.add(userobj)
            validatorgroup.user_set.remove(userobj) 
            updatetext=admintext
        else:
            supergroup.user_set.remove(userobj)
            validatorgroup.user_set.remove(userobj) 
            updatetext='nil'
            
        
        #writing changes to logfile
        log=imsadminlog.objects.create(adminname=request.user,
                                    username=userobj,
                                    rightsupdate=updatetext,
                                    timestamp=datetime.datetime.now())
          
    template='ims/imsadmin.html'
    return render(request, template, context)  
    
def imshome(request):
    #all the context for home view created here
    context=resources.imslistcontext(request, max=10) #gets three counts for dashboard
    
    #raised line and closedline gets qs for linechart
    raisedline=imsmodel.objects.order_by('datetime_creation').filter(datetime_creation__date__lte=datetime.datetime.today(),
                                        datetime_creation__date__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                        ).annotate(month=TruncMonth('datetime_creation')
                                                   ).values('month').annotate(c=Count('pt_id')).values('month','c')
    
    closedline=imsmodel.objects.order_by('closure_update_timestamp').filter(closure_confirm_switch=True).filter(closure_update_timestamp__date__lte=datetime.datetime.today(),
                                        closure_update_timestamp__date__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                        ).annotate(month=TruncMonth('closure_update_timestamp')
                                                   ).values('month').annotate(c=Count('pt_id')).values('month','c')
    
    
    #tat per month.
    tatdata=imsmodel.objects.order_by('closure_update_timestamp').filter(closure_confirm_switch=True).filter(closure_update_timestamp__date__lte=datetime.datetime.today(),
                                        closure_update_timestamp__date__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                        ).annotate(datediff=ExpressionWrapper(F('closure_update_timestamp__date')-F('datetime_creation__date'),output_field=DateField())
                                                                              ).annotate(month=TruncMonth('datetime_creation__date')).annotate(adatediff=Avg('datediff')).values('month','adatediff')
    
    raisedline=resources.datename(raisedline)
    closedline=resources.datename(closedline)
    tatdata=resources.datename(tatdata)
    
    raisedline=chartdata.chartdataorder(raisedline)
    closedline=chartdata.chartdataorder(closedline)
    tatdata=chartdata.chartdataorder(tatdata)
    
    pendingassignment=imsmodel.objects.filter(submit_confirm_switch=True).filter(assign_qa_comments_confirm_switch=False).count()
    pendinginvestigation=imsmodel.objects.filter(assign_qa_comments_confirm_switch=True).filter(investigation_confirm_switch=False).count()
    pendingvalidation=imsmodel.objects.filter(investigation_confirm_switch=True).filter(validation_confirm_switch=False).count()
    pendingclosure=imsmodel.objects.filter(validation_confirm_switch=True).filter(closure_confirm_switch=False).count()
    pendinginvforu=imsmodel.objects.filter(assign_qa_comments_confirm_switch=True).filter(investigation_confirm_switch=False).filter(qa_assign_to=request.user).count()
    
    context['raisedline']=raisedline
    context['closedline']=closedline
    context['tatdata']=tatdata
    context['pendingassignment']=pendingassignment
    context['pendinginvestigation']=pendinginvestigation
    context['pendingvalidation']=pendingvalidation
    context['pendingclosure']=pendingclosure
    context['pendinginvforu']=pendinginvforu
    
    template='ims/imshome.html'
    return render(request, template, context)  
    

def imsedit(request,pk=0):
    #this function handles get and post of edit request of all forms
    
    context={} 
    if request.method=="POST":

        pk=request.POST['primkey']
        #finding assign obj from pk
        instance=get_object_or_404(imsmodel, pk=pk)
        #checks for the unique switch of the form from model to recognise the form
        if 'assign_qa_comments_confirm_switch' in request.POST:
            assignform=imsassignform(request.POST, instance=instance) 
            FileFormSet=modelformset_factory(imsassignfiles,form=imsassignfileform, extra=3)
            formset=FileFormSet(request.POST, request.FILES,queryset=imsassignfiles.objects.filter(post=pk))
            response=resources.imsassignmethod(assignform,formset, request)
            return response
        elif 'investigation_confirm_switch' in request.POST:
            investigation_form=imsinvestigationform(request.POST, instance=instance)
            FileFormSet=modelformset_factory(imsinvestigationfiles,form=imsinvestigationfileform, extra=3)
            formset=FileFormSet(request.POST, request.FILES,queryset=imsinvestigationfiles.objects.filter(post=pk))
            response=resources.imsinvestigationmethod(investigation_form,formset, request)
            return response
        elif 'validation_confirm_switch' in request.POST:
            validation_form=imsvalidateform(request.POST, instance=instance)
            FileFormSet=modelformset_factory(imsvalidationfiles,form=imsvalidationfileform, extra=3)
            formset=FileFormSet(request.POST, request.FILES,queryset=imsvalidationfiles.objects.filter(post=pk))
            response=resources.imsvalidationmethod(validation_form,formset,request)
            return response
        elif 'closure_confirm_switch' in request.POST:
            closure_form=imsclosureform(request.POST, instance=instance)
            FileFormSet=modelformset_factory(imsclosurefiles,form=imsclosurefileform, extra=3)
            formset=FileFormSet(request.POST, request.FILES,queryset=imsclosurefiles.objects.filter(post=pk))
            response=resources.imsclosuremethod(closure_form,formset, request)
            return response
    #uses formfinder method to assign form
    if request.method=="GET":
        context,template=resources.formfinder(request,pk)
        return render(request, template, context)
    
     
    

def imsdelete(request, pk):
    #handles delete of object on request
    context={}
    Deleteobj=get_object_or_404(imsmodel, pk=pk)
    #Deleteobj.delete()
    context['modellist']=imsmodel.objects.all().order_by('-datetime_creation')[:50]
    querystatus=resources.get_progress(request, context['modellist'])
    context['querystatus']=querystatus
    return HttpResponseRedirect( 'imsview',context)

#handles update report view            
class imsdetailview(View):
    
    def get(self, request, pk=0):
        #this method handles view without edits, 
        context={}
        ViewModel=get_object_or_404(imsmodel,pk=pk)
        pt_ViewForm=imssubmissionform(instance=ViewModel)
        detail_ViewForm=imssubmissiondetailsform(instance=ViewModel)
        
        subfiles=imssubmissionfiles.objects.filter(post=pk)
        assfiles=imsassignfiles.objects.filter(post=pk)
        invfiles=imsinvestigationfiles.objects.filter(post=pk)
        valfiles=imsvalidationfiles.objects.filter(post=pk)
        clofiles=imsclosurefiles.objects.filter(post=pk)

        context['pt_Viewform']=pt_ViewForm
        context['detail_Viewform']=detail_ViewForm
        context['subfiles']=subfiles
        
        #for rest of forms check if form is submitted, and then pass it to template
        if ViewModel.assign_qa_comments_confirm_switch==True:
            assign_ViewForm=imsassignform(instance=ViewModel)
            context['assign_Viewform']=assign_ViewForm
            context['assfiles']=assfiles
        
        if ViewModel.investigation_confirm_switch==True:
            investigate_ViewForm=imsinvestigationform(instance=ViewModel)
            context['investigate_Viewform']=investigate_ViewForm
            context['invfiles']=invfiles
            
        if ViewModel.validation_confirm_switch==True:
            validation_ViewForm=imsvalidateform(instance=ViewModel)
            context['validate_Viewform']=validation_ViewForm
            context['valfiles']=valfiles
        
        if ViewModel.closure_confirm_switch==True:
            closure_ViewForm=imsclosureform(instance=ViewModel)
            context['closure_ViewForm']=closure_ViewForm
            context['clofiles']=clofiles
        
        template='ims/imsdetailview.html'
        
        return render(request, template ,context)

class imsview(View):
    
    #this is the main view showing the list of records and create new record (handled by get request)
    #post request handles the file submission and save for submission form from ims model and submission files model

    def get(self,request, _create='nil'):
        context={}
        FileFormSet = modelformset_factory(imssubmissionfiles,form=imssubmissionfileform, max_num=3, extra=3)
        if _create != 'nil':   #if a create request
            ptform=imssubmissionform
            detailform=imssubmissiondetailsform
            formset =FileFormSet(queryset=imssubmissionfiles.objects.none())
            context['ptform']=ptform
            context['detailform']=detailform 
            context['formset']=formset
            template='ims/imssubmission.html'  
        else:
            context=resources.imslistcontext(request)
            template='ims/imslist.html'                
        return render(request, template, context)
    
        
    def post(self, request):
        #assigns request.post to imssubmission form
        ##this logic verifies if saved form has come for edit or new form.
        ptform,formset=resources.editornew(request)
        
        #submit or save
        if 'submission' in request.POST:
            if ptform.is_valid() and formset.is_valid():
                #dealing with pt form
                pt_instance=ptform.save()
                pk=pt_instance.id
                formsetsave=resources.validateformset(formset,imssubmissionfiles , pt_instance)
            else:
                context={}
                detailform=imssubmissiondetailsform(request.POST)
                context['ptform']=ptform
                context['detailform']=detailform 
                context['formset']=formset
                template='ims/imssubmission.html'
                return render(request, template, context) 
                
                
            instance=get_object_or_404(imsmodel, pk=pk)
            detailform=imssubmissiondetailsform(request.POST, instance=instance)
            if detailform.is_valid():   
                detail_instance=detailform.save(commit=False)
                detail_instance.submit_confirm_switch=True
                detail_instance.report_to='quality'
                detail_instance.submission_confirm_user=request.user
                detail_instance.submission_update_timestamp=datetime.datetime.now()
                detail_instance.save()
                messages.info(request, 'Your form is successfully submitted')
            else:
                context={}
                detailform=imssubmissiondetailsform(request.POST)
                context['ptform']=ptform
                context['detailform']=detailform 
                context['formset']=formset
                template='ims/imssubmission.html'
                return render(request, template, context) 
            
           # context=resources.imslistcontext(request)
            return HttpResponseRedirect('imsview')
                
                
        elif 'save' in request.POST:
            if ptform.is_valid() and formset.is_valid():
                pt_instance=ptform.save()
                pk=pt_instance.id
                formsetsave=resources.validateformset(formset,imssubmissionfiles , pt_instance)
            else:
                context={}
                detailform=imssubmissiondetailsform(request.POST)
                context['ptform']=ptform
                context['detailform']=detailform 
                context['formset']=formset
                template='ims/imssubmission.html'
                return render(request, template, context) 
            
            instance=get_object_or_404(imsmodel, pk=pk)
            detailform=imssubmissiondetailsform(request.POST, instance=instance)
            
            if detailform.is_valid():
                detail_instance=detailform.save(commit=False)
                detail_instance.submit_confirm_switch=False
                detail_instance.report_to='quality'
                detail_instance.submission_confirm_user=request.user
                detail_instance.submission_update_timestamp=datetime.datetime.now()
                detail_instance.save()
                messages.info(request,'Your form is saved')
            else:
                context={}
                detailform=imssubmissiondetailsform(request.POST)
                context['ptform']=ptform
                context['detailform']=detailform 
                context['formset']=formset
                template='ims/imssubmission.html'
                return render(request, template, context) 
            
            return HttpResponseRedirect('imsview')
        


                    