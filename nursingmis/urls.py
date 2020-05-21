"""nursingmis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog #for admin date time picker
from django.conf import settings #for media files
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('general.urls')),
    path('', include('manpower.urls')),
    path('', include('quality.urls')),
    path('', include('training.urls')),
    path('', include('hr.urls')),
    path('', include('general_reports.urls')),
    path('', include('manpower_reports.urls')),
    path('', include('quality_reports.urls')),
    path('', include('training_reports.urls')),
    path('', include('hr_reports.urls')),
    path('', include('hicdata.urls')),
    path('', include('testitems.urls')),
    path('', include('general_charts.urls')),
    path('', include('quality_charts.urls')),
    path('', include('nursequalitydata.urls')),
    path('', include('ims.urls')),
    path('',include('actionplan.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),  #for admin datetime picker on app
]

urlpatterns=urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)