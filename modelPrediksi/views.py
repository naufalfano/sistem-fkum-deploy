from django.shortcuts import render

def modelPrediksi(request):
    return render(request, 'modelPrediksi/dashboard-model.html')