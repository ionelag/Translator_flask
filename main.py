from flask import *
from flask_session import Session
import os
from fileinput import filename
import pytesseract
import uuid
from werkzeug.utils import secure_filename
import speech_recognition as sr
from speech_recognition import AudioFile
from googletrans import Translator


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somethingmvbdffre'
#app.secret_key = secrets.token_urlsafe(16)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_AUDIO_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['ALLOWED_AUDIO_EXTENSIONS'] = ALLOWED_AUDIO_EXTENSIONS

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_audio_file(filename):
    ALLOWED_AUDIO_EXTENSIONS = set(['wav'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

app.config['UPLOAD_FOLDER'] = 'uploads'  # Set a folder for storing uploaded files
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/upload_image', methods=['POST'])
def uploadFiles():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        f = request.files['file']

        if not f:
            flash('No file uploaded', 'error')
            return redirect(request.url)

        if not allowed_file(f.filename):
            flash('Invalid file!', 'error')
            return redirect(request.url)

        imageName = str(uuid.uuid4())
        imagePath = os.path.join(app.config['UPLOAD_FOLDER'], imageName)

        f.save(imagePath)

        if not os.path.exists(imagePath):
            flash('Failed to save uploaded file', 'error')
            return redirect(request.url)

        try:
            imageText = pytesseract.image_to_string(imagePath)
            os.remove(imagePath)  # Delete the image to save space
            return render_template("image_uploaded_successfully.html", name=f.filename, imageText=imageText)
        except Exception as e:
            flash(f'Error in OCR: {e}', 'error')
            return redirect(request.url)

    flash('Invalid request method', 'error')
    return redirect(url_for('main'))



@app.route('/upload_audio', methods=['POST'])
def uploadAudio():
    if request.method == 'POST':
        if 'audio' not in request.files:
            flash('No audio file part', 'error')
            return redirect(request.url)

        audio_file = request.files['audio']

        if not audio_file:
            flash('No audio file uploaded', 'error')
            return redirect(request.url)

        if not allowed_audio_file(audio_file.filename):
            flash('Invalid file!', 'error')
            return redirect(request.url)

        audio_name = str(uuid.uuid4()) + '.wav'
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_name)

        audio_file.save(audio_path)

        if not os.path.exists(audio_path):
            flash('Failed to save uploaded audio file', 'error')
            return redirect(request.url)
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source) #duration=
            text = recognizer.recognize_sphinx(audio_data)
            os.remove(audio_path)  # Delete the audio file to save space
            return render_template("audio_uploaded_succesfully.html", name=audio_file.filename, text=text)
        except Exception as e:
            flash(f'Error in audio recognition: {e}', 'error')
            return redirect(request.url)

    flash('Invalid request method', 'error')
    return redirect(url_for('main'))

@app.route('/translated_text', methods=['POST'])
def translate_text():
    if request.method == 'POST':
        text_to_translate = request.form.get('text_to_translate')
        language = request.form.get('language')
        translator = Translator()
        translated_text = translator.translate(text_to_translate, src='auto', dest=language)
        return translated_text.text

@app.route('/invalid_file')
def invalid_file():
    return render_template("invalid_file.html")

#@app.route('/delete/<filename>', methods=['POST'])
#def delete_file(filename):
#    if request.method == 'POST':
#        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#if os.path.exists(file_path):
#            os.remove(file_path)
#       return redirect(url_for('main'))
#    return 'Method Not Allowed'


if __name__ == "__main__":
    app.run(debug=True)