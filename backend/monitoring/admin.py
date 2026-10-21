from django.contrib import admin

from .models import Alert, DiagnosticReport, HealthCheck, MetricRecord, SystemComponent

admin.site.register(SystemComponent)
admin.site.register(MetricRecord)
admin.site.register(HealthCheck)
admin.site.register(Alert)
admin.site.register(DiagnosticReport)
