from django.urls import path
from . import views

urlpatterns = [
    path('detail-nilai/', views.detailNilai),
    path('form-nilai/', views.uploadNilai)
]