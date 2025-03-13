from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)

