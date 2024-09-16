#!/bin/bash

ENDPOINT="http://127.0.0.1:5000/api_1"

# Log file to store the health check results
LOG_FILE="/var/log/health_check.log"

http_response=$(curl -s -o /dev/null -w "%{http_code}" "$ENDPOINT")

if [ "$http_response" -eq 200 ]; then
    echo "$(date): API at $ENDPOINT is reachable - Health check passed" >> "$LOG_FILE"
else
    echo "$(date): API at $ENDPOINT is unreachable - Health check failed (HTTP $http_response)" >> "$LOG_FILE"
fi


