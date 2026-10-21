# État d'avancement - Backend Industrial Health Monitor AI

## Fait
- Fondations Django 5.2, DRF, MySQL (utf8mb4), env via python-dotenv.
- Modèles : SystemComponent, MetricRecord, HealthCheck, Alert, DiagnosticReport.
- Migrations appliquées.
- Services : rules_engine, anomaly_detector, collector simulé, alert_service, diagnostic_service.
- API REST : components, metrics, health-checks (run), alerts (acknowledge/resolve), diagnostics, reports.
- Auth par session, pagination, filtres.
- OpenAPI schema/docs.
- LLM isolé (placeholder HTTP, validation JSON, fallback).

## Reste à faire
- Corriger erreurs Ruff (bare except, unused imports, style).
- Exécuter Bandit complètement.
- Ajouter tests (modèles, règles, API, permissions, LLM mock).
- Implémenter collecteur Windows/industriel (interfaces déjà prévues).
- Ajouter commande seed_demo_data.
- Rédiger README complet.
- Configurer rôles/permissions (admin, operator, reader).
- Rate limiting et audit logs.
- Transactions atomiques pour écritures liées.
- Diagnostic asynchrone réel (PENDING/COMPLETED/FAILED) si besoin.
- Export PDF sécurisé (optionnel).
