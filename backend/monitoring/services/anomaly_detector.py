def detect_anomalies(metrics: dict) -> list[dict]:
    anomalies = []
    if metrics.get('CPU', 0) > 95:
        anomalies.append({'type': 'cpu_spike', 'severity': 'CRITICAL'})
    if metrics.get('LATENCY', 0) > 400:
        anomalies.append({'type': 'latency_spike', 'severity': 'WARNING'})
    return anomalies
