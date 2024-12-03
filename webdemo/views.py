from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

'''
Tanpa pakai template (langsung views)
def homepage(request):
    return HttpResponse("testing views django 123")
'''
def index(request):
    return render(request,'homepage.html')
def logout_view(request):
    logout(request)
    return redirect('/login/')