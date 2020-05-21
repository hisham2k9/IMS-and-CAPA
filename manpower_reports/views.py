from django.shortcuts import render

# Create your views here.

def manpower_reports(request):
    return render (request, 'manpower_reports.html')