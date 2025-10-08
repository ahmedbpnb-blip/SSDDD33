from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    n8n_webhook_url = request.args.get('n8n_url')
    if not n8n_webhook_url:
        return jsonify({"error": "n8n_url parameter is missing"}), 400

    try:
        data = request.get_json()
        
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(n8n_webhook_url, json=data, headers=headers)
        
        response.raise_for_status() 
        
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
