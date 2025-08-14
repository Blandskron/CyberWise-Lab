# Observabilidad y Auditoría

## Ejecutar stack ELK local
```bash
cd infra
docker compose -f docker-compose.obsv.yml up -d
````

* ES: [http://localhost:9200](http://localhost:9200)
* Kibana: [http://localhost:5600](http://localhost:5600)
* Logstash: puerto 5044 (beats)
* Filebeat lee `../logs/app.log`

## App (variables)

* `.env` basado en `.env.example`
* Habilitar /health y /metrics: `ENABLE_HEALTH=true`, `ENABLE_METRICS=true`

## Métricas Prometheus

* `GET /metrics` expone:

  * `api_requests_total{method,path,status}`
  * `api_errors_5xx_total`
  * `api_errors_4xx_total`
  * `api_request_seconds_bucket` (latencia)
  * `api_write_ops_total{ip}`

## KPIs sugeridos (fórmula)

* **Tasa 5xx** = `increase(api_errors_5xx_total[1h]) / increase(api_requests_total[1h])`
* **Tasa 4xx** = `increase(api_errors_4xx_total[1h]) / increase(api_requests_total[1h])`
* **Latencia p95** = `histogram_quantile(0.95, sum(rate(api_request_seconds_bucket[5m])) by (le))`
* **Write ops por IP (10m)** = `sum(increase(api_write_ops_total[10m])) by (ip)`

## Alertas (Prometheus)

* Ver `scripts/alerts/prometheus_rules.yml` (ejemplos: >20 5xx/h, p95>1s, many writes/IP).

---

### Cómo probar rápido
1) Crea carpeta de logs:
```bash
mkdir -p logs
````

2. Arranca tu API (con `/health` y `/metrics` activados en `.env`):

```bash
uvicorn app.main:app --reload --port 8000
```

3. (Opcional) Levanta ELK:

```bash
cd infra && docker compose -f docker-compose.obsv.yml up -d
```

4. Corre smoke:

```bash
./scripts/pentest/smoke_tests.sh
