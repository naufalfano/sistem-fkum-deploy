from django.db import models

class RetrainLog(models.Model):
    model_semester = models.CharField(max_length=20)
    f1_score = models.FloatField()
    retrained_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.model_semester

class Meta:
    db_table = 'retrainLog'