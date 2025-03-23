from django.shortcuts import render
from apps.accounts.views import superuser_required

# Create your views here.

@superuser_required
def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)

