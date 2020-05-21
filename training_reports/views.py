from django.shortcuts import render

# Create your views here.
def training_reports(request):
    return render(request, 'training_reports.html')