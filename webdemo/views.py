from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
from dataNilai.models import nilaiMahasiswa

'''
Tanpa pakai template (langsung views)
def homepage(request):
    return HttpResponse("testing views django 123")
'''
def index(request):
    #Search and filter
    dashboard = nilaiMahasiswa.objects.all().order_by('nama_mahasiswa')
    
    record_count = nilaiMahasiswa.objects.all().count()
    angkatan_list = nilaiMahasiswa.objects.values_list('angkatan', flat=True).distinct()
    search_query = request.GET.get('query')
    filter_angkatan = request.GET.get('angkatan')
    filter_status = request.GET.get('status')
    
    if search_query:
        dashboard = dashboard.filter(Q(nama_mahasiswa__icontains = search_query) | Q(NIM__icontains = search_query))
    if filter_angkatan and filter_angkatan != 'Semua Angkatan':
        dashboard = dashboard.filter(angkatan = filter_angkatan)
    if filter_status and filter_status != 'Semua':
        if filter_status == 'Lulus':
            dashboard = dashboard.filter(hasil_ukmppd = 1)
        elif filter_status == 'Retake':
            dashboard = dashboard.filter(hasil_ukmppd = 0)  
                    
    #Pagination
    paginator = Paginator(dashboard, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    record_count = dashboard.count()    
    #Widget Prediksi
    predict_lulus = nilaiMahasiswa.objects.filter(hasil_ukmppd = 1).count()
    predict_retake = nilaiMahasiswa.objects.filter(hasil_ukmppd = 0).count()

    context = {
        'page_obj': page_obj,
        'record_count': record_count,
        'angkatan_list': angkatan_list,
        'search_query': search_query,
        'filter_angkatan': filter_angkatan,
        'filter_status': filter_status,
        'predict_lulus': predict_lulus,
        'predict_retake': predict_retake,
    }
        
    return render(request, 'homepage.html', context)

def detailNilai(request, NIM):
    select_nim = NIM
    detail = get_object_or_404(nilaiMahasiswa, NIM=NIM)
    context = {
        'select_nim': select_nim,
        'detail': detail
    }
    
    return render(request, 'detail-nilai.html', context)

def deleteRecord(request, NIM):
    delete_detail = get_object_or_404(nilaiMahasiswa, NIM=NIM)
    delete_detail.delete()

    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('/login/')