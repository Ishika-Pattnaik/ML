import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from engine import extract_aadhaar_logic
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) # Crucial: Allows your main project's domain to access this API

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/extract-aadhaar', methods=['POST'])
def api_route():
    # Check if a file was actually sent
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Process the image using your engine
        aadhaar_number = extract_aadhaar_logic(filepath)

        # Cleanup: Delete the file after processing to save server space
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
                "message": "Aadhaar number not found in image"
            }), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Bind to PORT environment variable for Render/Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
