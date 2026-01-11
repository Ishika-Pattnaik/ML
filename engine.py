import re
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

# Initialize model once. use_gpu=False is required for most free hosting tiers.
ocr_model = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)

def extract_aadhaar_logic(image_path):
    # Run OCR
    result = ocr_model.ocr(image_path, cls=True)
    
    if not result or not result[0]:
        return None

    # Combine all detected text into one string
    text_lines = [line[1][0] for line in result[0]]
    full_text = " ".join(text_lines)
    
    # Remove everything except numbers and spaces
    clean_text = re.sub(r'[^0-9\s]', '', full_text)
    
    # Look for the 12-digit Aadhaar pattern (e.g., 1234 5678 9012 or 123456789012)
    match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', clean_text)
    
    if match:
        # Return only the digits (remove spaces)
        return match.group().replace(" ", "")
    
    return None
