import re
from paddleocr import PaddleOCR

# This is the 'bulletproof' way to initialize PaddleOCR 
# It avoids using arguments that are causing version conflicts
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def extract_aadhaar_logic(image_path):
    # Pass use_gpu=False here instead of in the constructor
    result = ocr_model.ocr(image_path, cls=True)
    
    if not result or not result[0]:
        return None

    text_lines = [line[1][0] for line in result[0]]
    full_text = " ".join(text_lines)
    
    clean_text = re.sub(r'[^0-9\s]', '', full_text)
    match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', clean_text)
    
    if match:
        return match.group().replace(" ", "")
    
    return None
