# Day 5 — Validated SLO Queries

## Metrics
- `app_requests_total` — counter, labels: method, endpoint, status
- `app_request_latency_seconds` — histogram, buckets: 0.005→5.0s

## Queries
### Availability
sum(rate(app_requests_total{status="200"}[5m])) / sum(rate(app_requests_total[5m]))

### Error Rate
sum(rate(app_requests_total{status="500"}[5m])) / sum(rate(app_requests_total[5m]))

### P95 Latency
histogram_quantile(0.95, sum(rate(app_request_latency_seconds_bucket[5m])) by (le))

### Request Rate by Endpoint
sum(rate(app_requests_total[5m])) by (endpoint)
