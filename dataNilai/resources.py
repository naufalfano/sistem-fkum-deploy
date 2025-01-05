from import_export import resources
from .models import nilaiMahasiswa

class nilaiMahasiswaResource(resources.ModelResource):
    class Meta:
        model = nilaiMahasiswa