from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import hasilUKMPPD
from .forms import HasilUKMPPDForm
import csv
import io

#Extract csv dan simpan kedalam db
def upload_ukmppd(request):
    form = HasilUKMPPDForm(request.POST, request.FILES)
    
    if form.is_valid():
        try:
            csv_ukmppd = request.FILES['file']
            csv_ukmppd = io.TextIOWrapper(csv_ukmppd.file, encoding='utf-8')
            reader = csv.DictReader(csv_ukmppd)
            
            #Extract data untuk setiap row
            with transaction.atomic():
                for row in reader:
                    nama_mahasiswa = row.get('nama_mahasiswa')
                    NIM = row.get('NIM')
                    angkatan = row.get('angkatan')
                    periode_ukmppd = row.get('periode_ukmppd')
                    
                    nilai_stase = [
                        'IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT',
                        'IKM', 'THTKL', 'KJW', 'OT2', 'BED', 'OBG', 'FOR', 'MOI', 'ELK']

                    nilai_dict = {field: float(row.get(field, '0').replace(',', '.')) for field in nilai_stase} 

                    hasil_ukmppd_get = row.get('hasil_ukmppd')
                    hasil_ukmppd = 1 if hasil_ukmppd_get == 'Lulus' else 0
                    
                    instance, created = hasilUKMPPD.objects.update_or_create(
                        NIM=NIM,
                        defaults = {
                            'nama_mahasiswa': nama_mahasiswa,
                            'angkatan': angkatan,
                            'periode_ukmppd': periode_ukmppd,
                            **nilai_dict,
                            'hasil_ukmppd': hasil_ukmppd
                        }
                    )
    
            messages.success(request, 'Data berhasil diupload')
            return redirect('form-upload-ukmppd')
    
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('form-upload-ukmppd')
    
    return render(request, 'dataUKMPPD/form-upload-ukmppd.html', {'form': form})

def remove_param_ukmppd(query_params):
    params = query_params.split('&')
    filtered_params = [param for param in params if not param.startswith('page=')]
    return '&'.join(filtered_params)

def dashboardUKMPPD(request):
    #Search and filter
    dashboard = hasilUKMPPD.objects.all().order_by('nama_mahasiswa')
    
    record_count = hasilUKMPPD.objects.all().count()
    angkatan_list = hasilUKMPPD.objects.values_list('angkatan', flat=True).distinct()
    periode_list = hasilUKMPPD.objects.values_list('periode_ukmppd', flat=True).distinct()
    
    ukmppd_search_query = request.GET.get('query')
    ukmppd_filter_periode = request.GET.get('periode_ukmppd')
    ukmppd_filter_status = request.GET.get('status')
    
    if ukmppd_search_query:
        dashboard = dashboard.filter(Q(nama_mahasiswa__icontains = ukmppd_search_query) | Q(NIM__icontains = ukmppd_search_query))
    if ukmppd_filter_periode and ukmppd_filter_periode != 'Semua Periode':
        dashboard = dashboard.filter(periode_ukmppd = ukmppd_filter_periode)
    if ukmppd_filter_status and ukmppd_filter_status != 'Semua':
        if ukmppd_filter_status == 'Lulus':
            dashboard = dashboard.filter(hasil_ukmppd = 1)
        elif ukmppd_filter_status == 'Retake':
            dashboard = dashboard.filter(hasil_ukmppd = 0)  
    
    query_params = request.GET.urlencode()
    clean_query = remove_param_ukmppd(query_params)
    
    #Pagination
    paginator = Paginator(dashboard, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    #Widget Prediksi
    ukmppd_lulus = hasilUKMPPD.objects.filter(hasil_ukmppd = 1).count()
    ukmppd_retake = hasilUKMPPD.objects.filter(hasil_ukmppd = 0).count()

    context = {
        'page_obj': page_obj,
        'record_count': record_count,
        'angkatan_list': angkatan_list,
        'periode_list': periode_list,
        'ukmppd_search_query': ukmppd_search_query,
        'ukmppd_filter_periode': ukmppd_filter_periode,
        'ukmppd_filter_status': ukmppd_filter_status,
        'ukmppd_lulus': ukmppd_lulus,
        'ukmppd_retake': ukmppd_retake,
        'clean_query': clean_query
    } 
    
    return render(request, 'dataUKMPPD/dashboard-ukmppd.html', context)

def uploadUKMPPD(request):
    return render(request, 'dataUKMPPD/form-upload-ukmppd.html')

def detailHasilUKMPPD(request, NIM):
    select_nim = NIM
    detail = get_object_or_404(hasilUKMPPD, NIM=NIM)
    context = {
        'select_nim': select_nim,
        'detail': detail
        }
    
    return render(request, 'dataUKMPPD/detail-hasil-ukmppd.html', context)

def deleteRecord(request, NIM):
    delete_detail = get_object_or_404(hasilUKMPPD, NIM=NIM)
    delete_detail.delete()

    return redirect('index')
