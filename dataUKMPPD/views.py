from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboardUKMPPD(request):
    return render(request, 'dataUKMPPD/dashboard-ukmppd.html')
