from flask import Flask, request, jsonify
import threading
import json
import numpy as np
import logging
from utils import generate_embedding

app = Flask(__name__)

@app.route('/.well-known/ready', methods=['GET'])
def readiness_check():
    return "Ready", 200

@app.route('/meta', methods=['GET'])
def readiness_check_2():
    return jsonify({'status': 'Ready'}), 200


@app.route('/vectors', methods=['POST']) 
def vectorize():
    """
    Accepts:
      - {"text": "single string"}
      - {"text": ["string1", "string2", ...]}
    Returns:
      - {"vector": [floats]} for single input
      - {"vector": [[floats], [floats], ...]} for list input
    """
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            # Fallback if content-type wasn't JSON
            raw = request.data.decode("utf-8").strip()
            payload = json.loads(raw) if raw else {}

        # Allow both {"text": "..."} and {"text": ["...", "..."]}
        text = payload.get('text', payload)
        if isinstance(text, list):
            vectors = [generate_embedding(t) for t in text]  # list of vectors
        else:
            vectors = generate_embedding(text)  # single vector

        return jsonify({'vector': vectors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Keep Flask quiet during vectorization    
app.logger.disabled = True
# Get the Flask app's logger
# Set logging level (ERROR or CRITICAL suppresses routing logs)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


# Local run entrypoint 
if __name__ == '__main__':
    # Host 0.0.0.0 so Weaviate (same machine) can reach it via 127.0.0.1
    app.run(host='0.0.0.0', port=5000, debug=False)

