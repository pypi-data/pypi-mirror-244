from django.contrib import admin
from evercycle_models.models.organization import Organization
from evercycle_models.models.workflow import Workflow
from evercycle_models.models.tracking import Tracking
from evercycle_models.models.audit import Audit

admin.site.register(Organization)
admin.site.register(Workflow)
admin.site.register(Tracking)
admin.site.register(Audit)
