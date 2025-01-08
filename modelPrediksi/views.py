from django.shortcuts import render
from dataUKMPPD.models import hasilUKMPPD

def modelPrediksi(request):
    return render(request, 'modelPrediksi/dashboard-model.html')

def retrain_sem_2(request):
    #Ambil data training dari database
    X = hasilUKMPPD.objects.values('IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT', 'IKM', 'THTKL', 'KJW', 'OT2')
    y = hasilUKMPPD.objects.values('hasil_ukmppd')
    return render(request, 'modelPrediksi/retrain-sem-2.html')

def retrain_sem_3(request):
    #Ambil data training dari database
    X = hasilUKMPPD.objects.values('IPD', 'IKA', 'RAD', 'SRM', 'KDK', 'MPK', 'ANT', 'MAT', 'IKM', 'THTKL', 'KJW', 'OT2')
    y = hasilUKMPPD.objects.values('hasil_ukmppd')
    
    return render(request, 'modelPrediksi/retrain-sem-3.html')

def retrain_sem_4(request):
    return render(request, 'modelPrediksi/retrain-sem-4.html')