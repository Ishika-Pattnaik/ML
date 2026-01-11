import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from engine import get_aadhaar_number
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) # Allows your main project to talk to this API

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Calling your original logic
        aadhaar_no = get_aadhaar_number(filepath)
        
        # Clean up the file after processing
        os.remove(filepath)
        
        if aadhaar_no:
            return jsonify({"success": True, "aadhaar_number": aadhaar_no})
        else:
            return jsonify({"success": False, "message": "Aadhaar number not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Essential for Render/Railway deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
