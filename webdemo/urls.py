from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('', include('django.contrib.auth.urls')),
    path('login/', include('users.urls')),
    path('data-ukmppd/', include('dataUKMPPD.urls'))
]
