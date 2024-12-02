from django.shortcuts import render

# Create your views here.
def modelPrediksi(request):
    return render(request, 'modelPrediksi/dashboard-model.html')