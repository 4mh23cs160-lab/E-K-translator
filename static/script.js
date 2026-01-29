document.addEventListener('DOMContentLoaded', function() {
    const englishText = document.getElementById('englishText');
    const kannadaText = document.getElementById('kannadaText');
    const translateBtn = document.getElementById('translateBtn');
    const speakEnglish = document.getElementById('speakEnglish');
    const speakKannada = document.getElementById('speakKannada');
    const message = document.getElementById('message');
    const audioPlayer = document.getElementById('audioPlayer');

    // Translate on button click
    translateBtn.addEventListener('click', translate);

    // Translate on Enter key
    englishText.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            translate();
        }
    });

    // Speak English button
    speakEnglish.addEventListener('click', function() {
        const text = englishText.value.trim();
        if (text) {
            speak(text, 'en');
        } else {
            showMessage('Please enter some text to speak', 'error');
        }
    });

    // Speak Kannada button
    speakKannada.addEventListener('click', function() {
        const text = kannadaText.value.trim();
        if (text) {
            speak(text, 'kn');
        } else {
            showMessage('Please translate first to get Kannada text', 'error');
        }
    });

    // Translate function
    async function translate() {
        const text = englishText.value.trim();

        if (!text) {
            showMessage('Please enter some English text', 'error');
            return;
        }

        translateBtn.disabled = true;
        translateBtn.classList.add('loading');
        showMessage('Translating...', '');

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (data.success) {
                kannadaText.value = data.translated;
                showMessage('Translation successful!', 'success');
            } else {
                showMessage('Error: ' + data.error, 'error');
            }
        } catch (error) {
            showMessage('Error: ' + error.message, 'error');
            console.error('Error:', error);
        } finally {
            translateBtn.disabled = false;
            translateBtn.classList.remove('loading');
        }
    }

    // Speak function
    async function speak(text, language) {
        try {
            const response = await fetch('/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: text,
                    language: language
                })
            });

            const data = await response.json();

            if (data.success) {
                audioPlayer.src = data.audio;
                audioPlayer.play();
            } else {
                showMessage('Error: ' + data.error, 'error');
            }
        } catch (error) {
            showMessage('Error: ' + error.message, 'error');
            console.error('Error:', error);
        }
    }

    // Show message function
    function showMessage(text, type) {
        message.textContent = text;
        message.className = 'message';
        if (type) {
            message.classList.add(type);
        }

        // Clear message after 3 seconds if it's a success message
        if (type === 'success') {
            setTimeout(() => {
                message.textContent = '';
                message.className = 'message';
            }, 3000);
        }
    }
});
