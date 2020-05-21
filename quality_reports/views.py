from django.shortcuts import render
from . import models
from hicdata import models
from nursequalitydata import models
from accounts import models
import hicdata
import nursequalitydata
import datetime
from hicdata import views
from nursequalitydata import views
from accounts.models import Locations
from django.views import View 
from quality_reports.tables import CAUTITable,AntibioticTable,CLABSITable,BodyFluidExposureTable,VAPTable
from quality_reports.tables import VAETable, SSITable,ThrombophlebitisTable,NSITable
from quality_reports.tables import ReturnToICUTable,IntubationTable,ReintubationTable,PressureInjuryTable
from quality_reports.tables import TracheostomyTable,RestraintInjuryTable
#####################################################################################

# tablelist=[CAUTITable,AntibioticTable,CLABSITable,BodyFluidExposureTable,VAPTable,
#            VAETable,SSITable,ThrombophlebitisTable,NSITable, ReturnToICUTable,IntubationTable, 
#            ReintubationTable,PressureInjuryTable,TracheostomyTable,RestraintInjuryTable]

# #print(tablelist)

# modellist=[hicdata.models.CAUTI,hicdata.models.Antibiotic,hicdata.models.CLABSI,hicdata.models.BodyFluidExposure,
#            hicdata.models.VAP,hicdata.models.VAE,hicdata.models.SSI,hicdata.models.Thrombophlebitis,
#            hicdata.models.NSI, nursequalitydata.models.ReturnToICU,nursequalitydata.models.Intubation, 
#            nursequalitydata.models.Reintubation,nursequalitydata.models.PressureInjury,
#            nursequalitydata.models.Tracheostomy,nursequalitydata.models.RestraintInjury]

##Making a globally available list of items in select tab of report
QA_ReportList=hicdata.views.FormList+nursequalitydata.views.FormList

##Making a globally available list of items in select tab of report
LocationList=Locations.objects.all()


# ##linking report(table) and list item into a dictionary
# Report_Dict={}
# for count, item in enumerate(QA_ReportList):

#     Report_Dict[item]=tablelist[count]
    
    
# ##linking model and list items into a dictionary
# Model_Dict={}
# for count, item in enumerate(QA_ReportList):
#     Model_Dict[item]=modellist[count]
    
# #print(Model_Dict)

## check the order of linking is right, to get right report
#print('Report_Dict',Report_Dict)

# Create your views here.
class qa_reports(View):
    
    def get(self, request):
        ReportType='CAUTI'  #had
        location='Everywhere'
        
        table=CAUTITable(hicdata.models.CAUTI.objects.all())
        return render(request, 'qa_reports.html',{'QA_ReportList':QA_ReportList, 'LocationList': LocationList, 'table': table,
                                                  'ReportType':ReportType, 'location':location})
    
    ##handles post request
    def post(self, request): 
        if request.POST['loc']=='All':        #all or specific 
            if request.POST['item']=='CAUTI':  #checking request
                table=CAUTITable(hicdata.models.CAUTI.objects.all())
                ReportType='CAUTI'
                loc=request.POST['loc']
                
            if request.POST['item']=='Antibiotic Resistance' : 
                table=AntibioticTable(hicdata.models.Antibiotic.objects.all())
                ReportType='Antibiotic Resistance'
                loc=request.POST['loc']
            if request.POST['item']=='CLABSI':
                table=CLABSITable(hicdata.models.CLABSI.objects.all())
                ReportType='CLABSI'
                loc=request.POST['loc']
            if request.POST['item']=='Body Fluid Exposure':
                table=BodyFluidExposureTable(hicdata.models.BodyFluidExposure.objects.all())
                ReportType='Body Fluid Exposure'
                loc=request.POST['loc']
            if request.POST['item']=='VAP':
                table=VAPTable(hicdata.models.VAP.objects.all())
                ReportType='VAP'
                loc=request.POST['loc']
            if request.POST['item']=='VAE':
                table=VAETable(hicdata.models.VAE.objects.all())
                ReportType='VAE'
                loc=request.POST['loc']
            if request.POST['item']=='Surgical Site Infection':
                table=SSITable(hicdata.models.SSI.objects.all())
                ReportType='Surgical Site Infection'
                loc=request.POST['loc']
            if request.POST['item']=='Thrombophlebitis':
                table=ThrombophlebitisTable(hicdata.models.Thrombophlebitis.objects.all())
                ReportType='Thrombophlebitis'
                loc=request.POST['loc']
            if request.POST['item']=='Needle Stick Injury':
                table=NSITable(hicdata.models.NSI.objects.all())
                ReportType='Needle Stick Injury'
                loc=request.POST['loc']
            if request.POST['item']=='Return To ICU':
                table=ReturnToICUTable(nursequalitydata.models.ReturnToICU.objects.all())
                ReportType='Return To ICU'
                loc=request.POST['loc']
            if request.POST['item']=='Intubation':
                table=IntubationTable(nursequalitydata.models.Intubation.objects.all())
                ReportType='Intubation'
                loc=request.POST['loc']
            if request.POST['item']=='Reintubation':
                table=ReintubationTable(nursequalitydata.models.Reintubation.objects.all())
                ReportType='Reintubation'
                loc=request.POST['loc']
            if request.POST['item']=='Pressure Injury':
                table=PressureInjuryTable(nursequalitydata.models.PressureInjury.objects.all())
                ReportType='Pressure Injury'
                loc=request.POST['loc']
            if request.POST['item']=='Tracheostomy':
                table=TracheostomyTable(nursequalitydata.models.Tracheostomy.objects.all())
                ReportType='Tracheostomy'
                loc=request.POST['loc']
            if request.POST['item']=='Restraint Injury':
                table=RestraintInjuryTable(nursequalitydata.models.RestraintInjury.objects.all())
                ReportType='Restraint Injury'
                loc=request.POST['loc']
            
        else:
            if request.POST['item']=='CAUTI':  #checking request
                loc=request.POST['loc']
                table=CAUTITable(hicdata.models.CAUTI.objects.filter(pt_location=loc))
                ReportType='CAUTI'
                
            
            if request.POST['item']=='Antibiotic Resistance' : 
                loc=request.POST['loc']
                table=AntibioticTable(hicdata.models.Antibiotic.objects.filter(pt_location=loc))
                ReportType='Antibiotic Resistance'
                
            if request.POST['item']=='CLABSI':
                loc=request.POST['loc']
                table=CLABSITable(hicdata.models.CLABSI.objects.filter(pt_location=loc))
                ReportType='CLABSI'
                
            if request.POST['item']=='Body Fluid Exposure':
                loc=request.POST['loc']
                table=BodyFluidExposureTable(hicdata.models.BodyFluidExposure.objects.filter(incident_location=loc))
                ReportType='Body Fluid Exposure'
                
            if request.POST['item']=='VAP':
                loc=request.POST['loc']
                table=VAPTable(hicdata.models.VAP.objects.filter(pt_location=loc))
                ReportType='VAP'
                
            if request.POST['item']=='VAE':
                loc=request.POST['loc']
                table=VAETable(hicdata.models.VAE.objects.filter(pt_location=loc))
                ReportType='VAE'
                
            if request.POST['item']=='Surgical Site Infection':
                loc=request.POST['loc']
                table=SSITable(hicdata.models.SSI.objects.filter(pt_location=loc))
                ReportType='Surgical Site Infection'
                
            if request.POST['item']=='Thrombophlebitis':
                loc=request.POST['loc']
                table=ThrombophlebitisTable(hicdata.models.Thrombophlebitis.objects.filter(pt_location=loc))
                ReportType='Thrombophlebitis'
                
            if request.POST['item']=='Needle Stick Injury':
                loc=request.POST['loc']
                table=NSITable(hicdata.models.NSI.objects.filter(staff_location=loc))
                ReportType='Needle Stick Injury'
                
            if request.POST['item']=='Return To ICU':
                loc=request.POST['loc']
                table=ReturnToICUTable(nursequalitydata.models.ReturnToICU.objects.filter(pt_location=loc))
                ReportType='Return To ICU'
                
            if request.POST['item']=='Intubation':
                loc=request.POST['loc']
                table=IntubationTable(nursequalitydata.models.Intubation.objects.filter(pt_location=loc))
                ReportType='Intubation'
                
            if request.POST['item']=='Reintubation':
                loc=request.POST['loc']
                table=ReintubationTable(nursequalitydata.models.Reintubation.objects.filter(pt_location=loc))
                ReportType='Reintubation'
                
            if request.POST['item']=='Pressure Injury':
                loc=request.POST['loc']
                table=PressureInjuryTable(nursequalitydata.models.PressureInjury.objects.filter(pt_location=loc))
                ReportType='Pressure Injury'
                
            if request.POST['item']=='Tracheostomy':
                loc=request.POST['loc']
                table=TracheostomyTable(nursequalitydata.models.Tracheostomy.objects.filter(pt_location=loc))
                ReportType='Tracheostomy'
                
            if request.POST['item']=='Restraint Injury':
                loc=request.POST['loc']
                table=RestraintInjuryTable(nursequalitydata.models.RestraintInjury.objects.filter(pt_location=loc))
                ReportType='Restraint Injury'
                    
                    

        return render(request, 'qa_reports.html',
                        {'QA_ReportList':QA_ReportList, 'LocationList': LocationList, 'table': table, 
                        'ReportType':ReportType, 'location':request.POST['loc']})