from django.contrib import admin
from .models import ReturnToICU,Intubation, Reintubation, PressureInjury, Tracheostomy, RestraintInjury
# Register your models here.


admin.site.register(ReturnToICU)
admin.site.register(Intubation)
admin.site.register(Reintubation)
admin.site.register(PressureInjury)
admin.site.register(Tracheostomy)
admin.site.register(RestraintInjury)