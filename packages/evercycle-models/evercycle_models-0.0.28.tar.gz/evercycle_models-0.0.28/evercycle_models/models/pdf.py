from django.db import models
from .audit import Audit

class Pdf(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    cod_id = models.CharField(max_length=50)
    audit = models.ForeignKey(Audit, models.DO_NOTHING)
    status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pdf'
