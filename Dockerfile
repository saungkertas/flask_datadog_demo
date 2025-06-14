FROM python:3.9-slim

WORKDIR /app
COPY app /app
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code


# Install python-json-logger for structured JSON logs (optional but recommended)
RUN pip install python-json-logger

# Set environment variables to enable Datadog log injection and trace
ENV DD_LOGS_INJECTION=true
ENV DD_TRACE_ENABLED=true

# Use a custom entrypoint script to configure logging and run the app
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
