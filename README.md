# CyberWise-Lab 

Proyecto educativo que guía, paso a paso, desde la creación de una API REST vulnerable (para prácticas de seguridad) hasta su observabilidad con métricas y logs, la construcción y publicación de imágenes en Docker Hub, el despliegue con Docker Compose/Portainer y la automatización CI/CD con GitHub Actions.

---

## 1) Propósito y alcance

* **Objetivo**: aprender a identificar, medir, monitorear y luego mitigar vulnerabilidades comunes en una API real (XSS, SQLi, CSRF-like por CORS abierto, errores 5xx, ausencia de autenticación robusta).
* **Alcance**: incluye arquitectura de la API, KPIs de seguridad, métricas (Prometheus), dashboards (Grafana/Kibana), auditoría de logs (ELK), empaquetado en contenedores, y pipelines CI/CD para publicar imágenes en Docker Hub.
* **Advertencia**: el proyecto es **educativo**. No desplegar la versión vulnerable en Internet ni con datos reales.

---

## 2) Arquitectura funcional

1. **API FastAPI (app)**

   * Capas separadas: routers (endpoints), services (lógica), repositories (SQL), utils (plantillas HTML), core (config, logging, toggles).
   * Vulnerabilidades intencionales en CRUD de clientes: inyección SQL por concatenación, XSS almacenado en render HTML, CORS permisivo, variantes form que facilitan ataques cross-origin, errores 500 “aleatorios” mediante middleware de caos (opcional según flags).
   * Endpoints de observabilidad: health (opcional) y metrics (Prometheus).

2. **Observabilidad y auditoría**

   * **Métricas**: middleware que instrumenta contadores de 2xx/4xx/5xx, histograma de latencia por ruta y contador de operaciones de escritura por IP.
   * **Logs**: formato JSON por línea con request\_id, método, ruta, latencia, estado y errores. Pensado para recolectarse con Filebeat.

3. **Stack de monitoreo**

   * **Prometheus**: scrapea la ruta /metrics de la API para KPIs y alertas.
   * **Grafana**: dashboards para p95 de latencia, tasas de 4xx/5xx, actividad de escritura por IP, etc.
   * **ELK (Elasticsearch + Logstash + Kibana) + Filebeat**: ingesta y visualización de logs de auditoría.

4. **Contenedores e imágenes**

   * Imagen de la app con un entrypoint que prepara permisos del volumen de logs y baja privilegios para ejecución.
   * Publicación en Docker Hub bajo el repositorio indicado por el autor (por ejemplo, blandskron/vuln-lab).

---

## 3) Toggle de características (modo “lab” vs. “safe”)

Variables de entorno permiten activar o desactivar componentes sin cambiar código:

* Observabilidad: ENABLE\_HEALTH, ENABLE\_METRICS, ENABLE\_AUDIT, ENABLE\_REQUEST\_ID.
* Mitigaciones (pensadas para la fase de reforzamiento): SQL\_PARAMS\_ON (consultas parametrizadas), XSS\_ESCAPE\_ON (escape/sanitización de HTML), CORS\_SAFE\_ON (lista blanca de orígenes y sin credenciales).
* Logging: LOG\_FILE y nivel/formato.
* Entorno: ENV con valores “lab” o “safe”.

Con todo desactivado (modo lab), la API mantiene la superficie vulnerable para el laboratorio. Con los flags “ON” (modo safe), se reduce el riesgo conforme a la parte de mitigación.

---

## 4) Métricas, KPIs y dashboards

* **Exposición de métricas**: la ruta /metrics entrega series Prometheus estándar del servicio (requests totales por método/ruta/estado, errores 4xx y 5xx, histograma de latencia, escrituras por IP).
* **KPIs recomendados** (cada uno con fórmula, frecuencia y herramienta):

  * Tasa de 5xx: increase(api\_errors\_5xx\_total\[1h]) dividido por increase(api\_requests\_total\[1h]); frecuencia 1–5 minutos; visualizar en Grafana; alertar en Prometheus.
  * Tasa de 4xx: increase(api\_errors\_4xx\_total\[1h]) dividido por increase(api\_requests\_total\[1h]); frecuencia 1–5 minutos; Grafana/Prometheus.
  * Latencia p95: histogram\_quantile 0.95 sobre api\_request\_seconds\_bucket (ventana 5 minutos); frecuencia continua; Grafana/Prometheus.
  * Escrituras por IP: sum(increase(api\_write\_ops\_total\[10m])) segmentado por IP; frecuencia 1–10 minutos; detección de abuso/bots; Grafana/Prometheus.
* **Dashboards**:

  * Grafana: panels para p95, tasas de 4xx/5xx y mapa de calor de rutas con mayor latencia.
  * Kibana: visión de logs por status, método, ruta, y búsquedas por request\_id o IP.

---

## 5) Auditoría de logs (ELK)

* **Formato**: eventos JSON con timestamp, request\_id, método, ruta, query, IP cliente, user-agent, estado, latencia y detalle de error si aplica.
* **Pipeline típico**: Filebeat (lee el archivo de logs de la app) → Logstash (parsea/normaliza) → Elasticsearch (indexa por fecha) → Kibana (visualiza).
* **Notas de permisos**:

  * El contenedor de la app ejecuta un entrypoint que asegura que el volumen de logs sea escribible por el usuario de la aplicación.
  * Filebeat exige que su archivo de configuración no sea escribible por grupo/otros; en Windows/Portainer puede requerirse una imagen personalizada con el YAML incluido o usar una opción de arranque que relaje la verificación.

---

## 6) Docker: imagen y ejecución

* **Imagen de la app**: basada en Python slim, instala dependencias y corre Uvicorn.
* **Entrypoint de la app**: crea la carpeta de logs, ajusta permisos del volumen y baja privilegios antes de ejecutar el servidor.
* **Publicación**: la imagen se publica en Docker Hub con tags por PR (pr-n), SHA corto (sha-xxxxxx), latest (en merges a main) y versión semántica (si se empujan tags vX.Y.Z).

---

## 7) Stack con Docker Compose

* **Servicios**:

  * api: la aplicación FastAPI que expone /metrics y escribe logs en un volumen compartido.
  * elasticsearch, logstash, kibana, filebeat: ingesta y visualización de logs.
  * prometheus: scrapea la API y almacena series temporales.
  * grafana: dashboards con datasource Prometheus preconfigurado.
* **Red y volúmenes**:

  * Red compartida para comunicación interna.
  * Volumen app\_logs compartido entre api (escribe) y filebeat (lee).
* **Consideraciones de host**:

  * En Windows/Portainer, los permisos de archivos montados pueden aparecer abiertos; se recomienda hornear configuraciones sensibles (como filebeat.yml) dentro de su imagen o montar en modo solo lectura.
  * Si la API corre fuera del stack (en tu host), Prometheus debe apuntar a host.docker.internal:8000 (o la IP del host en Linux).

---

## 8) Portainer (despliegue simplificado)

* **Stack con variables de entorno**: se recomienda usar sustitución de variables en el Compose (por ejemplo, API\_TAG, API\_PORT, LOG\_FILE) y subir un archivo .env del stack a Portainer.
* **Servicio api**: referenciado por imagen desde Docker Hub (blandskron/vuln-lab\:latest o una etiqueta específica).
* **Logs y métricas**: el stack puede crecer para incluir Prometheus/Grafana y ELK; al usar Portainer en Windows, es especialmente útil usar imágenes personalizadas para evitar problemas de permisos en archivos montados.

---

## 9) CI/CD con GitHub Actions

* **Flujo para Pull Requests**:

  * Disparador en cada PR dirigido a la rama main (abrir, actualizar, reabrir).
  * Construcción multi-arquitectura con Buildx (amd64 y arm64).
  * Publicación de la imagen en Docker Hub con tags: pr-n, sha-<commit>, y etiqueta especial del evento de PR.
  * Requiere secretos del repositorio: DOCKERHUB\_USERNAME y DOCKERHUB\_TOKEN.

* **Flujo para merge a main y para tags**:

  * En pushes a main, se publica la imagen con latest y sha-<commit>.
  * En tags vX.Y.Z, se publica además una etiqueta de versión.
  * Ambas rutas usan caché de capas para acelerar la construcción.

* **Buenas prácticas**:

  * Habilitar reglas de rama para que el build del PR sea condición de merge.
  * Mantener el Dockerfile alineado con la ubicación real de requisitos (por ejemplo, app/requirements.txt).
  * Etiquetado claro para promoción entre ambientes (pr-n para QA, latest o versiones para producción controlada en el laboratorio).

---

## 10) Alertas y respuesta a incidentes

* **Reglas de ejemplo**:

  * Errores 5xx superiores a 20 en una hora, severidad crítica.
  * Latencia p95 mayor a 1 segundo sostenida por 10 minutos, severidad warning.
  * Aumento anómalo de respuestas 4xx por mal uso del API.
  * Picos de operaciones de escritura desde una misma IP (posible abuso).
* **Notificaciones**: integrables con Prometheus Alertmanager o soluciones tipo ElastAlert para ELK. En entornos reales, enviar a Slack, correo o PagerDuty.
* **Acciones sugeridas**:

  * Revisar logs por request\_id en Kibana.
  * Correlacionar rutas, IPs y user-agents con spikes en métricas.
  * Conmutar flags de mitigación si el incidente lo requiere.

---

## 11) Mitigación y reforzamiento (Parte 4)

* **Medidas técnicas**:

  * Consultas parametrizadas en repositorios SQL (evita inyección).
  * Escape/sanitización de contenido antes de renderizar HTML (mitiga XSS almacenado).
  * Política CORS estricta y sin credenciales para orígenes no confiables; uso de tokens CSRF si se reintroduce autenticación basada en cookies.
* **Impacto en el riesgo**:

  * Reducción de la probabilidad de ejecución de scripts en el cliente.
  * Menor superficie de inyección y de exfiltración de datos.
  * Disminución de operaciones cross-origin no deseadas.
* **Verificación posterior**:

  * Repetición de pruebas de penetración básicas (búsquedas SQLi, carga de payloads XSS, intentos de solicitudes desde otros orígenes).
  * Confirmación en métricas y logs de la ausencia de situaciones anómalas comparadas con la línea base previa.

---

## 12) Problemas comunes y cómo resolverlos

* **ImportError por imports relativos**: ejecutar siempre la app desde la raíz del proyecto (uvicorn app.main\:app) y asegurar que existan archivos **init**.py en los paquetes; preferir imports absolutos tipo “from app…”.
* **PermissionError al escribir logs**: el entrypoint del contenedor prepara permisos del volumen de logs y ejecuta la app con un usuario no root; en despliegues locales, verificar que la ruta configurada en LOG\_FILE exista y sea escribible.
* **Filebeat rechaza el filebeat.yml**: no puede ser escribible por grupo/otros; en Windows/Portainer, se recomienda hornear el archivo dentro de la imagen o arrancar con un flag que relaje la verificación; idealmente mantener permisos 0644 y propietario root.
* **Ruta de requirements en Dockerfile**: si los requisitos están en app/requirements.txt, el Dockerfile debe copiar desde esa ruta; mantener coherencia con el repositorio para evitar fallos en CI.
* **Prometheus sin objetivo UP**: confirmar que Prometheus apunte a api:8000/metrics dentro del stack; si la API está fuera de Docker, usar host.docker.internal:8000 (o IP del host en Linux).

---

## 13) Qué aprendiste con este proyecto

* A **construir una API** con separación por capas y comprender puntos de falla típicos de seguridad.
* A **instrumentar métricas y logs** para observabilidad real y análisis forense.
* A **empaquetar y publicar** imágenes en Docker Hub con buenas prácticas de permisos.
* A **desplegar un stack** de monitoreo con Prometheus/Grafana y ELK.
* A **automatizar el ciclo** de build y publicación con GitHub Actions, activado por PRs y merges.
* A **definir KPIs y alertas** para seguridad, y a **mitigar** de forma gradual con toggles.

---

## 14) Licencia y uso

* Proyecto con fines **educativos**. Úsalo en entornos controlados.
* No expongas la versión vulnerable a Internet ni la utilices con información sensible.
* Ajusta los toggles de mitigación antes de cualquier demostración pública o evaluación fuera de laboratorio.
