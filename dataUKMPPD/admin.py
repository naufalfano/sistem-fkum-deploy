from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import hasilUKMPPD


# Register your models here.
class hasilUKMPPDResource(resources.ModelResource):
    class Meta:
        model = hasilUKMPPD
        import_id_fields = ['mahasiswa_ID']
        fields = (
            'mahasiswa_ID', 
            'nama_mahasiswa', 
            'NIM', 
            'angkatan', 
            'periode_ukmppd', 
            'hasil_ukmppd'
        )

class hasilUKMPPDAdmin(ImportExportModelAdmin):
    resource_class = hasilUKMPPDResource

admin.site.register(hasilUKMPPD, hasilUKMPPDAdmin)