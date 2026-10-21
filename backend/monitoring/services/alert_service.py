from monitoring.models import Alert, HealthCheck, SystemComponent


def create_alerts(component: SystemComponent, health_check: HealthCheck, status: str) -> None:
    if status == 'HEALTHY':
        return
    severity = 'CRITICAL' if status == 'CRITICAL' else 'WARNING'
    exists = Alert.objects.filter(component=component, severity=severity, status='OPEN').exists()
    if not exists:
        Alert.objects.create(
            component=component, health_check=health_check, severity=severity,
            title=f'{severity} on {component.name}', description=health_check.summary,
        )
