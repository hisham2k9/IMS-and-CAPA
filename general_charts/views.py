from django.shortcuts import render

# Create your views here.

def general_charts(request):
    return render(request, 'general_charts.html')
