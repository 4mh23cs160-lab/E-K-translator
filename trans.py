from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
from io import BytesIO
import base64

app = Flask(__name__)
translator = Translator()

# Create a folder for temporary audio files if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

if not os.path.exists('static/audio'):
    os.makedirs('static/audio')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Translate English to Kannada
        translation = translator.translate(text, src_language='en', dest_language='kn')
        translated_text = translation['text']
        
        return jsonify({
            'original': text,
            'translated': translated_text,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/speak', methods=['POST'])
def speak():
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')  # 'en' for English, 'kn' for Kannada
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Map language codes to gTTS language codes
        lang_map = {
            'en': 'en',
            'kn': 'kn'
        }
        
        lang_code = lang_map.get(language, 'en')
        
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Save to BytesIO object
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        # Convert to base64 for sending to frontend
        audio_base64 = base64.b64encode(audio_fp.read()).decode('utf-8')
        
        return jsonify({
            'audio': f'data:audio/mp3;base64,{audio_base64}',
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
