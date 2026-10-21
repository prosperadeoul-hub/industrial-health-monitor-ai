from rest_framework import serializers

from monitoring.models import (
    Alert,
    DiagnosticReport,
    HealthCheck,
    MetricRecord,
    SystemComponent,
)


class SystemComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemComponent
        fields = ['id', 'name', 'component_type', 'description', 'environment', 'source_type', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MetricRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricRecord
        fields = ['id', 'component', 'metric_type', 'value', 'unit', 'measured_at', 'source', 'is_simulated', 'created_at']
        read_only_fields = ['id', 'created_at']


class HealthCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCheck
        fields = ['id', 'component', 'status', 'score', 'summary', 'checked_at', 'rules_version', 'details']
        read_only_fields = ['id', 'status', 'summary', 'checked_at', 'rules_version', 'details']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'component', 'health_check', 'severity', 'title', 'description', 'status', 'created_at', 'updated_at', 'resolved_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DiagnosticReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticReport
        fields = ['id', 'component', 'health_check', 'provider', 'model_name', 'status', 'findings', 'recommendations', 'limitations', 'summary', 'generated_at', 'error_code']
        read_only_fields = ['id', 'status', 'generated_at']
