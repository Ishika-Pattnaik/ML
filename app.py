import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
# Import the logic from engine.py
from engine import extract_aadhaar_logic

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def health_check():
    """
    Critical for Render: This allows the server to bind to a port 
    instantly before the heavy ML models finish downloading.
    """
    return jsonify({"status": "API is Live"}), 200

@app.route('/extract-aadhaar', methods=['POST'])
def api_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # The ML processing happens here
        aadhaar_number = extract_aadhaar_logic(filepath)

        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)

        if aadhaar_number:
            return jsonify({
                "status": "success",
                "aadhaar_number": aadhaar_number
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Aadhaar number not detected"
            }), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Use the port assigned by Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
