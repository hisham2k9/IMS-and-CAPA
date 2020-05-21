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
from . import views
from nursequalitydata.views import nursequalitydata
#urlpatterns = [
 #   path('nursequalitydata', views.nursequalitydata, name='nursequalitydata'),
  #  path('NQsave', views.NQsave, name='save')
  #  ]


urlpatterns = [
    path(r'nursequalitydata', nursequalitydata.as_view(), name='nursequalitydata'),
    path(r'nursequalitylist', views.nursequalitylist, name='nursequalitylist'),
    path(r'nursequalityedit<int:pk><str:formname>', views.nursequalityedit, name='nursequalityedit'),#to edit post
    path(r'nursequalitydelete<int:pk><str:formname>', views.nursequalitydelete, name='nursequalitydelete'),
    ]