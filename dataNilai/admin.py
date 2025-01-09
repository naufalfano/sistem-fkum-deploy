from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import caseRetake

class caseRetakeResource(resources.ModelResource):
    class Meta:
        model = caseRetake
        import_id_fields = ['case_ID']
        fields = (
            'case_ID',
            'case',
            'semester',
            'IPD',
            'IKA',
            'RAD',
            'SRM',
            'KDK',
            'MPK',
            'ANT',
            'MAT',
            'IKM',
            'THTKL',
            'KJW',
            'OT2',
            'BED',
            'OBG',
            'FOR',
            'MOI',
            'ELK',
            'solution'
        )

@admin.register(caseRetake)
class caseRetakeAdmin(ImportExportModelAdmin):
    resource_class = caseRetakeResource