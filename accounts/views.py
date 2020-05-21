from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from chat import models
import datetime
import requests




# Create your views here.

# url = 'http://api.openweathermap.org/data/2.5/weather'
# encoded_city_name = 'Kozhikode'
# country_code = 'in'
# access_token = ''

# r = requests.get('{0}?q={1},{2}&APPID={3}'.format(
# url, 
# encoded_city_name, 
# country_code, 
# access_token))

# #print(r.json())


#temp login and logout
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password= request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect( 'imshome')
        else:   
            messages.info(request, 'Invalid Credentials')
            
            return redirect ( 'login')
    return render(request, 'login.html')


''' def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password= request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            chats=models.c  hatlog.objects.all()[10:]
            
            return HttpResponseRedirect( 'index', {'chats': chats})
        else:   
            messages.info(request, 'Invalid Credentials')
            
            return redirect ( 'login')
    return render(request, 'login.html') '''
def logout(request):
    auth.logout(request)
    return redirect( 'login')

def chatsubmit(request):
    chat=models.chatlog(textmessage=request.POST['message'], chatuserid=request.user)
    chat.save()
    chats=models.chatlog.objects.order_by('timestamp').reverse()[:10]
    print(chats)
    return HttpResponseRedirect( 'index',{'chats': chats})
def index(request):
    chats=models.chatlog.objects.order_by('timestamp').reverse()[:10]
    
    return render(request, 'index.html', {'chats': chats})
    
