from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api.views import (
    AlertViewSet,
    DiagnosticReportViewSet,
    HealthCheckViewSet,
    MetricRecordViewSet,
    SystemComponentViewSet,
)

router = DefaultRouter()
router.register('components', SystemComponentViewSet, basename='component')
router.register('metrics', MetricRecordViewSet, basename='metric')
router.register('health-checks', HealthCheckViewSet, basename='healthcheck')
router.register('alerts', AlertViewSet, basename='alert')
router.register('diagnostics', DiagnosticReportViewSet, basename='diagnostic')
router.register('reports', DiagnosticReportViewSet, basename='report')

urlpatterns = [path('', include(router.urls))]
