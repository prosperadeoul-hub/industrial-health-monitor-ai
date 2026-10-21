RULES_VERSION = '1.0'

THRESHOLDS = {
    'CPU': (70.0, 90.0),
    'MEMORY': (75.0, 90.0),
    'AVAILABILITY': (99.0, 95.0),
    'LATENCY': (200.0, 500.0),
}


def evaluate(metrics: dict) -> dict:
    results = []
    worst = 'HEALTHY'
    order = {'HEALTHY': 0, 'WARNING': 1, 'CRITICAL': 2}
    for mtype, (w, c) in THRESHOLDS.items():
        val = metrics.get(mtype)
        if val is None:
            status = 'WARNING'
            reason = 'missing'
        else:
            if mtype in ('CPU', 'MEMORY', 'LATENCY'):
                if val >= c:
                    status = 'CRITICAL'
                elif val >= w:
                    status = 'WARNING'
                else:
                    status = 'HEALTHY'
            else:
                if val < c:
                    status = 'CRITICAL'
                elif val < w:
                    status = 'WARNING'
                else:
                    status = 'HEALTHY'
            reason = 'threshold'
        results.append({'metric': mtype, 'value': val, 'status': status, 'reason': reason})
        if order[status] > order[worst]:
            worst = status
    summary = 'All metrics within thresholds' if worst == 'HEALTHY' else f'{worst} condition detected'
    return {'status': worst, 'summary': summary, 'details': results, 'rules_version': RULES_VERSION}
