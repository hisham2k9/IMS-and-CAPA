from django.shortcuts import render
from . import models
from hicdata import models
from nursequalitydata import models
from accounts import models
import hicdata
import nursequalitydata
import datetime

# Create your views here.

def quality(request):
    
    ##location list derived from query.
    LocationList=models.Locations.objects.all()
    
    ## Textlist and count Dictionary for loop in template
    ContentDict={}
    
    if request.method=='POST':
        ContentDict={}
        fromdate=request.POST['FromDate']
        loc=request.POST['locname']
        todate=request.POST['ToDate']
        
        
        Header='You are seeing data of %s from %s to %s'%(loc, fromdate, todate)
        print(todate)
        todate = datetime.datetime.strptime(todate, '%Y-%m-%d').date() ##converting str date to datetime object
        fromdate = datetime.datetime.strptime(fromdate, '%Y-%m-%d').date()
        difference=todate-fromdate  #createing timedelta object for difference
       
        if loc!='All':             ##makes filter for location as well
            ##Text and count of Tracheostomy
            TracheostomyText='Tracheostomy Cases'
            Tracheostomycount=len(nursequalitydata.models.Tracheostomy.objects.filter(datetime_tracheostomy__date__lte=todate,
                                                                            datetime_tracheostomy__date__gt=todate-difference).
                                filter(pt_location=loc))
            
            ContentDict[TracheostomyText]=Tracheostomycount 
            
            ##Text and count of Pressure Sore Injury
            PressureInjuryText='Pressure Sore Injury'
            PressureInjurycount=len(nursequalitydata.models.PressureInjury.objects.filter(dateofobservation__lte=todate,
                                                                            dateofobservation__gt=todate-difference).
                                filter(pt_location=loc))
            
            ContentDict[PressureInjuryText]=PressureInjurycount 
            
            
            ##Text and count of Reintubation
            ReintubationText='Reintubation Cases'
            Reintubationcount=len(nursequalitydata.models.Reintubation.objects.filter(datetime_reintubation__date__lte=todate,
                                                                            datetime_reintubation__date__gt=todate-difference).
                                filter(pt_location=loc))
            
            ContentDict[ReintubationText]=Reintubationcount 
            
            ##Text and count of Intubation
            IntubationText='Intubation Cases'
            Intubationcount=len(nursequalitydata.models.Intubation.objects.filter(datetime_intubation__date__lte=todate,
                                                                            datetime_intubation__date__gt=todate-difference).
                                filter(pt_location=loc))
            
            ContentDict[IntubationText]=Intubationcount
            
            ##Text and count of Return to ICU in 48 hours
            ReturntoICUText='Return to ICU in 48 hours'
            ReturntoICUcount=len(nursequalitydata.models.ReturnToICU.objects.filter(datetime_return__date__lte=todate,
                                                                            datetime_return__date__gt=todate-difference).
                                filter(pt_location=loc))
            ContentDict[ReturntoICUText]=ReturntoICUcount
            
            
            ##Text and count of cauti in request case
            CAUTIText='Cauti Cases'
            CAUTICount=len(hicdata.models.CAUTI.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference).filter(pt_location=loc))
            ContentDict[CAUTIText]=CAUTICount
            
            ##Text and count for antibiotic in request case
            AntibioticText='Antibiotic resistance cases'
            AntibioticCount=len(hicdata.models.Antibiotic.objects.filter(dateofadministration__lte=todate,
                                                            dateofadministration__gt=todate-difference).filter(pt_location=loc))
            ContentDict[AntibioticText]=AntibioticCount
            
            ##Text and count for CLABSI in request case
            CLABSIText='CLABSI cases'
            CLABSICount=len(hicdata.models.CLABSI.objects.filter(dateofrecognition__lte=todate,
                                                            dateofrecognition__gt=todate-difference).filter(pt_location=loc))
            ContentDict[CLABSIText]=CLABSICount
            
            ##Text and count for BodyFluidExposure in request case
            BodyFluidExposureText='BodyFluidExposure cases'
            BodyFluidExposureCount=len(hicdata.models.BodyFluidExposure.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference).filter(incident_location=loc))
            ContentDict[BodyFluidExposureText]=BodyFluidExposureCount
            
            ##Text and count for VAP in request case
            VAPText='VAP cases'
            VAPCount=len(hicdata.models.VAP.objects.filter(dateofrecognition__lte=todate,
                                                            dateofrecognition__gt=todate-difference).filter(pt_location=loc))
            ContentDict[VAPText]=VAPCount
            
            ##Text and count for VAE in request case
            VAEText='VAE cases'
            VAECount=len(hicdata.models.VAE.objects.filter(dateofrecognition__lte=todate,
                                                            dateofrecognition__gt=todate-difference).filter(pt_location=loc))
            ContentDict[VAEText]=VAECount
            
            ##Text and count for SSI in request case
            SSIText='SSI cases'
            SSICount=len(hicdata.models.SSI.objects.filter(dateofnotification__lte=todate,
                                                            dateofnotification__gt=todate-difference).filter(pt_location=loc))
            ContentDict[SSIText]=SSICount
            
            ##Text and count for Thrombophlebitis in request case
            ThrombophlebitisText='Thrombophlebitis cases'
            ThrombophlebitisCount=len(hicdata.models.Thrombophlebitis.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference).filter(pt_location=loc))
            ContentDict[ThrombophlebitisText]=ThrombophlebitisCount
            
            ##Text and count for NSI in request case
            NSIText='NSI cases'
            NSICount=len(hicdata.models.NSI.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference).filter(staff_location=loc))
            ContentDict[NSIText]=NSICount
        else:
            ##Text and count of Tracheostomy
            TracheostomyText='Tracheostomy Cases'
            Tracheostomycount=len(nursequalitydata.models.Tracheostomy.objects.filter(datetime_tracheostomy__date__lte=todate,
                                                                            datetime_tracheostomy__date__gt=todate-difference))
            
            ContentDict[TracheostomyText]=Tracheostomycount 
            
            ##Text and count of Pressure Sore Injury
            PressureInjuryText='Pressure Sore Injury'
            PressureInjurycount=len(nursequalitydata.models.PressureInjury.objects.filter(dateofobservation__lte=todate,
                                                                            dateofobservation__gt=todate-difference))
            
            ContentDict[PressureInjuryText]=PressureInjurycount 
            
            
            ##Text and count of Reintubation
            ReintubationText='Reintubation Cases'
            Reintubationcount=len(nursequalitydata.models.Reintubation.objects.filter(datetime_reintubation__date__lte=todate,
                                                                            datetime_reintubation__date__gt=todate-difference))
            
            ContentDict[ReintubationText]=Reintubationcount 
            
            ##Text and count of Intubation
            IntubationText='Intubation Cases'
            Intubationcount=len(nursequalitydata.models.Intubation.objects.filter(datetime_intubation__date__lte=todate,
                                                                            datetime_intubation__date__gt=todate-difference))
            
            ContentDict[IntubationText]=Intubationcount
            
            ##Text and count of Return to ICU in 48 hours
            ReturntoICUText='Return to ICU in 48 hours'
            ReturntoICUcount=len(nursequalitydata.models.ReturnToICU.objects.filter(datetime_return__date__lte=todate,
                                                                            datetime_return__date__gt=todate-difference))
            ContentDict[ReturntoICUText]=ReturntoICUcount
            
            
            ##Text and count of cauti in request case
            CAUTIText='Cauti Cases'
            CAUTICount=len(hicdata.models.CAUTI.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[CAUTIText]=CAUTICount
            
            ##Text and count for antibiotic in request case
            AntibioticText='Antibiotic resistance cases'
            AntibioticCount=len(hicdata.models.Antibiotic.objects.filter(dateofadministration__lte=todate,
                                                            dateofadministration__gt=todate-difference))
            ContentDict[AntibioticText]=AntibioticCount
            
            ##Text and count for CLABSI in request case
            CLABSIText='CLABSI cases'
            CLABSICount=len(hicdata.models.CLABSI.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[CLABSIText]=CLABSICount
            
            ##Text and count for BodyFluidExposure in request case
            BodyFluidExposureText='BodyFluidExposure cases'
            BodyFluidExposureCount=len(hicdata.models.BodyFluidExposure.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[BodyFluidExposureText]=BodyFluidExposureCount
            
            ##Text and count for VAP in request case
            VAPText='VAP cases'
            VAPCount=len(hicdata.models.VAP.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[VAPText]=VAPCount
            
            ##Text and count for VAE in request case
            VAEText='VAE cases'
            VAECount=len(hicdata.models.VAE.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[VAEText]=VAECount
            
            ##Text and count for SSI in request case
            SSIText='SSI cases'
            SSICount=len(hicdata.models.SSI.objects.filter(dateofnotification__lte=todate,
                                                            dateofnotification__gt=todate-difference))
            ContentDict[SSIText]=SSICount
            
            ##Text and count for Thrombophlebitis in request case
            ThrombophlebitisText='Thrombophlebitis cases'
            ThrombophlebitisCount=len(hicdata.models.Thrombophlebitis.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[ThrombophlebitisText]=ThrombophlebitisCount
            
            ##Text and count for NSI in request case
            NSIText='NSI cases'
            NSICount=len(hicdata.models.NSI.objects.filter(dateofincident__lte=todate,
                                                            dateofincident__gt=todate-difference))
            ContentDict[NSIText]=NSICount
        
        
        
        return render(request, 'quality.html', {"LocationList":LocationList, "ContentDict": ContentDict,'Header':Header} )

        
    
    
    ##Default header content
    else:
        Header='You are seeing Data from past 30 days'
        
        ##Text and count of Tracheostomy
        TracheostomyText='Tracheostomy Cases'
        Tracheostomycount=len(nursequalitydata.models.Tracheostomy.objects.filter(
            datetime_tracheostomy__date__lte=datetime.datetime.today(),
            datetime_tracheostomy__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        
        ContentDict[TracheostomyText]=Tracheostomycount 
        
        ##Text and count of Pressure Sore Injury
        PressureInjuryText='Pressure Sore Injury'
        PressureInjurycount=len(nursequalitydata.models.PressureInjury.objects.filter(
            dateofobservation__lte=datetime.datetime.today(),
            dateofobservation__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        
        ContentDict[PressureInjuryText]=PressureInjurycount
        
        ##Text and count of Reintubation
        ReintubationText='Reintubation Cases'
        Reintubationcount=len(nursequalitydata.models.Reintubation.objects.filter(
            datetime_reintubation__date__lte=datetime.datetime.today(),
            datetime_reintubation__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        
        ContentDict[ReintubationText]=Reintubationcount
        
        
        ##Text and count of Intubation
        IntubationText='Intubation Cases'
        Intubationcount=len(nursequalitydata.models.Intubation.objects.filter(
            datetime_intubation__date__lte=datetime.datetime.today(),
            datetime_intubation__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        print('count',Intubationcount)
        ContentDict[IntubationText]=Intubationcount
        
        ##Text and count of Return to ICU
        ReturntoICUText='Return to ICU in 48 hours'
        ReturntoICUcount=len(nursequalitydata.models.ReturnToICU.objects.filter(
            datetime_return__date__lte=datetime.datetime.today(),
            datetime_return__date__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[ReturntoICUText]=ReturntoICUcount
        
        
        ##Text and count of cauti 
        CAUTIText='Cauti Cases'
        CAUTICount=len(hicdata.models.CAUTI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                        dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[CAUTIText]=CAUTICount
        
        ##Text and count for antibiotic
        AntibioticText='Antibiotic resistance cases'
        AntibioticCount=len(hicdata.models.Antibiotic.objects.filter(dateofadministration__lte=datetime.datetime.today(),
                                                        dateofadministration__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[AntibioticText]=AntibioticCount
        
        ##Text and count for CLABSI
        CLABSIText='CLABSI cases'
        CLABSICount=len(hicdata.models.CLABSI.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                        dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[CLABSIText]=CLABSICount
        
        ##Text and count for BodyFluidExposure
        BodyFluidExposureText='BodyFluidExposure cases'
        BodyFluidExposureCount=len(hicdata.models.BodyFluidExposure.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                        dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[BodyFluidExposureText]=BodyFluidExposureCount
        
        ##Text and count for VAP
        VAPText='VAP cases'
        VAPCount=len(hicdata.models.VAP.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                        dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[VAPText]=VAPCount
        
        ##Text and count for VAE
        VAEText='VAE cases'
        VAECount=len(hicdata.models.VAE.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                        dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[VAEText]=VAECount
        
        ##Text and count for SSI
        SSIText='SSI cases'
        SSICount=len(hicdata.models.SSI.objects.filter(dateofnotification__lte=datetime.datetime.today(),
                                                        dateofnotification__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[SSIText]=SSICount
        
        ##Text and count for Thrombophlebitis
        ThrombophlebitisText='Thrombophlebitis cases'
        ThrombophlebitisCount=len(hicdata.models.Thrombophlebitis.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                        dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[ThrombophlebitisText]=ThrombophlebitisCount
        
        ##Text and count for NSI
        NSIText='NSI cases'
        NSICount=len(hicdata.models.NSI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                        dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=30)))
        ContentDict[NSIText]=NSICount
    
    return render(request, 'quality.html', {"LocationList":LocationList, "ContentDict": ContentDict,'Header':Header} )
