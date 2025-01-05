from django.urls import path
from . import views

urlpatterns = [
    path('detail-nilai/<str:NIM>', views.detailNilai, name='detail-nilai'),
    path('form-nilai/', views.uploadNilai, name='form-upload-nilai'),
    path('upload-nilai', views.upload_nilai, name='upload-nilai'),
]