from django.db import models
from .organization import Organization


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, models.CASCADE)
