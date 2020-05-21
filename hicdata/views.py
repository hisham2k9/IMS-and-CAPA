from django.shortcuts import render, HttpResponseRedirect,get_object_or_404, redirect
from django import forms
from .models import CAUTIForm, AntibioticForm,CLABSIForm, BodyFluidExposureForm, VAPForm, VAEForm, SSIForm, ThrombophlebitisForm, NSIForm
from . import views
from .models import CAUTI, Antibiotic,CLABSI, BodyFluidExposure, VAP, VAE, SSI, Thrombophlebitis, NSI
from django.contrib import messages
from django.views.generic import View, ListView

# Create your views here.

##create another panel heading with edit button.
##create let that button take into list view of all the instances of model.
##link each model to its hyper link.
##let the link take to any required instance of model.
##once in the instance, make changes... create request to save back the model.
##once saved take to blank screen with just choices to choose another option, show your form is successfully saved
    
    ## form selector list
FormList=[ 'CAUTI','Antibiotic_Resistance', 'CLABSI', 'Body_Fluid_Exposure',
           'VAP', 'VAE', 'Surigical_Site_Infection', 'Thrombophlebitis',
           'Needle_Stick_Injury'] 

class Resources:
    
    ## formdict and formverbose are chained dicts. formname->formsave->form
    
    #link your formverbose name to save button in this dict
    FormVerbose={'CAUTI':'CAUTIsave','Antibiotic_Resistance':'Antibioticsave', 'CLABSI':'CLABSIsave',
                'Body_Fluid_Exposure': 'BodyFluidExposuresave','VAP':'VAPsave', 'VAE':'VAEsave',
                'Surigical_Site_Infection':'SSIsave', 'Thrombophlebitis':'Thrombophlebitissave',
                'Needle_Stick_Injury':'NSIsave'}
    
    ##link your form to save button here
    FormDict={'CAUTIsave':[CAUTI,CAUTIForm],'Antibioticsave':[Antibiotic,AntibioticForm], 'CLABSIsave':[CLABSI,CLABSIForm],
            'BodyFluidExposuresave':[BodyFluidExposure,BodyFluidExposureForm], 'VAPsave':[VAP,VAPForm], 'VAEsave':[VAE,VAEForm],
            'SSIsave':[SSI,SSIForm], 'Thrombophlebitissave':[Thrombophlebitis,ThrombophlebitisForm], 'NSIsave':[NSI,NSIForm]}
    
    def ModelSelector(self, formname):
        for key, value in Resources.FormVerbose.items():
            #print('formname',formname)
            if formname==key:
                buttonname=value
               # print(buttonname)
        for key, value in Resources.FormDict.items():
            if buttonname==key:
                model = value[0]
        return model, buttonname  
    
    def FormSelector(self, formname):   
    #creating diffrenet button names for each form, and also assigning forms for each request string of formname
        for key, value in Resources.FormVerbose.items():
            if formname==key:
                buttonname=value
        for key, value in Resources.FormDict.items():
            if buttonname==key:
                form = value[1]
        return form, buttonname

def test(request):
    return render(request, 'hicedit.html')

def hicdelete(request, pk, formname):
    model,buttonname=Resources.ModelSelector(1, formname)
   #form, buttonname-Resources.FormSelector(1, formname)
    Deletemodel=get_object_or_404(model, pk=pk)
    Deletemodel.delete()
    
    model, buttonname=Resources.ModelSelector(1, formname)
    
    modellist=model.objects.all().order_by('-timestamp')[:20]
    
    ##adds content to response for hic list
    request.session['formname'] = formname
    
    return HttpResponseRedirect( 'hiclist', {'FormList': FormList, 'modellist':modellist, 'formname':formname})
    
    
 
def hicedit(request, pk=0, formname=0 ):


    model,buttonname=Resources.ModelSelector(1, formname)

    
    form, buttonname=Resources.FormSelector(1,formname)
    EditModel=get_object_or_404(model, pk=pk)
    EditForm=form(instance=EditModel) 
    return render(request, 'hicforms.html', {'FormList': FormList,'form': EditForm, 
                                             'button':buttonname, 'formname':formname,
                                             'pk':pk})

class hiclist(View):
    pass
    

            
            
        
def hiclist(request, pk=0):
    

    if request.method =='GET' and request.session.has_key('formname'): ##checks if the request is coming from hicdelete
        #print('haskey')
        formname=request.session.get('formname') #assigns formname from hicdelete
    
    else:
        formname=request.POST['formname'] #if it is a post request, with request coming from hicdata to edit
    #print(formname)
    x=1
    model, buttonname=Resources.ModelSelector(x, formname)
    modellist=model.objects.all().order_by('-timestamp')[:20]
    #print(modellist)

    return render(request, 'hicedit.html', {'FormList': FormList, 'modellist':modellist, 'formname':formname})
        

class hicdata(View):
    
    def get (self, request, form=None):
        return render(request, 'hicforms.html', {'FormList': FormList,'form': form})
    
    def save(self,request,form,instance=0):
        
        if instance==0:
            form=form(request.POST)
        else:
            form=form(request.POST, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.username=request.user
            print(form.errors)
            instance.save()
            messages.info(request, 'Your form is successfully saved')
            return HttpResponseRedirect('hicdata')
        else:
            print(form.errors)
            messages.info(request, 'Error, Invalid details! Form not saved!')
            return HttpResponseRedirect('hicdata')
        
            
            
            ##use pk to get model object
            ##pass it as instance to form and then save
            
            pass
        
    def post(self,request):
        
        for k, v in Resources.FormDict.items():
            if k in request.POST:
                form=v[1]
                model=v[0]
                
                
        if 'item' not in request.POST:
            #print(request.POST)
            if 'primkey' in request.POST:
                pk=request.POST['primkey']
                instance=get_object_or_404(model, pk=pk)
                response=self.save(request,form, instance)
                return response
            else:
                response=self.save(request,form)
                return response
                
        else:
            formname=request.POST['item']
            form, buttonname=Resources.FormSelector(self, formname)
            return render(request, 'hicforms.html', {'FormList': FormList, 'form': form, 
                                                     'formname':formname, 'button': buttonname })
    





##################################################################################################################
#######################OLD FUNCTION BASED VIEWS###################################################################
##################################################################################################################

