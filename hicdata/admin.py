from django.contrib import admin
from .models import CAUTI, Antibiotic,CLABSI, BodyFluidExposure, VAP, VAE, SSI, Thrombophlebitis, NSI
# Register your models here.
admin.site.register(CAUTI)
admin.site.register(Antibiotic)
admin.site.register(CLABSI)
admin.site.register(BodyFluidExposure)
admin.site.register(VAP)
admin.site.register(VAE)
admin.site.register(SSI)
admin.site.register(Thrombophlebitis)
admin.site.register(NSI)