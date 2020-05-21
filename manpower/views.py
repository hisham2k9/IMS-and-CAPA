from django.shortcuts import render

# Create your views here.
def manpower(request):
    return render(request, 'manpower.html')