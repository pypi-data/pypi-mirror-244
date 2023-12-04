from django.db import models

class ServiceProviderServices(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    service_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'service_provider_services'
