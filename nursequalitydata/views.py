from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django import forms
from .models import ReturnToICUForm, IntubationForm, ReintubationForm, PressureInjuryForm, TracheostomyForm, RestraintInjuryForm
from . import views
from .models import ReturnToICU, Intubation , Reintubation, PressureInjury, Tracheostomy, RestraintInjury
from django.contrib import messages
from django.views.generic import View, ListView

# Create your views here.
FormList=['Return_To_ICU', 'Intubation', 'Reintubation', 'Pressure_Injury',
          'Tracheostomy', 'Restraint_Injury']

class Resources:
    ## formdict and formverbose are chained dicts. formname->formsave->form
    
    #link your formverbose name to save button in this dict
    FormVerbose={'Return_To_ICU':'ReturnToICUsave','Intubation':'Intubationsave', 'Reintubation':'Reintubationsave',
                'Pressure_Injury': 'PressureInjurysave','Tracheostomy':'Tracheostomysave',
                 'Restraint_Injury':'RestraintInjurysave',
                }
    ##link your form to save button here
    FormDict={'ReturnToICUsave':[ReturnToICU,ReturnToICUForm],'Intubation':[Intubation,IntubationForm],
             'Reintubationsave':[Reintubation,ReintubationForm],'PressureInjurysave':[PressureInjury,PressureInjuryForm],
             'Tracheostomysave':[Tracheostomy,TracheostomyForm], 'RestraintInjurysave':[RestraintInjury,RestraintInjuryForm],
             }
    
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

def nursequalitydelete(request, pk, formname):
    model,buttonname=Resources.ModelSelector(1, formname)
   #form, buttonname-Resources.FormSelector(1, formname)
    Deletemodel=get_object_or_404(model, pk=pk)
    #Deletemodel.delete()
    
    model, buttonname=Resources.ModelSelector(1, formname)
    
    modellist=model.objects.all().order_by('-timestamp')[:20]
    
    ##adds content to response for hic list
    request.session['formname'] = formname
    
    return HttpResponseRedirect( 'nursequalitylist', {'FormList': FormList, 'modellist':modellist, 'formname':formname}) 

def nursequalityedit(request, pk=0, formname=0 ):
    

    model,buttonname=Resources.ModelSelector(1, formname)

    
    form, buttonname=Resources.FormSelector(1,formname)
    EditModel=get_object_or_404(model, pk=pk)
    EditForm=form(instance=EditModel) 
    return render(request, 'nursequalityforms.html', {'FormList': FormList,'form': EditForm, 
                                             'button':buttonname, 'formname':formname,
                                             'pk':pk})
    
def nursequalitylist(request, pk=0):
    

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

    return render(request, 'nursequalityedit.html', {'FormList': FormList, 'modellist':modellist, 'formname':formname})


class nursequalitydata(View):
    
    def get (self, request, form=None):
        return render(request, 'nursequalityforms.html', {'FormList': FormList,'form': form})
    
    def save(self,request,form,instance=0):
        
        if instance==0:
            form=form(request.POST)
        else:
            form=form(request.POST, instance=instance)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.username=request.user
            instance.save()
            messages.info(request, 'Your form is successfully saved')
            return HttpResponseRedirect('nursequalitydata')
        else:
            print(form.errors)
            messages.info(request, 'Error, Invalid details! Form not saved!')
            return HttpResponseRedirect('nursequalitydata')
        
            
            
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
            return render(request, 'nursequalityforms.html', {'FormList': FormList, 'form': form, 
                                                     'formname':formname, 'button': buttonname })
    

###########################################################################################################################S
# def nursequalitydata(request):
    
#     if request.method=='POST':
#         formname=request.POST['item']
#         form, buttonname=FormSelector(formname)
#         return render (request, 'nursequalityforms.html',
#                     {'FormList': FormList, 'form': form, 'formname':formname, 'button': buttonname})
#     else:
#          return render (request, 'nursequalityforms.html',
#                     {'FormList': FormList})
        
# def FormSelector(formname):
    
#     #creating diffrenet button names for each form, and also assigning forms for each request string of formname
#     #print(formname)
#     if formname=='Return To ICU':
#         form=ReturnToICUForm
#         buttonname='ReturnToICUsave'
#     elif formname=='Intubation Form':
#         form=IntubationForm
#         buttonname='Intubationsave'
#     elif formname=='Reintubation':
#         form=ReintubationForm
#         buttonname='Reintubationsave'
#     elif formname=='Pressure Injury':
#         form=PressureInjuryForm
#         buttonname='PressureInjurysave'
#     elif formname=='Tracheostomy':
#         form=TracheostomyForm
#         buttonname='Tracheostomysave'
#     elif formname=='Restraint Injury':
#         form=RestraintInjuryForm
#         buttonname='RestraintInjurysave'
#     return form, buttonname



# def NQsave(request):
    
#     if request.method=='POST':
        
#         #print(form)
        
#         ##selecting form to save ##checks the button name for right form to save data
        
#         ##ReturnToICUform
#         if request.method=='POST' and 'ReturnToICUsave' in request.POST:
#             form=ReturnToICUForm( request.POST) #calls form content to returntoicu form
#             print('form detected')
#             if form.is_valid(): #validates the form
#                 instance=form.save(commit=False)  #Initializing without commit save
#                 instance.username=request.user   #initializing user id
#                 instance.save()                #complete save of form
                
                
#                 print('forrm saved')

#                 instance.save()
#                 print('instance saved')
#                 messages.info(request, 'Your form is successfully saved')
#                 return HttpResponseRedirect('nursequalitydata')
#                 print('form saved')
#             else:
#                 messages.info(request, "Error, Invalid details! Form Not Saved!")
#                 return HttpResponseRedirect('nursequalitydata')
            
#         ##Intubation form
#         if request.method=='POST' and 'Intubationsave' in request.POST:
#             form=IntubationForm(request.POST)
#             print('form detected')
#             if form.is_valid():
#                 print('FOrm validated')
#                 instance=form.save(commit=False) 
#                 instance.username=request.user
#                 print('form saved')
#                 instance.save()
#                 print('instance saved')
#                 messages.info(request,'Your form is successfully saved')
#                 return HttpResponseRedirect('nursequalitydata')
#             else:
#                 messages.info(request, 'Error, Invalid details! Form Not Saved!')
#                 return HttpResponseRedirect('nursequalitydata')
#             return HttpResponseRedirect('nursequalitydata') 
            
#         ##Reintubation form
#         if request.method=='POST' and 'Reintubationsave' in request.POST:
#             form=ReintubationForm(request.POST)
#             print('form detected')
#             if form.is_valid():
#                 print('FOrm validated')
#                 instance=form.save(commit=False) 
#                 instance.username=request.user
#                 print('form saved')
#                 instance.save()
#                 print('instance saved')
#                 messages.info(request,'Your form is successfully saved')
#                 return HttpResponseRedirect('nursequalitydata')
#             else:
#                 messages.info(request, 'Error, Invalid details! Form Not Saved!')
#                 return HttpResponseRedirect('nursequalitydata')
#             return HttpResponseRedirect('nursequalitydata') 
        
#         ##Pressure Injury form
#         if request.method=='POST' and 'PressureInjurysave' in request.POST:
#             form=PressureInjuryForm(request.POST)
#             print('form detected')
#             if form.is_valid():
#                 print('FOrm validated')
#                 instance=form.save(commit=False) 
#                 instance.username=request.user
#                 print('form saved')
#                 instance.save()
#                 print('instance saved')
#                 messages.info(request,'Your form is successfully saved')
#                 return HttpResponseRedirect('nursequalitydata')
#             else:
#                 messages.info(request, 'Error, Invalid details! Form Not Saved!')
#                 return HttpResponseRedirect('nursequalitydata')
#             return HttpResponseRedirect('nursequalitydata') 
        
#         ##Tracheostomy form
#         if request.method=='POST' and 'Tracheostomysave' in request.POST:
#             form=TracheostomyForm(request.POST)
#             print('form detected')
#             if form.is_valid():
#                 print('FOrm validated')
#                 instance=form.save(commit=False) 
#                 instance.username=request.user
#                 print('form saved')
#                 instance.save()
#                 print('instance saved')
#                 messages.info(request,'Your form is successfully saved')
#                 return HttpResponseRedirect('nursequalitydata')
#             else:
#                 messages.info(request, 'Error, Invalid details! Form Not Saved!')
#                 return HttpResponseRedirect('nursequalitydata')
#             return HttpResponseRedirect('nursequalitydata') 
        
#         ##Restrain Injury
#         if request.method=='POST' and 'RestraintInjurysave' in request.POST:
#             form=RestraintInjuryForm(request.POST)
#             print('form detected')
#             if form.is_valid():
#                 print('FOrm validated')
#                 instance=form.save(commit=False) 
#                 instance.username=request.user
#                 print('form saved')
#                 instance.save()
#                 print('instance saved')
#                 messages.info(request,'Your form is successfully saved')
#                 return HttpResponseRedirect('nursequalitydata')
#             else:
#                 messages.info(request, 'Error, Invalid details! Form Not Saved!')
#                 return HttpResponseRedirect('nursequalitydata')
#             return HttpResponseRedirect('nursequalitydata') 
        
          
            
#     else:
#         print('this is get method')
#         return HttpResponseRedirect('nursequalitydata')