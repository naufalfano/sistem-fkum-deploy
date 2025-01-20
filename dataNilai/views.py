from django.shortcuts import render, redirect
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from .models import nilaiMahasiswa
from .forms import NilaiMahasiswaForm
from .models import caseRetake
from typing import Dict, List, Tuple
import numpy as np
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
       return {'hasil_ukmppd': 0, 'solution': ""}
    
    try:
        predict_ukmppd = model.predict([features])[0]
        return {'hasil_ukmppd': predict_ukmppd, 'solution': ""}
    except Exception as e:
        print(f"Prediction Failed: {e}")
        return {'hasil_ukmppd': 0, 'solution': ""}

# Sistem Pakar
def evaluate_rules(data):
    semester = int(data.get('semester', 0))
    solution = ""

    # Rules Semester 2
    if semester == 2:
        if data.get('SRM', 0) < 64:
            solution = ("Memberi perhatian intensif pada tingkat dreyfuss level Novice untuk stase "
                        "Ilmu Kesehatan Masyarakat (IKM), Ilmu Kesehatan Mata (MAT), Ilmu Penyakit "
                        "THT-KL (THT-KL), Ilmu Kedokteran Jiwa (KJW), dan Anestesiologi dan Terapi "
                        "Insentif (ANT) untuk tingkat dreyfuss level Advance Beginner.")
        elif data.get('IPD', 0) < 64 or data.get('IKA', 0) < 64 or data.get('KDK', 0) < 64:
            solution = ("Memberi perhatian intensif pada tingkat dreyfuss level Novice untuk stase "
                        "Ilmu Kesehatan Masyarakat (IKM), Ilmu Kesehatan Mata (MAT), Ilmu Penyakit "
                        "THT-KL (THT-KL), dan Anestesiologi dan Terapi Insentif (ANT) untuk tingkat "
                        "dreyfuss level Advance Beginner.")
        elif data.get('RAD', 0) < 64:
            solution = ("Memberi perhatian intensif pada tingkat dreyfuss level Novice untuk stase "
                        "Ilmu Kesehatan Masyarakat (IKM), dan Anestesiologi dan Terapi Insentif (ANT) "
                        "untuk tingkat dreyfuss level Advance Beginner.")
        else :
            solution = ("Memberi perhatian intensif pada Modul Integrasi (MOI) untuk tingkat dreyfuss level Competent.")

    # Rules Semester 3
    elif semester == 3:
        if data.get('ANT', 0) < 64:
            solution = ("Memberi perhatian intensif pada tingkat dreyfuss level Advance Beginner untuk "
                        "stase Ilmu Bedah (BED), dan Modul Integrasi (MOI) untuk tingkat dreyfuss level Competent.")
        elif data.get('MAT', 0) < 64 or data.get('IKM', 0) < 64 or data.get('THTKL', 0) < 64 or data.get('KJW', 0) < 64:
            solution = ("Memberi perhatian intensif pada tingkat dreyfuss level Advance Beginner untuk "
                        "stase Ilmu Bedah (BED), Ilmu Kebidanan dan Kandungan (OBG), Kedokteran Forensik (FOR), "
                        "dan Modul Integrasi (MOI) untuk tingkat dreyfuss level Competent.")
        else :
            solution = ("Memberi perhatian intensif pada Modul Integrasi (MOI) untuk tingkat dreyfuss level Competent.")

    # Rules Semester 4
    elif semester == 4:
        if data.get('BED', 0) < 64 or data.get('OBG', 0) < 64 or data.get('FOR', 0) < 64:
            solution = ("Memberi perhatian intensif pada Modul Integrasi (MOI) untuk tingkat dreyfuss level Competent.")
        else :
            solution = ("Memberi perhatian intensif pada Modul Integrasi (MOI) untuk tingkat dreyfuss level Competent.")

    return solution



#File upload
def upload_nilai(request):
    form = NilaiMahasiswaForm(request.POST, request.FILES)

    if form.is_valid():
        try:
            csv_nilai = request.FILES['file']
            csv_nilai = io.TextIOWrapper(csv_nilai.file, encoding='utf-8')
            reader = csv.DictReader(csv_nilai)

            with transaction.atomic():
                for row in reader:
                    nama_mahasiswa = row.get('nama_mahasiswa')
                    NIM = row.get('NIM')
                    angkatan = row.get('angkatan')
                    semester = row.get('semester')

                    nilai_stase = [
                        'IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT',
                        'IKM', 'THTKL', 'KJW', 'OT2', 'BED', 'OBG', 'FOR', 'MOI', 'ELK']

                    nilai_dict = {
                        field: float(row.get(field, '0').replace(',', '.')) if row.get(field, '0').replace(',', '.') != '' else 0.0
                        for field in nilai_stase
                    }

                    result = predictKelulusan({**nilai_dict, 'semester': semester})
                    getSolution = ""
                    if result['hasil_ukmppd'] == 0:
                        getSolution = evaluate_rules({**nilai_dict, 'semester': semester})

                    
                    instance, created = nilaiMahasiswa.objects.update_or_create(
                        NIM=NIM,
                        defaults={
                            'nama_mahasiswa': nama_mahasiswa,
                            'angkatan': angkatan,
                            'semester': semester,
                            **nilai_dict,
                            'hasil_ukmppd': result['hasil_ukmppd'],
                            'solution': getSolution
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