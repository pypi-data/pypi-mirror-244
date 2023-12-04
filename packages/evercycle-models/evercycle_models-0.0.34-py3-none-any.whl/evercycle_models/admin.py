from django.contrib import admin
from evercycle_models.models.organization import Organization
from evercycle_models.models.workflow import Workflow
from evercycle_models.models.tracking import Tracking
from evercycle_models.models.audit import Audit
from evercycle_models.models.tracking_status import TrackingStatus

admin.site.register(Organization)
admin.site.register(Workflow)
admin.site.register(Tracking)
admin.site.register(Audit)
admin.site.register(TrackingStatus)

