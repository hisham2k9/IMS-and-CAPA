import django_tables2 as tables
import hicdata
import nursequalitydata

##1. CAUTI from hicdata
class CAUTITable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.CAUTI
        exclude=['username', 'timestamp', 'id']

##2. Antibiotic from hicdata
class AntibioticTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.Antibiotic
        exclude=['username', 'timestamp', 'id']

##3. Clabsi from hicdata
class CLABSITable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.CLABSI
        exclude=['username', 'timestamp', 'id']
        
##4. BodyFluidExposure from hicdata
class BodyFluidExposureTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.BodyFluidExposure
        exclude=['username', 'timestamp', 'id']

##5. VAP from hicdata
class VAPTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.VAP
        exclude=['username', 'timestamp', 'id']

##6. VAE from hicdata
class VAETable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.VAE
        exclude=['username', 'timestamp', 'id']
        
##7. SSI from hicdata
class SSITable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.SSI
        exclude=['username', 'timestamp', 'id']
        

##8. Thrombophlebitis from hicdata
class ThrombophlebitisTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.Thrombophlebitis
        exclude=['username', 'timestamp', 'id']
        
##9. NSI from hicdata
class NSITable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = hicdata.models.NSI
        exclude=['username', 'timestamp', 'id']


###############################################################################
#############################################################################
##nurse quality data

##1. ReturnToICU from hicdata
class ReturnToICUTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = nursequalitydata.models.ReturnToICU
        exclude=['username', 'timestamp', 'id']

##2. Intubation from hicdata
class IntubationTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = nursequalitydata.models.Intubation
        exclude=['username', 'timestamp', 'id']

##3. Reintubation from hicdata
class ReintubationTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = nursequalitydata.models.Reintubation
        exclude=['username', 'timestamp', 'id']

##4. PressureInjury from hicdata
class PressureInjuryTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = nursequalitydata.models.PressureInjury
        exclude=['username', 'timestamp', 'id']


##5. Tracheostomy from hicdata
class TracheostomyTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = nursequalitydata.models.Tracheostomy
        exclude=['username', 'timestamp', 'id']



##6. RestraintInjury from hicdata
class RestraintInjuryTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover",
                 'id':'table' }
        model = nursequalitydata.models.RestraintInjury
        exclude=['username', 'timestamp', 'id']
