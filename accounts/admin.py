from django.contrib import admin
from .models import Departments, Locations, Doctors
# Register your models here.

admin.site.register(Departments)
admin.site.register(Locations)
admin.site.register(Doctors)