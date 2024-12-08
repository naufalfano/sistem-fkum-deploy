from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def detailNilai(request):
    return render(request, 'dataNilai/detail-nilai.html')

def uploadNilai(request):
    return render(request, 'dataNilai/form-upload-nilai.html')