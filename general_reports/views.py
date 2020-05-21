from django.shortcuts import render

# Create your views here.

def general_reports(request):
    
    return render (request, 'general_reports.html')