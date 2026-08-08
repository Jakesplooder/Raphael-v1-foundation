import cv2
import numpy as np
from PIL import Image
import pytesseract
import logging
from pathlib import Path

# Configure pytesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logger = logging.getLogger(__name__)

class QAError(Exception):
    pass

class BoundsError(QAError):
    pass

class ContrastError(QAError):
    pass

class OCRError(QAError):
    pass

def verify_visual_qa(image_path: Path, expected_text: str = None) -> bool:
    """
    Runs the Visual QA pipeline.
    Raises specific QAErrors on failure, or returns True on success.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise QAError(f"Failed to load image: {image_path}")

    # 1. Bounding-Box checks
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find contours using edge detection
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        raise OCRError("No content detected in image for QA.")
        
    # Get bounding box of all content
    x_min = min([cv2.boundingRect(c)[0] for c in contours])
    y_min = min([cv2.boundingRect(c)[1] for c in contours])
    x_max = max([cv2.boundingRect(c)[0] + cv2.boundingRect(c)[2] for c in contours])
    y_max = max([cv2.boundingRect(c)[1] + cv2.boundingRect(c)[3] for c in contours])
    
    img_h, img_w = img.shape[:2]
    
    # Define safe print area (5% padding)
    pad_x = int(img_w * 0.05)
    pad_y = int(img_h * 0.05)
    
    if x_min < pad_x or y_min < pad_y or x_max > (img_w - pad_x) or y_max > (img_h - pad_y):
        raise BoundsError(f"Content placed outside safe print boundaries (5% padding). "
                          f"Bounds: ({x_min},{y_min}) to ({x_max},{y_max}) on {img_w}x{img_h} image.")
        
    # 2. Contrast check
    roi = gray[y_min:y_max, x_min:x_max]
    std_dev = np.std(roi)
    if std_dev < 15: # Arbitrary minimal contrast threshold
        raise ContrastError(f"Poor text-to-background contrast (std_dev={std_dev:.2f}).")
        
    # 3. OCR Sanity Check
    # Add some padding to the ROI for Tesseract
    pad = 20
    roi_y_min = max(0, y_min - pad)
    roi_y_max = min(img_h, y_max + pad)
    roi_x_min = max(0, x_min - pad)
    roi_x_max = min(img_w, x_max + pad)
    
    pil_roi = Image.fromarray(cv2.cvtColor(img[roi_y_min:roi_y_max, roi_x_min:roi_x_max], cv2.COLOR_BGR2RGB))
    ocr_text = pytesseract.image_to_string(pil_roi).strip()
    
    # We only care that *some* text is readable if expected_text is provided
    if expected_text and not ocr_text:
        raise OCRError("Tesseract could not extract any readable text, but typography was requested.")
        
    # If the user expects text, check if we captured a reasonable fraction of it.
    if expected_text and len(ocr_text) < len(expected_text) * 0.3:
         raise OCRError(f"OCR text readability is too poor. Got: '{ocr_text}', expected something like: '{expected_text}'")

    return True
