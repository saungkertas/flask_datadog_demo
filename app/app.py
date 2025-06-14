from flask import Flask, request
import logging
import sys
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

# Configure JSON logging to stdout for Datadog log collection
log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s trace_id=%(dd.trace_id)s span_id=%(dd.span_id)s')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    app.logger.info("HTTP request received", extra={
        "method": request.method,
        "path": request.path,
        "remote_addr": request.remote_addr,
    })

@app.route("/")
def hello():
    return "Hello, World!"
