from django.shortcuts import render
from django.http import HttpResponse

'''
Tanpa pakai template (langsung views)
def homepage(request):
    return HttpResponse("testing views django 123")
'''

def index(request):
    return render(request,'homepage.html')