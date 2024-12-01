from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardUKMPPD),
    path('form-ukmppd/', views.uploadUKMPPD),
    path('detail-hasil/', views.detailHasilUKMPPD)
]