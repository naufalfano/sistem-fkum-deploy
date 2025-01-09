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
# Create Case Base
def create_case_base(semester: int) -> List[Dict[str, any]]:
    cases = caseRetake.objects.filter(semester=semester)
    case_base = []
    for case in cases:
        attributes = {
            "IPD": case.IPD,
            "IKA": case.IKA,
            "RAD": case.RAD,
            "SRM": case.SRM,
            "KDK": case.KDK,
            "MPK": case.MPK,
            "ANT": case.ANT,
            "MAT": case.MAT,
            "IKM": case.IKM,
            "THTKL": case.THTKL,
            "KJW": case.KJW,
            "OT2": case.OT2,
            "BED": case.BED,
            "OBG": case.OBG,
            "FOR": case.FOR,
            "MOI": case.MOI,
            "ELK": case.ELK,
        }
        # attributes = {key: value for key, value in attributes.items() if value is not None}
        case_base.append({
            "attributes": attributes,
            "solution": case.solution,
            "case_instance": case
        })
    return case_base

# Retrieve
def retrieve_case(case_base: List[Dict[str, any]], new_case: Dict[str, any], k: int = 1) -> List[Tuple[int, float, str]]:
    distances = []
    for index, case in enumerate(case_base):
        existing_case = case["attributes"]
        distance = compute_distance(new_case, existing_case)
        distances.append((case["case_instance"], distance, case["solution"]))  # Include caseRetake instance

    distances.sort(key=lambda x: x[1])
    return distances[:k]

# Compute Distance
def compute_distance(case1: Dict[str, any], case2: Dict[str, any]) -> float:
    keys = set(case1.keys()).union(case2.keys())
    vector1 = np.array([case1.get(key, 0) if case1.get(key) is not None else 0 for key in keys])
    vector2 = np.array([case2.get(key, 0) if case2.get(key) is not None else 0 for key in keys])
    return np.linalg.norm(vector1 - vector2)

# Reuse
def reuse_solution(retrieved_cases: List[Tuple[int, float, str]]) -> str:
    if retrieved_cases:
        weighted_scores = {}
        for _, distance, solution in retrieved_cases:
            weight = 1 / (distance + 1e-5)  # Add a small constant to avoid division by zero
            weighted_scores[solution] = weighted_scores.get(solution, 0) + weight
        
        # Return the solution with the highest weight
        return max(weighted_scores, key=weighted_scores.get)
    return "No similar case found."


# Rekomendasi Sistem Pakar
def find_similar_case(new_case: Dict[str, float], semester: int) -> Tuple[caseRetake, float]:
    case_base = create_case_base(semester)
    retrieved_cases = retrieve_case(case_base, new_case)
    solution = reuse_solution(retrieved_cases)
    
    return solution
    


#Extract csv dan simpan kedalam db
def upload_nilai(request):
    form = NilaiMahasiswaForm(request.POST, request.FILES)
    
    if form.is_valid():
        try:
            csv_nilai = request.FILES['file']
            csv_nilai = io.TextIOWrapper(csv_nilai.file, encoding='utf-8')
            reader = csv.DictReader(csv_nilai)

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
                    
                    nilai_dict = {
                        field: float(row.get(field, '0').replace(',', '.')) if row.get(field, '0').replace(',', '.') != '' else 0.0
                        for field in nilai_stase
                    }   

                    result = predictKelulusan({
                        **nilai_dict,
                        'semester': semester
                    })

                    # Ensure that result is a dictionary and contains the correct keys
                    hasil_ukmppd = result.get('hasil_ukmppd', 0)
                    solution = result.get('solution', "")

                    # Jika hasil UKMPPD = 0, cari solusi menggunakan sistem pakar
                    if hasil_ukmppd == 0:
                        solution = find_similar_case(nilai_dict, semester )
                    
                    instance, created = nilaiMahasiswa.objects.update_or_create(
                        NIM = NIM,
                        defaults = {
                            'nama_mahasiswa': nama_mahasiswa,
                            'angkatan': angkatan,
                            'semester': semester,
                            **nilai_dict,
                            'hasil_ukmppd': hasil_ukmppd,  # Correct assignment
                            'solution': solution
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