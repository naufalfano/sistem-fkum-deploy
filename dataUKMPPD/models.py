from django.db import models

class hasilUKMPPD (models.Model):
    mahasiswa_ID = models.IntegerField(primary_key=True)
    nama_mahasiswa = models.CharField(max_length=200)
    NIM = models.IntegerField(default=0)
    angkatan = models.CharField(max_length=20)
    periode_ukmppd = models.CharField(max_length=50)
    hasil_ukmppd = models.CharField(max_length=20)

    def __str__(self):
        return self.nama_mahasiswa