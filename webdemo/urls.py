from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('login/', include('users.urls')),
    path('data-ukmppd/', include('dataUKMPPD.urls')),
    path('model-prediksi/', include('modelPrediksi.urls')),
    path('data-nilai/', include('dataNilai.urls'))
]
