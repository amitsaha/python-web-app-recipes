from flask import Flask, request
import prometheus_client
from prometheus_client import start_http_server, Counter

REQUEST_COUNT = Counter('request_count', 'App Request Count',
        ['app_name', 'method', 'endpoint', 'http_status'])
app = Flask(__name__)

@app.after_request
def increment_request_count(response):
    REQUEST_COUNT.labels('test_app', request.method, request.path,
            response.status_code).inc()
    return response


# Expose a metrics endpoint to return
# prometheus metrics
@app.route('/metrics')
def metrics():
    return prometheus_client.generate_latest()

@app.route('/test')
def test():
    return 'rest'

if __name__ == '__main__':
    app.run(debug=True)
