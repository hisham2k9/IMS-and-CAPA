from django.contrib import admin
from .models import imsmodel, imssubmissionfiles,imsassignfiles, imsinvestigationfiles, imsvalidationfiles, imsadminlog

# Register your models here.
admin.site.register(imsmodel)
admin.site.register(imssubmissionfiles)
admin.site.register(imsassignfiles)
admin.site.register(imsinvestigationfiles)
admin.site.register(imsvalidationfiles)
admin.site.register(imsadminlog)