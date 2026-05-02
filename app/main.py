from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time
import random

app = Flask(__name__)

# ── Prometheus Metrics ──────────────────────────────────────────
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint', 'status'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# ── Helper ───────────────────────────────────────────────────────
def track(method, endpoint, status, start):
    REQUEST_COUNT.labels(method, endpoint, str(status)).inc()
    REQUEST_LATENCY.labels(method, endpoint, str(status)).observe(time.time() - start)

# ── Routes ───────────────────────────────────────────────────────
@app.route('/')
def index():
    start = time.time()
    track('GET', '/', '200', start)
    return jsonify({
        'service': 'openshift-sre-platform',
        'status': 'running',
        'version': 'v2'
    })

@app.route('/health')
def health():
    start = time.time()
    time.sleep(random.uniform(0.001, 0.05))  # realistic latency
    track('GET', '/health', '200', start)
    return jsonify({
        'status': 'ok',
        'service': 'openshift-sre-platform'
    })

@app.route('/api/data')
def data():
    start = time.time()
    time.sleep(random.uniform(0.05, 0.3))    # simulate DB/API call
    track('GET', '/api/data', '200', start)
    return jsonify({
        'message': 'Hello from Openshift SRE Platform'
    })

@app.route('/api/error')
def error():
    start = time.time()
    track('GET', '/api/error', '500', start) # generates error rate data
    return jsonify({
        'error': 'Simulated internal server error'
    }), 500

@app.route('/api/slow')
def slow():
    start = time.time()
    time.sleep(random.uniform(0.6, 1.5))     # breaches P95 latency SLO
    track('GET', '/api/slow', '200', start)
    return jsonify({
        'message': 'Slow response - latency SLO breach simulation'
    })

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)