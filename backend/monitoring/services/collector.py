import random
from datetime import UTC, datetime

from monitoring.models import MetricRecord, SystemComponent


class SimulatedCollector:
    def collect(self, component: SystemComponent) -> list[MetricRecord]:
        metrics = {
            'CPU': random.uniform(10, 99),
            'MEMORY': random.uniform(20, 95),
            'AVAILABILITY': random.uniform(90, 100),
            'LATENCY': random.uniform(10, 600),
        }
        units = {'CPU': '%', 'MEMORY': '%', 'AVAILABILITY': '%', 'LATENCY': 'ms'}
        now = datetime.now(UTC)
        records = []
        for mtype, value in metrics.items():
            records.append(MetricRecord.objects.create(
                component=component, metric_type=mtype, value=round(value, 2),
                unit=units[mtype], measured_at=now, source='simulated', is_simulated=True,
            ))
        return records
