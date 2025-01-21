# OCR Application

This repository contains a Python-based Optical Character Recognition (OCR) application capable of extracting text from images, detecting languages, and storing results in a database. The application leverages Tesseract-OCR and supports multiple languages.

## Features

- **Language Detection:** Automatically detects the language of the text in the image.
- **Multi-Language Support:** Supports English, Hindi, Marathi, Punjabi, and Gujarati.
- **Text Extraction:** Extracts text from images with language-specific accuracy.
- **Database Integration:** Stores results, including detected text, language, confidence, and timestamps, in a SQLite database.
- **Preprocessing:** Optimizes images for improved OCR performance.

## Project Structure

```
.
├── database.py         # Database class for managing SQLite operations
├── smart_ocr.py        # Core OCR logic and language detection
├── main.py             # Entry point of the application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

## Prerequisites

- Python 3.7 or later
- Tesseract-OCR installed on your system
- Language data files for Tesseract

### Installing Tesseract-OCR

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng tesseract-ocr-hin tesseract-ocr-mar tesseract-ocr-pan tesseract-ocr-guj
```

#### Windows:
1. Download and install Tesseract-OCR from [here](https://github.com/tesseract-ocr/tesseract).
2. Add Tesseract to your system's PATH.
3. Download additional language data files from [tessdata](https://github.com/tesseract-ocr/tessdata) and place them in the `tessdata` directory.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ocr-application.git
cd ocr-application
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare an image file for OCR.
2. Run the application:
```bash
python main.py
```

3. The application will process the image, detect the language, extract the text, and save the results to the database.

## Configuration

- `LANGUAGE_CODES` in `smart_ocr.py` defines the supported languages and their Tesseract codes.
- Update the Tesseract-OCR path if necessary in `smart_ocr.py`.

## Example Output

```
Processing image...

Detected Language: english
Confidence: 92.15%

Extracted Text:
--------------------------------------------------
This is a sample text extracted from the image.
```

## Database

Results are stored in `ocr_results.db`. Use any SQLite viewer to access the data.

Table Structure:
- `id`: Unique identifier
- `image_path`: Path to the processed image
- `extracted_text`: Text extracted from the image
- `detected_language`: Detected language
- `confidence`: Confidence level of language detection
- `processed_date`: Timestamp of processing
- `status`: Status of the operation

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
