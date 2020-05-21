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
from actionplan.views import actionplanview

urlpatterns = [
    path('actionplanedit', views.actionplanedit, name='actionplanedit'),
    path('actionplanedit<int:pk>',views.actionplanedit,name='actionplanedit'),
    path('actionplandelete<int:pk>', views.actionplandelete, name='actionplandelete'),
    path('actionplanview', actionplanview.as_view(), name='actionplanview'),
    path('actionplanview<str:_create>', actionplanview.as_view(), name='actionplanview'),
    #path('imsdetailview<int:pk>',imsdetailview.as_view(),name='imsdetailview'),
    #path('imshome', views.imshome, name='imshome'),
    #path('imsadmin',views.imsadmin, name='imsadmin'),
    #path('imsarchive',views.imsarchive,name='imsarchive')
    ]