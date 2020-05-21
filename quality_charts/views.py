from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View
import hicdata
import nursequalitydata
import accounts
from django_pivot.pivot import pivot
from django_pivot.histogram import histogram
from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from accounts.models import Locations
import datetime
####################################################################################


 ## i want a dictionary with keys as locations and values as count of each location events
       # qs=nursequalitydata.models.ReturnToICU.objects.values('pt_location').annotate(Count('pt_id'))
        #print(qs)
        #kick = [[q['pt_location'], q['pt_id__count']] for q in qs]
        #kick =[(k,v) for k, v in qs.items()]
        
        ## i want a query with data coming as date on x axis, count on y axis, and dimension expressed in line
        
        #pivot_table=pivot(hicdata.models.CAUTI.objects.all(),'dateofincident', 'pt_location', 'pt_id' )
        
        
LocationList=Locations.objects.all()




class quality_charts(View):
    
    
    def get(self, request):
        
        qs={}
        qs2={}
        ##hic data 
        ##cautidata
        CAUTIpie=hicdata.models.CAUTI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        CAUTIline=hicdata.models.CAUTI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        ##antibiotic
        Antibioticpie=hicdata.models.Antibiotic.objects.filter(dateofadministration__lte=datetime.datetime.today(),
                                                                dateofadministration__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        Antibitiocline=hicdata.models.Antibiotic.objects.filter(dateofadministration__lte=datetime.datetime.today(),
                                                                dateofadministration__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofadministration')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        
        ##clabsi
        CLABSIpie=hicdata.models.CLABSI.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        CLABSIline=hicdata.models.CLABSI.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
       
        ##bodyfluidexposure
        ##special note: needs to annotate each fields in pie chart to match the template names
        BodyFluidExposurepie=hicdata.models.BodyFluidExposure.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)).annotate(pt_location=
                                                                               F('incident_location')).values('pt_location').annotate(pt_id__count=Count('staff_id'))
        BodyFluidExposureline=hicdata.models.BodyFluidExposure.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('staff_id')).values('month','c')
        
        ##VAP 
        VAPpie=hicdata.models.VAP.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        VAPline=hicdata.models.VAP.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        ##VAE 
        VAEpie=hicdata.models.VAE.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        VAEline=hicdata.models.VAE.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        ##SSI 
        SSIpie=hicdata.models.SSI.objects.filter(dateofnotification__lte=datetime.datetime.today(),
                                                                dateofnotification__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        SSIline=hicdata.models.SSI.objects.filter(dateofnotification__lte=datetime.datetime.today(),
                                                                dateofnotification__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofnotification')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        ##Thrombophlebitis 
        Thrombophlebitispie=hicdata.models.Thrombophlebitis.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        Thrombophlebitisline=hicdata.models.Thrombophlebitis.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        ##NSI 
        NSIpie=hicdata.models.NSI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)).annotate(pt_location=
                                                                               F('staff_location')).values('pt_location').annotate(Count('staff_id'))
        NSIline=hicdata.models.NSI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('staff_id')).values('month','c') 
        
        ##Return TO ICU 48 hours
        ReturnToICUpie=nursequalitydata.models.ReturnToICU.objects.filter(datetime_return__lte=datetime.datetime.today(),
                                                                datetime_return__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        ReturnToICUline=nursequalitydata.models.ReturnToICU.objects.filter(datetime_return__lte=datetime.datetime.today(),
                                                                datetime_return__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_return')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        ##Intubation
        Intubationpie=nursequalitydata.models.Intubation.objects.filter(datetime_intubation__lte=datetime.datetime.today(),
                                                                datetime_intubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        Intubationline=nursequalitydata.models.Intubation.objects.filter(datetime_intubation__lte=datetime.datetime.today(),
                                                                datetime_intubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_intubation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
                                                                
         ##Reintubation
        Reintubationpie=nursequalitydata.models.Reintubation.objects.filter(datetime_reintubation__lte=datetime.datetime.today(),
                                                                datetime_reintubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        Reintubationline=nursequalitydata.models.Reintubation.objects.filter(datetime_reintubation__lte=datetime.datetime.today(),
                                                                datetime_reintubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_reintubation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        ##PressureInjury
        PressureInjurypie=nursequalitydata.models.PressureInjury.objects.filter(dateofobservation__lte=datetime.datetime.today(),
                                                                dateofobservation__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        PressureInjuryline=nursequalitydata.models.PressureInjury.objects.filter(dateofobservation__lte=datetime.datetime.today(),
                                                                dateofobservation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofobservation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
                                                                
                                                                                                                    
        
        ##Tracheostomy
        Tracheostomypie=nursequalitydata.models.Tracheostomy.objects.filter(datetime_tracheostomy__lte=datetime.datetime.today(),
                                                                datetime_tracheostomy__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        Tracheostomyline=nursequalitydata.models.Tracheostomy.objects.filter(datetime_tracheostomy__lte=datetime.datetime.today(),
                                                                datetime_tracheostomy__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_tracheostomy')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        ##RestraintInjury
        RestraintInjurypie=nursequalitydata.models.RestraintInjury.objects.filter(datetime_restraintstart__lte=datetime.datetime.today(),
                                                                datetime_restraintstart__gt=datetime.datetime.today()-datetime.timedelta(days=365)).values('pt_location').annotate(Count('pt_id'))
        RestraintInjuryline=nursequalitydata.models.RestraintInjury.objects.filter(datetime_restraintstart__lte=datetime.datetime.today(),
                                                                datetime_restraintstart__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_restraintstart')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
        
        ##add your queries to list qs
        qs=[CAUTIpie,CAUTIline, Antibioticpie,Antibitiocline, CLABSIpie, CLABSIline,
            BodyFluidExposurepie,BodyFluidExposureline,VAPpie,VAPline, VAEpie, VAEline,
            SSIpie, SSIline,Thrombophlebitispie,Thrombophlebitisline, NSIpie, NSIline,
            ReturnToICUpie,ReturnToICUline, Intubationpie, Intubationline, Reintubationpie,Reintubationline,
            PressureInjurypie,PressureInjuryline, Tracheostomypie, Tracheostomyline, 
            RestraintInjurypie,RestraintInjuryline
            ]
        ##add unique names of charts
        ChartNames=['CAUTI','CAUTI_', 'Antibiotic Resistance Incidents','Antibiotic Resistance Incidents_',
                     'CLABSI', 'CLABSI_', 'Body Fluid Exposure', 'Body Fluid Exposure_', 'VAP', 'VAP_','VAE','VAE_',
                     'SSI', 'SSI_', 'Thrombophlebitis', 'Thrombophlebitis_', 'NSI', 'NSI_', 'Return to ICU in 48 Hours',
                     'Return to ICU in 48 Hours_', 'Intubation', 'Intubation_', 'Reintubation', 'Reintubation_', 
                     'Pressure Injury', 'Pressure Injury_', 'Tracheostomy', 'Tracheostomy_',
                     'Restraint Injury', 'Restraint Injury_'
                    
                    ]
        scriptdata=zip(qs,ChartNames)
        print(BodyFluidExposureline)
        
        
        return render(request, 'quality_charts.html', {'LocationList':LocationList,'qs':qs,
                                                       'ChartNames':ChartNames, 'scriptdata': scriptdata})
        
        
    def post(self, request):
        
        if request.POST['locSelection']=='All':
            return redirect('/quality_charts') 

        else:
            loc=request.POST['locSelection']
            #print(type(loc))
            ##CAUTI
            print('helli',hicdata.models.CAUTI.objects.filter(pt_location='  KT ICU'))
            CAUTIline=hicdata.models.CAUTI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LCAUTIline=hicdata.models.CAUTI.objects.filter(pt_location=loc).filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            
            
            ##Antibiotic
            Antibitiocline=hicdata.models.Antibiotic.objects.filter(dateofadministration__lte=datetime.datetime.today(),
                                                                dateofadministration__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofadministration')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LAntibitiocline=hicdata.models.Antibiotic.objects.filter(pt_location=loc).filter(dateofadministration__lte=datetime.datetime.today(),
                                                                dateofadministration__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofadministration')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            
            ##CLABSI
            CLABSIline=hicdata.models.CLABSI.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LCLABSIline=hicdata.models.CLABSI.objects.filter(pt_location=loc).filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')                                                    
            
            ##BodyFluidExposure
            BodyFluidExposureline=hicdata.models.BodyFluidExposure.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('staff_id')).values('month','c')
            LBodyFluidExposureline=hicdata.models.BodyFluidExposure.objects.filter(incident_location=loc).filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('staff_id')).values('month','c')
            
            ##VAP 
            VAPline=hicdata.models.VAP.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')

            LVAPline=hicdata.models.VAP.objects.filter(pt_location=loc).filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
        
            ##VAE 
            VAEline=hicdata.models.VAE.objects.filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')

            LVAEline=hicdata.models.VAE.objects.filter(pt_location=loc).filter(dateofrecognition__lte=datetime.datetime.today(),
                                                                dateofrecognition__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofrecognition')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            ##SSI
            SSIline=hicdata.models.SSI.objects.filter(dateofnotification__lte=datetime.datetime.today(),
                                                                dateofnotification__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofnotification')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LSSIline=hicdata.models.SSI.objects.filter(pt_location=loc).filter(dateofnotification__lte=datetime.datetime.today(),
                                                                dateofnotification__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofnotification')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            #Thrombophlebitis
            Thrombophlebitisline=hicdata.models.Thrombophlebitis.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LThrombophlebitisline=hicdata.models.Thrombophlebitis.objects.filter(pt_location=loc).filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            ##NSI
            NSIline=hicdata.models.NSI.objects.filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('staff_id')).values('month','c') 
            LNSIline=hicdata.models.NSI.objects.filter(staff_location=loc).filter(dateofincident__lte=datetime.datetime.today(),
                                                                dateofincident__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofincident')
                                                                           ).values('month').annotate(c=Count('staff_id')).values('month','c') 
            
            ##Return TO ICU
            ReturnToICUline=nursequalitydata.models.ReturnToICU.objects.filter(datetime_return__lte=datetime.datetime.today(),
                                                                datetime_return__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_return')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LReturnToICUline=nursequalitydata.models.ReturnToICU.objects.filter(pt_location=loc).filter(datetime_return__lte=datetime.datetime.today(),
                                                                datetime_return__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_return')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            ##Intubation
            Intubationline=nursequalitydata.models.Intubation.objects.filter(datetime_intubation__lte=datetime.datetime.today(),
                                                                datetime_intubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_intubation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LIntubationline=nursequalitydata.models.Intubation.objects.filter(pt_location=loc).filter(datetime_intubation__lte=datetime.datetime.today(),
                                                                datetime_intubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_intubation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            ##Reintubation
            Reintubationline=nursequalitydata.models.Reintubation.objects.filter(datetime_reintubation__lte=datetime.datetime.today(),
                                                                datetime_reintubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_reintubation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LReintubationline=nursequalitydata.models.Reintubation.objects.filter(pt_location=loc).filter(datetime_reintubation__lte=datetime.datetime.today(),
                                                                datetime_reintubation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_reintubation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            ##Pressure Injury
            PressureInjuryline=nursequalitydata.models.PressureInjury.objects.filter(dateofobservation__lte=datetime.datetime.today(),
                                                                dateofobservation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofobservation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LPressureInjuryline=nursequalitydata.models.PressureInjury.objects.filter(pt_location=loc).filter(dateofobservation__lte=datetime.datetime.today(),
                                                                dateofobservation__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('dateofobservation')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')                                                    
            
            ##Tracheostomy
            Tracheostomyline=nursequalitydata.models.Tracheostomy.objects.filter(datetime_tracheostomy__lte=datetime.datetime.today(),
                                                                datetime_tracheostomy__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_tracheostomy')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LTracheostomyline=nursequalitydata.models.Tracheostomy.objects.filter(pt_location=loc).filter(datetime_tracheostomy__lte=datetime.datetime.today(),
                                                                datetime_tracheostomy__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_tracheostomy')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            ##Restraint Injury
            RestraintInjuryline=nursequalitydata.models.RestraintInjury.objects.filter(datetime_restraintstart__lte=datetime.datetime.today(),
                                                                datetime_restraintstart__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_restraintstart')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            LRestraintInjuryline=nursequalitydata.models.RestraintInjury.objects.filter(pt_location=loc).filter(datetime_restraintstart__lte=datetime.datetime.today(),
                                                                datetime_restraintstart__gt=datetime.datetime.today()-datetime.timedelta(days=365)
                                                                ).annotate(month=TruncMonth('datetime_restraintstart')
                                                                           ).values('month').annotate(c=Count('pt_id')).values('month','c')
            
            ##add your total hospital  qs in this list
            qsList=[CAUTIline,Antibitiocline,  CLABSIline, 
            BodyFluidExposureline,VAPline, VAEline,
            SSIline, Thrombophlebitisline, NSIline, 
            ReturnToICUline, Intubationline,  Reintubationline,
            PressureInjuryline, Tracheostomyline, 
            RestraintInjuryline,
            ]
            print(LReturnToICUline)
            ##add your location qs in this list
            LqsList=[
                LCAUTIline, LAntibitiocline, LCLABSIline,LBodyFluidExposureline,LVAPline, LVAEline,
                LSSIline,LThrombophlebitisline, LNSIline,LReturnToICUline, LIntubationline, LReintubationline,
                LPressureInjuryline,  LTracheostomyline, 
                LRestraintInjuryline
            ]
            ##add unique names of charts
            ChartNames=['CAUTI', 'Antibiotic Resistance Incidents',
                        'CLABSI',  'Body Fluid Exposure',  'VAP','VAE',
                        'SSI', 'Thrombophlebitis',  'NSI',  'Return to ICU in 48 Hours',
                        'Intubation',  'Reintubation', 
                        'Pressure Injury',  'Tracheostomy', 
                        'Restraint Injury', 
                        
                        ]
            scriptdata=zip(qsList, LqsList,ChartNames)
            
            return render(request, 'quality_charts_search.html', {'loc':loc, 'LocationList':LocationList,'qsList':qsList,'Lqs':LqsList,
                                                       'ChartNames':ChartNames, 'scriptdata': scriptdata})
        