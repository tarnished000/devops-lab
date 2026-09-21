# Monitoring: Prometheus + Grafana + Alertmanager

## Status

Wired into `docker-compose.yml` alongside the app stack. Written and
internally consistent (scrape targets, dashboard queries and alert rules
all reference the metric names the app actually exports), but I haven't
had a live Docker daemon in my own environment to run `docker compose up`
and watch it end to end — please do that once and sanity-check it before
trusting it in anger.

## What's here

- The app (`app/main.py`) now exposes Prometheus metrics on `/metrics`:
  request counts and latency histograms, via a small ASGI middleware.
- `monitoring/prometheus.yml` — scrapes the app and itself, loads
  `alerts.yml`, and points at Alertmanager.
- `monitoring/alerts.yml` — three rules: `AppDown`, `HighErrorRate`
  (>5% 5xx over 5m), `HighRequestLatency` (p95 > 1s over 5m).
- `monitoring/alertmanager.yml` — routes alerts to a `default` receiver
  that currently has **no real notification channel** wired up (see the
  comment in that file for how to add one, e.g. a webhook or Telegram bot).
- `monitoring/grafana/provisioning/` — auto-provisions a Prometheus
  datasource and one dashboard (`notes-app.json`: request rate, error
  rate, p95 latency) so Grafana has something useful on first boot.

## Running it

```bash
cp .env.example .env   # set a real GRAFANA_ADMIN_PASSWORD
docker compose up -d --build
```

- App: http://localhost:8080 (via nginx)
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Grafana: http://localhost:3000 (login `admin` / your `GRAFANA_ADMIN_PASSWORD`)

## Still to do

- Wire a real Alertmanager receiver (webhook/Telegram/email) instead of
  the no-op default.
- Once the Kubernetes stage is actually running on a real cluster,
  decide whether monitoring moves in-cluster (kube-prometheus-stack) or
  stays as a separate Compose stack watching it from outside.
