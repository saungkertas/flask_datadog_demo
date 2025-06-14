#!/bin/sh

# Run the Flask app with ddtrace-run (auto-instrumentation for traces)
exec ddtrace-run gunicorn --bind 0.0.0.0:5000 app:app
