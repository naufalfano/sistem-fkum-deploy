from django.db import models

class hasilUKMPPD(models.Model):
    mahasiswa_ID = models.AutoField(primary_key=True)
    nama_mahasiswa = models.CharField(max_length=512)
    NIM = models.IntegerField()
    angkatan = models.CharField(max_length=20)
    periode_ukmppd = models.CharField(max_length=50)
    IPD = models.FloatField(blank=True, null=True)
    IKA = models.FloatField(blank=True, null=True)
    RAD = models.FloatField(blank=True, null=True)
    SRM = models.FloatField(blank=True, null=True)
    KDK = models.FloatField(blank=True, null=True)
    MPK = models.FloatField(blank=True, null=True)
    ANT = models.FloatField(blank=True, null=True)
    MAT = models.FloatField(blank=True, null=True)
    IKM = models.FloatField(blank=True, null=True)
    THTKL = models.FloatField(blank=True, null=True)
    KJW = models.FloatField(blank=True, null=True)
    OT2 = models.FloatField(blank=True, null=True)
    BED = models.FloatField(blank=True, null=True)
    OBG = models.FloatField(blank=True, null=True)
    FOR = models.FloatField(blank=True, null=True)
    MOI = models.FloatField(blank=True, null=True)
    ELK = models.FloatField(blank=True, null=True)
    hasil_ukmppd = models.IntegerField(choices=[(0, 'Retake'), (1, 'Lulus')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_mahasiswa

class Meta:
    db_table = 'hasilUKMPPD'