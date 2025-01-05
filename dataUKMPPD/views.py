from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import hasilUKMPPD

def dashboardUKMPPD(request):
    dashboard = hasilUKMPPD.objects.all()
    paginator = Paginator(dashboard, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    } 
    return render(request, 'dataUKMPPD/dashboard-ukmppd.html', context)

def uploadUKMPPD(request):
    return render(request, 'dataUKMPPD/form-upload-ukmppd.html')

def detailHasilUKMPPD(request):
    return render(request, 'dataUKMPPD/detail-hasil-ukmppd.html')
