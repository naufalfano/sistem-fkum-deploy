from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardUKMPPD, name='index_ukmppd'),
    path('form-ukmppd/', views.uploadUKMPPD, name='form-upload-ukmppd'),
    path('upload-ukmppd', views.upload_ukmppd, name='upload-ukmppd'),
    path('detail-hasil/<str:NIM>', views.detailHasilUKMPPD, name='detail-hasil-ukmppd'),
    path('delete/<str:NIM>', views.deleteRecord, name='delete-hasil-ukmppd'),
]