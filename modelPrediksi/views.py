from django.shortcuts import render, redirect
from dataUKMPPD.models import hasilUKMPPD
from dataNilai.models import nilaiMahasiswa
from dataNilai.views import evaluate_rules
from .models import RetrainLog
import numpy as np
import pandas as pd
import os
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from imblearn.over_sampling import SMOTE
from sklearn.metrics import f1_score
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
import joblib

def modelPrediksi(request):
    if request.method == 'POST':
        semester = request.POST.get('semester')
        
        if semester == '2':
            fields = ['IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK']
            params = {
                "colsample_bytree": 0.9,
                "learning_rate": 0.1,
                "subsample": 0.9,
                "max_depth": 5,
                "gamma": 0.1
            }
            n_splits = 5
            
        elif semester == '3':
            fields = ['IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT', 'IKM', 'THTKL', 'KJW', 'OT2']
            params = {
                "colsample_bytree": 0.3,
                "learning_rate": 0.1,
                "subsample": 0.5,
                "max_depth": 3,
                "gamma": 0.1
            }
            n_splits = 8
            
        elif semester == '4':
            fields = ['IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT', 'IKM', 'THTKL', 'KJW', 'OT2', 'BED', 'OBG', 'FOR', 'MOI', 'ELK']
            params = {
                "colsample_bytree": 0.3,
                "learning_rate": 0.3,
                "subsample": 0.5,
                "max_depth": 5,
                "gamma": 0.1
            }
            n_splits = 8
        else:
            messages.error(request, 'Semester tidak sesuai')
            return redirect('index')

        X = pd.DataFrame(list(hasilUKMPPD.objects.values(*fields)))
        y = pd.Series(list(hasilUKMPPD.objects.values_list('hasil_ukmppd', flat=True)))
        
        model = XGBClassifier(eval_metric='logloss', **params)
        kfold_cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        f1_scores = []

        for fold, (train_index, test_index) in enumerate(kfold_cv.split(X, y)):
            X_train = X.iloc[train_index]
            y_train = y.iloc[train_index]
            X_test = X.iloc[test_index]
            y_test = y.iloc[test_index]

            smote = SMOTE(sampling_strategy='auto', random_state=42)
            X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

            model.fit(X_train_resampled, y_train_resampled)

            y_pred = model.predict(X_test)

            f1 = f1_score(y_test, y_pred)
            f1_scores.append(f1)

        mean_f1 = np.mean(f1_scores)

        model_dir = 'webdemo/predictive-models'
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f'final_sem_{semester}.pkl')
        joblib.dump(model, model_path)

        with transaction.atomic():
            for nilai in nilaiMahasiswa.objects.filter(semester=semester):
                update_data = {field: getattr(nilai, field) for field in fields}
                hasil_ukmppd = model.predict([list(update_data.values())])[0]
                
                solution = ""
                if hasil_ukmppd == 0:
                    nilai_dict = {field: getattr(nilai, field) for field in fields}
                    solution = evaluate_rules({**nilai_dict, 'semester': semester})

                nilai.hasil_ukmppd = hasil_ukmppd
                nilai.solution = solution
                nilai.save()

        RetrainLog.objects.create(model_semester=semester, f1_score=mean_f1)

        messages.success(request, f'Model Semester {semester} telah berhasil diperbarui')
        return redirect('index_prediksi')

    latest_f1_score = {
        '2': RetrainLog.objects.filter(model_semester='2').order_by('-retrained_date').first(),
        '3': RetrainLog.objects.filter(model_semester='3').order_by('-retrained_date').first(),
        '4': RetrainLog.objects.filter(model_semester='4').order_by('-retrained_date').first(),
    }

    latest_f1_score = {semester: log.f1_score if log else None for semester, log in latest_f1_score.items()}

    retrain_logs = RetrainLog.objects.all().order_by('-retrained_date')
    
    #Pagination
    paginator = Paginator(retrain_logs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'retrain_logs': retrain_logs,
        'latest_f1_score': latest_f1_score,
        'page_obj': page_obj
    }
    
    return render(request, 'modelPrediksi/dashboard-model.html', context)
