from django.urls import path
from . import views

urlpatterns = [
    path('', views.modelPrediksi, name="index_prediksi"),
    #path('retrain_sem_2/', views.retrain_sem_2, name="retrain_sem_2"),
    #path('retrain_sem_3/', views.retrain_sem_3, name="retrain_sem_3"),
    #path('retrain_sem_4/', views.retrain_sem_4, name="retrain_sem_4"),
]