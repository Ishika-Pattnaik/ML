from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from engine import extract_details  # Ensure engine.py is in the same folder

app = Flask(__name__)

# 1. ENABLE CORS: This is vital so the other guy's repo can call your Mac
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure where to save uploaded images temporarily
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    """Serves the dashboard to you or anyone hitting the URL in a browser."""
    return render_template('index.html')

@app.route('/extract', methods=['POST', 'OPTIONS'])
def upload_file():
    # Handle the 'Preflight' request sent by browsers during cross-domain calls
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded", "is_valid_ocr": False}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file", "is_valid_ocr": False}), 400

    # Save the file temporarily
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        # 2. TRIGGER YOUR ENGINE
        data = extract_details(filepath)
        
        # 3. ADD INTEGRATION HELPERS
        # This allows the other guy to just check 'if (data.is_valid_ocr)'
        has_name = data.get('Name') != "Not Found"
        has_aadhar = data.get('Aadhaar Number') != "Not Found"
        data['is_valid_ocr'] = has_name and has_aadhar
        
        # Log the result in your terminal so you can see what's happening
        print(f"[*] Processed {file.filename} | Match Ready: {data['is_valid_ocr']}")
        
        return jsonify(data)

    except Exception as e:
        print(f"[!] System Error: {str(e)}")
        return jsonify({"error": "Server processing error", "is_valid_ocr": False}), 500
    
    finally:
        # 4. CLEANUP: Delete the image so your Mac doesn't fill up with sensitive data
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    # 0.0.0.0 makes the server public on your network
    # port 5000 is what you are forwarding via Ngrok
    app.run(host='0.0.0.0', port=5000, debug=True)
