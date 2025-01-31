from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
    path('login/', include('users.urls')),
    path('detail-nilai/<str:NIM>', views.detailNilai, name='detail-nilai'),
    path('delete/<str:NIM>', views.deleteRecord, name='delete-nilai'),
    path('data-ukmppd/', include('dataUKMPPD.urls')),
    path('model-prediksi/', include('modelPrediksi.urls')),
    path('data-nilai/', include('dataNilai.urls'))
]
