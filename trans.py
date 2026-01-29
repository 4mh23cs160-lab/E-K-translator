from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
from io import BytesIO
import base64
import requests
import json

app = Flask(__name__)


from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
from io import BytesIO
import base64
import requests
import json

app = Flask(__name__)

# Simple English to Kannada dictionary for common words/phrases
KANNADA_DICT = {
    'hello': 'ನಮಸ್ಕಾರ',
    'hi': 'ಹಾಯ್',
    'good morning': 'ಸುಪ್ರಭಾತ',
    'good night': 'ಶುಭರಾತ್ರಿ',
    'thank you': 'ಧನ್ಯವಾದ',
    'yes': 'ಹೌದು',
    'no': 'ಇಲ್ಲ',
    'please': 'ದಯವಿಟ್ಟು',
    'sorry': 'ಕ್ಷಮಿಸಿ',
    'how are you': 'ನೀವು ಹೇಗಿದ್ದೀರಿ',
    'what is your name': 'ನಿಮ್ಮ ಹೆಸರು ಏನು',
    'my name is': 'ನನ್ನ ಹೆಸರು',
    'welcome': 'ಸ್ವಾಗತ',
    'goodbye': 'ವಿದಾಯ',
    'bye': 'ಬೈ',
    'good': 'ಚೆನ್ನಾಗಿದೆ',
    'bad': 'ಹೆಚ್ಚು ಆಗಿಲ್ಲ',
    'love': 'ಪ್ರೀತಿ',
    'friend': 'ಸ್ನೇಹಿತ',
    'family': 'ಕುಟುಂಬ',
    'water': 'ನೀರು',
    'food': 'ಆಹಾರ',
    'work': 'ಕೆಲಸ',
    'school': 'ಶಾಲೆ',
    'home': 'ಮನೆ',
    'car': 'ಕಾರು',
    'book': 'ಪುಸ್ತಕ',
    'money': 'ಹಣ',
    'time': 'ಸಮಯ',
    'day': 'ದಿನ',
    'night': 'ರಾತ್ರಿ',
    'year': 'ವರ್ಷ',
    'month': 'ತಿಂಗಳು',
    'week': 'ವಾರ',
    'i love you': 'ನಾನು ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ',
    'do you speak kannada': 'ನೀವು ಕನ್ನಡ ಮಾತನಾಡುತ್ತೀರಾ',
    'english': 'ಇಂಗ್ಲಿಷ್',
    'kannada': 'ಕನ್ನಡ',
    'language': 'ಭಾಷೆ',
}


def translate_text(text, target_language='kn'):
    """Translate text using dictionary and fallback to API"""
    try:
        text_lower = text.lower().strip()
        
        # Check dictionary first
        if text_lower in KANNADA_DICT:
            return KANNADA_DICT[text_lower]
        
        # Try to translate using Google Translate via web interface
        url = "https://translate.googleapis.com/translate_a/element.js"
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': target_language,
            'text': text
        }
        
        # Use alternative: try the simple Google Translate API
        try:
            from urllib.parse import quote
            simple_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_language}&dt=t&q={quote(text)}"
            response = requests.get(simple_url, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result and result[0] and result[0][0]:
                    return result[0][0][0]
        except:
            pass
        
        # Fallback: return original text if translation fails
        return text
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text

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
        
        # Translate English to Kannada using MyMemory API
        translated_text = translate_text(text, target_language='kn')
        
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


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
