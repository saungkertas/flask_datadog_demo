from flask import Flask, request, jsonify, g
import logging
import sys
import time
from pythonjsonlogger import jsonlogger
from ddtrace import patch_all
from datadog import initialize, statsd

# Enable Datadog auto-instrumentation
patch_all()

# Configure Datadog statsd client (DogStatsD)
# By default, the agent listens on localhost:8125 in Docker Compose
initialize(statsd_host='datadog', statsd_port=8125)

app = Flask(__name__)

# Configure JSON logging to stdout for Datadog log collection
log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s trace_id=%(dd.trace_id)s span_id=%(dd.span_id)s')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def before_request():
    g.start_time = time.time()
    app.logger.info("HTTP request received", extra={
        "method": request.method,
        "path": request.path,
        "remote_addr": request.remote_addr,
    })

@app.after_request
def after_request(response):
    # Calculate response time
    if hasattr(g, 'start_time'):
        duration = (time.time() - g.start_time) * 1000  # ms
        statsd.histogram('flask.response_time', duration, tags=[
            f'path:{request.path}',
            f'method:{request.method}',
            f'status_code:{response.status_code}'
        ])
        app.logger.info("HTTP request completed", extra={
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": duration
        })
    # Count failures (status code >= 400)
    if response.status_code >= 400:
        statsd.increment('flask.request_failure', tags=[
            f'path:{request.path}',
            f'method:{request.method}',
            f'status_code:{response.status_code}'
        ])
    return response

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/fail")
def fail():
    # Simulate a failure
    return jsonify({"error": "Simulated failure"}), 500

# Optional: simulate a 404 by not defining a route for /notfound

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
