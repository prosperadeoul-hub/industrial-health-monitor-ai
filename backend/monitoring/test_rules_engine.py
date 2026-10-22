from monitoring.services.rules_engine import evaluate


def test_cpu_critical():
    r = evaluate({'CPU': 95, 'MEMORY': 50, 'AVAILABILITY': 99.5, 'LATENCY': 100})
    assert r['status'] == 'CRITICAL'


def test_missing_metric_warning():
    r = evaluate({})
    assert r['status'] == 'WARNING'
