from django.shortcuts import render, get_object_or_404
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
def remove_param_nilai(query_params):
    params = query_params.split('&')
    filtered_params = [param for param in params if not param.startswith('page=')]
    return '&'.join(filtered_params)

def index(request):
    #Search and filter
    dashboard = nilaiMahasiswa.objects.all().order_by('nama_mahasiswa')
    
    record_count = nilaiMahasiswa.objects.all().count()
    angkatan_list = nilaiMahasiswa.objects.values_list('angkatan', flat=True).distinct()
    nilai_search_query = request.GET.get('query')
    nilai_filter_angkatan = request.GET.get('angkatan')
    nilai_filter_status = request.GET.get('status')
    
    if nilai_search_query:
        dashboard = dashboard.filter(Q(nama_mahasiswa__icontains = nilai_search_query) | Q(NIM__icontains = nilai_search_query))
    if nilai_filter_angkatan and nilai_filter_angkatan != 'Semua Angkatan':
        dashboard = dashboard.filter(angkatan = nilai_filter_angkatan)
    if nilai_filter_status and nilai_filter_status != 'Semua':
        if nilai_filter_status == 'Lulus':
            dashboard = dashboard.filter(hasil_ukmppd = 1)
        elif nilai_filter_status == 'Retake':
            dashboard = dashboard.filter(hasil_ukmppd = 0)
            
    query_params = request.GET.urlencode()
    clean_query = remove_param_nilai(query_params)
                    
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
        'nilai_search_query': nilai_search_query,
        'nilai_filter_angkatan': nilai_filter_angkatan,
        'nilai_filter_status': nilai_filter_status,
        'predict_lulus': predict_lulus,
        'predict_retake': predict_retake,
        'clean_query': clean_query
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