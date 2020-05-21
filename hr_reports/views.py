from django.shortcuts import render

# Create your views here.
def hr_reports(request):
    return render(request, 'hr_reports.html')