Text and Speech Processing Web Application

This web application built with Flask enables users to process text and speech inputs. It allows users to upload images containing text, extract text from them using Optical Character Recognition (OCR), upload audio files for speech recognition, and translate text to different languages.

Features
1. Upload Image: Allows users to upload images containing text for OCR processing.
2. Text Extraction: Utilizes pytesseract library for extracting text from uploaded images.
3. Upload Audio: Enables users to upload audio files for speech recognition.
4. Speech Recognition: Utilizes speech_recognition library for converting speech to text.
5. Translation: Provides translation functionality using the googletrans library.

Installation

1. Clone the repository
2. Install dependencies
3. Install Tesseract-OCR:

Download and install Tesseract-OCR from https://github.com/tesseract-ocr/tesseract.

4. Set up a virtual environment (optional but recommended)
5. Run the application
6. Access the application at http://localhost:5000/.


Usage
1. Navigate to the homepage to access the main interface.
2. To extract text from an image, click on the "Upload Image" button and select an image file.
3. To transcribe speech from an audio file, click on the "Upload Audio" button and select an audio file.
4. To translate text, enter the text and select the desired target language.

Acknowledgements
1. Flask: The web framework used.
2. pytesseract: Python wrapper for Google's Tesseract-OCR Engine.
3. SpeechRecognition: Library for performing speech recognition.
4. googletrans: Google Translate API for Python.


   

