import uuid

from django.db import models


class SystemComponent(models.Model):
    class SourceType(models.TextChoices):
        SIMULATED = 'SIMULATED', 'Simulated'
        CONNECTOR = 'CONNECTOR', 'Real connector'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    component_type = models.CharField(max_length=60)
    description = models.TextField(blank=True, default='')
    environment = models.CharField(max_length=60, default='demo')
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.SIMULATED)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['component_type', 'is_active'])]

    def __str__(self) -> str:
        return self.name


class MetricRecord(models.Model):
    class MetricType(models.TextChoices):
        CPU = 'CPU', 'CPU'
        MEMORY = 'MEMORY', 'Memory'
        AVAILABILITY = 'AVAILABILITY', 'Availability'
        LATENCY = 'LATENCY', 'Latency'
        ERROR_RATE = 'ERROR_RATE', 'Error rate'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.ForeignKey(SystemComponent, on_delete=models.CASCADE, related_name='metrics')
    metric_type = models.CharField(max_length=20, choices=MetricType.choices)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    measured_at = models.DateTimeField()
    source = models.CharField(max_length=60, default='simulated')
    is_simulated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-measured_at']
        indexes = [
            models.Index(fields=['component', 'metric_type', 'measured_at']),
            models.Index(fields=['measured_at']),
        ]

    def __str__(self) -> str:
        return f'{self.component.name} {self.metric_type}={self.value}'


class HealthCheck(models.Model):
    class Status(models.TextChoices):
        HEALTHY = 'HEALTHY', 'Healthy'
        WARNING = 'WARNING', 'Warning'
        CRITICAL = 'CRITICAL', 'Critical'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.ForeignKey(SystemComponent, on_delete=models.CASCADE, related_name='health_checks')
    status = models.CharField(max_length=10, choices=Status.choices)
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    summary = models.CharField(max_length=255)
    checked_at = models.DateTimeField()
    rules_version = models.CharField(max_length=20, default='1.0')
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-checked_at']
        indexes = [models.Index(fields=['component', 'checked_at'])]

    def __str__(self) -> str:
        return f'{self.component.name} {self.status}'


class Alert(models.Model):
    class Severity(models.TextChoices):
        WARNING = 'WARNING', 'Warning'
        CRITICAL = 'CRITICAL', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        ACKNOWLEDGED = 'ACKNOWLEDGED', 'Acknowledged'
        RESOLVED = 'RESOLVED', 'Resolved'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.ForeignKey(SystemComponent, on_delete=models.CASCADE, related_name='alerts')
    health_check = models.ForeignKey(HealthCheck, on_delete=models.SET_NULL, null=True, blank=True, related_name='alerts')
    severity = models.CharField(max_length=10, choices=Severity.choices)
    title = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['component', 'status', 'severity'])]

    def __str__(self) -> str:
        return f'{self.component.name} {self.severity} {self.status}'


class DiagnosticReport(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.ForeignKey(SystemComponent, on_delete=models.CASCADE, related_name='diagnostics')
    health_check = models.ForeignKey(HealthCheck, on_delete=models.CASCADE, related_name='diagnostics')
    provider = models.CharField(max_length=60, blank=True, default='')
    model_name = models.CharField(max_length=120, blank=True, default='')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    findings = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    limitations = models.JSONField(default=list, blank=True)
    summary = models.TextField(blank=True, default='')
    generated_at = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=60, blank=True, default='')

    class Meta:
        ordering = ['-generated_at', '-id']
        indexes = [models.Index(fields=['component', 'status'])]

    def __str__(self) -> str:
        return f'{self.component.name} diagnostic {self.status}'
