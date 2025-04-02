const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US'; // Language for speech recognition
recognition.continuous = true;
recognition.interimResults = true;

let previousTranscript = ""; // Track previous transcript to filter out repetitions

recognition.onresult = async function(event) {
    let transcript = event.results[event.results.length - 1][0].transcript;
    const isFinalResult = event.results[event.results.length - 1].isFinal; // Check if the result is final

    if (isFinalResult) {
        console.log("Speech Recognized (final): ", transcript); // Log recognized text
        
        // Filter out repeated phrases or words
        if (transcript !== previousTranscript) {
            previousTranscript = transcript; // Update previous transcript to prevent repetition
            const recognizedTextElement = document.getElementById('recognizedText');
            recognizedTextElement.textContent += transcript + ' ';  // Add space for readability

            // Translate the recognized text using Azure
           spanishText = document.getElementById('recognizedText').textContent;
            console.log("Translating text...");
            const selectedLanguage = document.getElementById('languageSelect').value; // Get selected language
            const translatedText = await translateText(spanishText, selectedLanguage); // Translate to selected language
            console.log("Translated Text: ", translatedText); // Log translated text
            document.getElementById('translatedText').textContent = translatedText;
        }
    }
};

recognition.onerror = function(event) {
    console.error("Speech Recognition Error: ", event.error); // Log recognition errors
};

document.getElementById('startButton').addEventListener('click', () => {
    if (recognition.started) return; // Prevent starting multiple recognitions

    console.log("Starting speech recognition...");
    document.getElementById('startButton').disabled = true; // Disable button while recording
    recognition.start();
    recognition.started = true; // Mark recognition as started
});

async function translateText(text, targetLanguage) {
    
    const baseUrl = window.location.origin;
    const url = `/api/translate/?text=${encodeURIComponent(text)}&targetLanguage=${encodeURIComponent(targetLanguage)}`;
    const fullUrl = baseUrl + url;

    try {
        const response = await fetch(url);
        console.log(text)
        console.log(targetLanguage)


        if (!response.ok) {
            throw new Error(`Translation API request failed with status: ${response.status}`);
        }

        const data = await response.json();
        console.log("data", data[0].translations[0].text)
        return data[0].translations[0].text; // Return the translated text
    } catch (error) {
        console.error("Error during translation: ", error);
        return `Error translating text. ${error.message}`; // Provide more detailed error message
    }
}

let voices = [];

window.speechSynthesis.onvoiceschanged = () => {
    voices = window.speechSynthesis.getVoices();
    console.log("Available Voices: ", voices);
};

function speakText(text) {
    console.log("Starting text-to-speech for: ", text);
    const utterance = new SpeechSynthesisUtterance(text);

    // Wait for voices to be loaded
    if (voices.length === 0) {
        console.log("No voices available yet.");
        return;
    }

    const selectedVoice = voices.find(voice => voice.lang === 'es-ES') || voices[0]; // Fallback to first voice available
    utterance.voice = selectedVoice;

    // Event listeners
    utterance.onstart = () => {
        console.log("Speech synthesis started...");
    };

    utterance.onend = () => {
        console.log("Speech synthesis completed.");
    };

    utterance.onerror = (event) => {
        console.error("Speech synthesis error: ", event.error);
    };

    window.speechSynthesis.speak(utterance);
}


document.getElementById('speakButton').addEventListener('click', () => {
    const translatedText = document.getElementById('translatedText').textContent;
    if (translatedText) {
        console.log("Speaking translated text: ", translatedText);
        speakText(translatedText); // Speak the translated text
    } else {
        console.log("No translated text to speak.");
    }
});

recognition.onend = function() {
    document.getElementById('startButton').disabled = false; // Re-enable the start button
    recognition.started = false;
};