from django.contrib import admin
from evercycle_models.models.organization import Organization
from evercycle_models.models.workflow import Workflow
from evercycle_models.models.tracking import Tracking

admin.site.register(Organization)
admin.site.register(Workflow)
admin.site.register(Tracking)
