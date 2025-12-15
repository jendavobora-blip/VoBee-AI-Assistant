/**
 * VoBee Voice Interface
 * 
 * This module provides voice input and output capabilities using
 * the Web Speech API for a more natural interaction with the AI system.
 * 
 * @module voice-interface
 */

/**
 * Voice Interface Class
 * Manages voice recognition and text-to-speech functionality
 */
class VoiceInterface {
    constructor() {
        this.isListening = false;
        this.isSupported = this.checkSupport();
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.currentVoice = null;
        this.settings = {
            language: 'en-US',
            continuous: false,
            interimResults: true,
            voicePitch: 1.0,
            voiceRate: 1.0,
            voiceVolume: 1.0
        };
        
        if (this.isSupported) {
            this.initializeRecognition();
            this.loadVoices();
        }
    }

    /**
     * Check if voice features are supported
     * @returns {boolean} Support status
     */
    checkSupport() {
        const hasSpeechRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
        const hasSpeechSynthesis = 'speechSynthesis' in window;
        
        return {
            recognition: hasSpeechRecognition,
            synthesis: hasSpeechSynthesis,
            full: hasSpeechRecognition && hasSpeechSynthesis
        };
    }

    /**
     * Initialize speech recognition
     */
    initializeRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech Recognition not supported');
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.lang = this.settings.language;
        this.recognition.continuous = this.settings.continuous;
        this.recognition.interimResults = this.settings.interimResults;
        this.recognition.maxAlternatives = 1;

        // Set up event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.onListeningStart && this.onListeningStart();
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.onListeningEnd && this.onListeningEnd();
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.onError && this.onError(event.error);
        };

        this.recognition.onresult = (event) => {
            this.handleRecognitionResult(event);
        };
    }

    /**
     * Handle speech recognition results
     * @param {SpeechRecognitionEvent} event - Recognition event
     */
    handleRecognitionResult(event) {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        // Callback for interim results
        if (interimTranscript && this.onInterimResult) {
            this.onInterimResult(interimTranscript);
        }

        // Callback for final results
        if (finalTranscript && this.onFinalResult) {
            this.onFinalResult(finalTranscript);
        }
    }

    /**
     * Start listening for voice input
     */
    startListening() {
        if (!this.recognition) {
            console.error('Speech recognition not initialized');
            return;
        }

        if (this.isListening) {
            console.log('Already listening');
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }

    /**
     * Stop listening for voice input
     */
    stopListening() {
        if (!this.recognition || !this.isListening) {
            return;
        }

        try {
            this.recognition.stop();
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
    }

    /**
     * Toggle voice recognition on/off
     */
    toggleListening() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    /**
     * Load available voices for text-to-speech
     */
    loadVoices() {
        if (!this.synthesis) {
            return;
        }

        const voices = this.synthesis.getVoices();
        
        if (voices.length > 0) {
            // Try to find a good English voice
            this.currentVoice = voices.find(voice => 
                voice.lang.startsWith('en') && voice.localService
            ) || voices[0];
        }

        // Some browsers load voices asynchronously
        this.synthesis.onvoiceschanged = () => {
            const newVoices = this.synthesis.getVoices();
            this.currentVoice = newVoices.find(voice => 
                voice.lang.startsWith('en') && voice.localService
            ) || newVoices[0];
        };
    }

    /**
     * Speak text using text-to-speech
     * @param {string} text - Text to speak
     * @param {Object} options - Optional speech settings
     */
    speak(text, options = {}) {
        if (!this.synthesis) {
            console.error('Speech synthesis not supported');
            return;
        }

        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        
        // Apply settings
        utterance.voice = this.currentVoice;
        utterance.pitch = options.pitch || this.settings.voicePitch;
        utterance.rate = options.rate || this.settings.voiceRate;
        utterance.volume = options.volume || this.settings.voiceVolume;
        utterance.lang = options.language || this.settings.language;

        // Event handlers
        utterance.onstart = () => {
            this.onSpeechStart && this.onSpeechStart();
        };

        utterance.onend = () => {
            this.onSpeechEnd && this.onSpeechEnd();
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event.error);
            this.onSpeechError && this.onSpeechError(event.error);
        };

        this.synthesis.speak(utterance);
    }

    /**
     * Stop current speech
     */
    stopSpeaking() {
        if (this.synthesis && this.synthesis.speaking) {
            this.synthesis.cancel();
        }
    }

    /**
     * Pause current speech
     */
    pauseSpeaking() {
        if (this.synthesis && this.synthesis.speaking) {
            this.synthesis.pause();
        }
    }

    /**
     * Resume paused speech
     */
    resumeSpeaking() {
        if (this.synthesis && this.synthesis.paused) {
            this.synthesis.resume();
        }
    }

    /**
     * Check if currently speaking
     * @returns {boolean} Speaking status
     */
    isSpeaking() {
        return this.synthesis && this.synthesis.speaking;
    }

    /**
     * Get available voices
     * @returns {Array} List of available voices
     */
    getAvailableVoices() {
        if (!this.synthesis) {
            return [];
        }
        return this.synthesis.getVoices();
    }

    /**
     * Set voice by name
     * @param {string} voiceName - Name of voice to use
     */
    setVoice(voiceName) {
        const voices = this.getAvailableVoices();
        const voice = voices.find(v => v.name === voiceName);
        
        if (voice) {
            this.currentVoice = voice;
            return true;
        }
        
        return false;
    }

    /**
     * Update settings
     * @param {Object} newSettings - New settings to apply
     */
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        
        if (this.recognition) {
            this.recognition.lang = this.settings.language;
            this.recognition.continuous = this.settings.continuous;
            this.recognition.interimResults = this.settings.interimResults;
        }
    }

    /**
     * Get current settings
     * @returns {Object} Current settings
     */
    getSettings() {
        return { ...this.settings };
    }

    /**
     * Get voice interface status
     * @returns {Object} Status information
     */
    getStatus() {
        return {
            supported: this.isSupported,
            listening: this.isListening,
            speaking: this.isSpeaking(),
            currentVoice: this.currentVoice ? this.currentVoice.name : null,
            settings: this.getSettings()
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VoiceInterface };
}
