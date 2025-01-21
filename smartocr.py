import pytesseract
from PIL import Image
import logging
from typing import Optional, Dict
from .database import Database

# Language codes and their confidence thresholds
LANGUAGE_CODES = {
    'english': 'eng',
    'hindi': 'hin',
    'marathi': 'mar',
    'punjabi': 'pan',
    'gujarati': 'guj'
}

class SmartOCR:
    def __init__(self, db_name: str = 'ocr_results.db', tesseract_path: Optional[str] = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.db = Database(db_name)
        
        # Verify installed languages
        self.verify_languages()

    def verify_languages(self):
        """Verify installed Tesseract languages"""
        try:
            installed_langs = pytesseract.get_languages()
            missing_langs = []
            
            for lang in LANGUAGE_CODES.values():
                if lang not in installed_langs:
                    missing_langs.append(lang)
            
            if missing_langs:
                self.logger.warning(f"Missing language packs: {', '.join(missing_langs)}")
                print("\nTo install missing language packs:")
                print("For Ubuntu/Debian:")
                print("sudo apt-get install " + " ".join([f"tesseract-ocr-{lang}" for lang in missing_langs]))
                print("\nFor Windows:")
                print("Download language data files from: https://github.com/tesseract-ocr/tessdata")
        except Exception as e:
            self.logger.error(f"Error checking languages: {str(e)}")

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        if image.mode != 'L':
            image = image.convert('L')
        return image

    def detect_language(self, image: Image.Image) -> tuple:
        """
        Detect the language of text in the image
        Returns: (detected_language, confidence)
        """
        try:
            best_confidence = 0
            detected_lang = 'english'  # default
            
            for lang_name, lang_code in LANGUAGE_CODES.items():
                try:
                    data = pytesseract.image_to_data(image, lang=lang_code, output_type=pytesseract.Output.DICT)
                    conf_scores = [float(x) for x in data['conf'] if x != '-1']
                    if conf_scores:
                        avg_conf = sum(conf_scores) / len(conf_scores)
                        if avg_conf > best_confidence:
                            best_confidence = avg_conf
                            detected_lang = lang_name
                except:
                    continue
            
            return detected_lang, best_confidence
            
        except Exception as e:
            self.logger.error(f"Error in language detection: {str(e)}")
            return 'english', 0.0

    def extract_text(self, image_path: str) -> Dict[str, str]:
        """Extract text from image after detecting language"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            with Image.open(image_path) as img:
                processed_img = self.preprocess_image(img)
                
                # Detect language
                detected_lang, confidence = self.detect_language(processed_img)
                self.logger.info(f"Detected language: {detected_lang} with confidence: {confidence:.2f}%")
                
                # Extract text in detected language
                lang_code = LANGUAGE_CODES[detected_lang]
                text = pytesseract.image_to_string(processed_img, lang=lang_code)
                
                if text.strip():
                    result = {
                        'status': 'success',
                        'message': f'Text extracted successfully in {detected_lang}',
                        'text': text.strip(),
                        'language': detected_lang,
                        'confidence': confidence
                    }
                else:
                    result = {
                        'status': 'warning',
                        'message': f'No text extracted in {detected_lang}',
                        'text': '',
                        'language': detected_lang,
                        'confidence': confidence
                    }
                
                # Save to database
                result['id'] = self.db.save_result(
                    image_path=image_path,
                    text=result['text'],
                    language=detected_lang,
                    confidence=confidence,
                    status=result['status']
                )
                
                return result
                
        except Exception as e:
            self.logger.error(f"OCR processing error: {str(e)}")
            return {
                'status': 'error',
                'message': f"Error processing image: {str(e)}",
                'text': '',
                'language': 'unknown',
                'confidence': 0.0
            }

    def get_saved_result(self, id: int) -> Dict:
        return self.db.get_result(id)
    
    def close(self):
        self.db.close()
