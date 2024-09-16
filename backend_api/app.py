import os
import random
import time
from flask import Flask, jsonify
import requests

app = Flask(__name__)


# Retrieve environment-specific integration key
environment = os.getenv('ENVIRONMENT', 'development')
integration_keys = {
    'development': os.getenv('DEVELOPMENT_EXTERNAL_INTEGRATION_KEY'),
    'acceptance': os.getenv('ACCEPTANCE_EXTERNAL_INTEGRATION_KEY'),
    'production': os.getenv('PRODUCTION_EXTERNAL_INTEGRATION_KEY')
}
integration_key = integration_keys.get(environment)

def generate_log():
    logs = [
        "Success",
        "Created",
        "Failed",
    ]
    return random.choice(logs)

@app.route('/download_external_logs', methods=['GET'])
def download_external_logs():
    if not integration_key:
        return jsonify({"error": "Integration key not found"}), 500

    # you need to replace the api with the actual URL
    external_api_url = "https://dummyapi.com/logs"

    headers = {
        "Authorization": f"Bearer {integration_key}"
    }

    # Dummy response 
    dummy_response = {
        "log_message": generate_log()
    }

    try:
        # you can comment the following lines and uncomment the dummy to test 
        response = requests.get(external_api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200

        # Return the dummy response instead
        return jsonify(dummy_response), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api_1')
def api_call():
    log_message = generate_log()
    print(f"Operation log: {log_message}")
    time.sleep(0.5)  # Wait for half a second
    return f"completed: {log_message}"

@app.route('/health_check')
def health_check():
    return "healthy"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
