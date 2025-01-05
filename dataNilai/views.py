from django.shortcuts import render, redirect
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from .models import nilaiMahasiswa
from .forms import NilaiMahasiswaForm
import pickle
import csv
import io

#Load predictive model for each sem
path_to_model = settings.PREDICTIVE_MODEL_PATH

with open(str(path_to_model / 'final_sem_2.pkl'), 'rb') as f:
    final_sem_2 = pickle.load(f)
    
with open(path_to_model / 'final_sem_3.pkl', 'rb') as f:
    final_sem_3 = pickle.load(f)
    
with open(path_to_model / 'final_sem_4.pkl', 'rb') as f:
    final_sem_4 = pickle.load(f)

#Prediksi kelulusan UKMPPD
def predictKelulusan(data):
    semester = data.get('semester')
    if semester == '2':
        model = final_sem_2
        features = [data.get(key, 0) for key in ['IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK']]
    elif semester == '3':
        model = final_sem_3
        features = [data.get(key, 0) for key in ['IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT','MAT', 'IKM', 'THTKL', 'KJW', 'OT2']]
    elif semester == '4':  
        model = final_sem_4
        features = [data.get(key, 0) for key in ['IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT', 'IKM', 'THTKL', 'KJW', 'OT2', 'BED', 'OBG', 'FOR', 'MOI', 'ELK']]
    else:
        return None
    
    try:
        predict_ukmppd = model.predict([features])[0]
        return predict_ukmppd
    
    except Exception as e:
        print(f"Prediction Failed: {e}")
        return None

#Extract csv dan simpan kedalam db
def upload_nilai(request):
    form = NilaiMahasiswaForm(request.POST, request.FILES)
    
    if form.is_valid():
        try:
            csv_nilai = request.FILES['file']
            csv_nilai = io.TextIOWrapper(csv_nilai.file, encoding='utf-8')
            reader = csv.DictReader(csv_nilai)
            
            print(f"CSV Header: {reader.fieldnames}")

            #Extract data untuk setiap row
            with transaction.atomic():
                for row in reader:
                    nama_mahasiswa = row.get('nama_mahasiswa')
                    NIM = row.get('NIM')
                    angkatan = row.get('angkatan')
                    semester = row.get('semester')
                    
                    nilai_stase = [
                        'IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT',
                        'IKM', 'THTKL', 'KJW', 'OT2', 'BED', 'OBG', 'FOR', 'MOI', 'ELK']
                    
                    nilai_dict = {field: float(row.get(field, 0)) for field in nilai_stase}
                    
                    instance, created = nilaiMahasiswa.objects.update_or_create(
                        NIM = NIM,
                        defaults = {
                            'nama_mahasiswa': nama_mahasiswa,
                            'angkatan': angkatan,
                            'semester': semester,
                            **nilai_dict,
                            'hasil_ukmppd': predictKelulusan({
                                **nilai_dict,
                                'semester': semester
                            })
                        }
                    )
                    
                messages.success(request, 'Data berhasil diupload')
                return redirect('form-upload-nilai')
            
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('form-upload-nilai')
        
    return render(request, 'dataNilai/form-upload-nilai.html', {'form': form})
                

def uploadNilai(request):
    return render(request, 'dataNilai/form-upload-nilai.html')