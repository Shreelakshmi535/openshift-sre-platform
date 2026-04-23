from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)
#prometheus metrics
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

@app.route('/health')
def health():
    REQUEST_COUNT.labels('GET', '/health', '200').inc()
    return jsonify({'status': 'ok', 'service': 'openshift-sre-platform'})

@app.route('/api/data')
def data():
    start = time.time()
    REQUEST_COUNT.labels('GET', '/api/data', '200').inc()
    result = jsonify({'message': 'Hello from Openshift SRE Platform'})
    REQUEST_LATENCY.labels('/api/data').observe(time.time() - start)
    return result

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)