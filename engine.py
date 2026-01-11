import re
# Keep all your existing imports (paddleocr, easyocr, etc.) here
from paddleocr import PaddleOCR

# Initialize OCR once (outside the function) to save time
ocr_model = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

def get_aadhaar_number(image_path):
    """
    This keeps your original logic but adds a Regex filter 
    to return only the Aadhaar number.
    """
    result = ocr_model.ocr(image_path, cls=True)
    
    # Flatten the result list and extract text
    extracted_text = []
    for idx in range(len(result)):
        res = result[idx]
        if res:
            for line in res:
                extracted_text.append(line[1][0])

    # YOUR ORIGINAL LOGIC: Joining all text to find the 12-digit pattern
    full_text = " ".join(extracted_text)
    
    # Regex to find: XXXX XXXX XXXX or XXXXXXXXXXXX
    match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', full_text)
    
    if match:
        return match.group().replace(" ", "")
    return None
