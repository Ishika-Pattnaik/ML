import re
from paddleocr import PaddleOCR

# Move initialization INSIDE the function
def extract_aadhaar_logic(image_path):
    # This only runs when an image is actually uploaded
    ocr_model = PaddleOCR(use_angle_cls=True, lang='en')
    
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
