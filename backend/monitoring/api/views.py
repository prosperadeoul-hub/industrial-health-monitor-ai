from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from monitoring.models import (
    Alert,
    DiagnosticReport,
    HealthCheck,
    MetricRecord,
    SystemComponent,
)
from monitoring.services.alert_service import create_alerts
from monitoring.services.rules_engine import evaluate

from .serializers import (
    AlertSerializer,
    DiagnosticReportSerializer,
    HealthCheckSerializer,
    MetricRecordSerializer,
    SystemComponentSerializer,
)


class SystemComponentViewSet(viewsets.ModelViewSet):
    queryset = SystemComponent.objects.all()
    serializer_class = SystemComponentSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active', 'updated_at'])


class MetricRecordViewSet(viewsets.ModelViewSet):
    queryset = MetricRecord.objects.all()
    serializer_class = MetricRecordSerializer
    filterset_fields = ['component', 'metric_type']


class HealthCheckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HealthCheck.objects.all()
    serializer_class = HealthCheckSerializer

    @action(detail=False, methods=['post'], url_path='run')
    def run(self, request):
        component_id = request.data.get('component')
        from monitoring.models import SystemComponent
        try:
            component = SystemComponent.objects.get(pk=component_id, is_active=True)
        except SystemComponent.DoesNotExist:
            return Response({'detail': 'Component not found'}, status=status.HTTP_404_NOT_FOUND)
        metrics = {}
        for m in component.metrics.order_by('-measured_at')[:10]:
            metrics[m.metric_type] = m.value
        result = evaluate(metrics)
        hc = HealthCheck.objects.create(
            component=component, status=result['status'], summary=result['summary'],
            checked_at=timezone.now(), details=result['details'],
        )
        create_alerts(component, hc, result['status'])
        return Response(HealthCheckSerializer(hc).data, status=status.HTTP_201_CREATED)


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filterset_fields = ['component', 'status', 'severity']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        if alert.status == 'RESOLVED':
            return Response({'detail': 'Resolved alert cannot be reopened'}, status=status.HTTP_400_BAD_REQUEST)
        alert.status = 'ACKNOWLEDGED'
        alert.save(update_fields=['status', 'updated_at'])
        return Response(AlertSerializer(alert).data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'RESOLVED'
        alert.resolved_at = timezone.now()
        alert.save(update_fields=['status', 'resolved_at', 'updated_at'])
        return Response(AlertSerializer(alert).data)


class DiagnosticReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiagnosticReport.objects.all()
    serializer_class = DiagnosticReportSerializer
    filterset_fields = ['component', 'status']


class ComponentMetricsView(viewsets.ViewSet):
    def list(self, request, component_pk=None):
        qs = MetricRecord.objects.filter(component_id=component_pk)
        return Response(MetricRecordSerializer(qs, many=True).data)
