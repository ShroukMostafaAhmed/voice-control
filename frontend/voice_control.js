// Voice Control System - Emma
// Fix: no confirm word spoken before executing — only speak backend result OR sorry, never both

class VoiceControl {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isEnabled = false;
        this.isAwake = false;
        this.waitingForCommand = false;
        this.voices = [];
        this.restartAttempts = 0;
        this.maxRestartAttempts = 999999;
        this.keepAliveInterval = null;
        this.isSpeaking = false;
        this.micBlocked = false;
        this.commandTimer = null;
        this.settleTimer = null;

        this.wakeResponses = [
            "I'm here.",
            "Yes?",
            "I'm listening.",
            "Go ahead.",
            "How can I help?",
            "What do you need?",
            "Tell me.",
            "I'm with you.",
        ];

        this.sorryResponses = [
            "Sorry, I didn't understand that.",
            "I didn't catch that.",
            "Could you say that again?",
            "Sorry, what was that?",
            "I'm not sure what you mean.",
        ];

        this.initSpeechRecognition();
        this.initSpeechSynthesis();
        this.startKeepAlive();
    }

    getRandomResponse(list) {
        return list[Math.floor(Math.random() * list.length)];
    }

    blockMicFor(ms) {
        this.micBlocked = true;
        if (this.settleTimer) clearTimeout(this.settleTimer);
        this.settleTimer = setTimeout(() => {
            this.micBlocked = false;
            console.log('Mic unblocked.');
        }, ms);
    }

    startCommandTimer() {
        if (this.commandTimer) clearTimeout(this.commandTimer);
        this.commandTimer = setTimeout(() => {
            if (this.waitingForCommand) {
                console.log('No command — sleeping.');
                this.sleep();
            }
        }, 15000);
    }

    sleep() {
        this.isAwake = false;
        this.waitingForCommand = false;
        if (this.commandTimer) clearTimeout(this.commandTimer);
        this.updateUI('listening');
        console.log('Emma sleeping.');
    }

    initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.error('Speech Recognition not supported');
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 3;

        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI('listening');
        };

        this.recognition.onresult = (event) => {
            // Hard block while Emma speaks or mic is settling
            if (this.isSpeaking || this.micBlocked) {
                console.log('Mic blocked — dropped input.');
                return;
            }

            const last = event.results.length - 1;
            if (!event.results[last].isFinal) return;

            const transcript = event.results[last][0].transcript.toLowerCase().trim();
            console.log(`Heard: "${transcript}"`);

            // --- WAKE WORD ---
            const isWakeWord =
                transcript.includes('hey emma') ||
                transcript.includes('hi emma') ||
                transcript.includes('hello emma') ||
                transcript.includes('ok emma') ||
                transcript.includes('okay emma') ||
                transcript === 'emma';

            if (isWakeWord) {
                this.isAwake = true;
                this.waitingForCommand = true;
                this.speakThen(this.getRandomResponse(this.wakeResponses), () => {
                    // block + settle after speaking, then open mic for command
                    this.blockMicFor(1500);
                    setTimeout(() => {
                        if (this.waitingForCommand) {
                            this.startCommandTimer();
                            this.updateUI('waiting');
                            console.log('Mic open — 15s to speak.');
                        }
                    }, 1500);
                });
                return;
            }

            // --- COMMAND ---
            if (this.isAwake && this.waitingForCommand) {
                if (this.commandTimer) clearTimeout(this.commandTimer);
                this.waitingForCommand = false;
                this.isAwake = false;
                // Execute directly — NO confirm word, backend result is the only response
                this.processVoiceCommand(transcript);
                return;
            }

            console.log('Ignoring — say "Hey Emma" first.');
        };

        this.recognition.onerror = (event) => {
            if (event.error === 'no-speech') return;
            if (event.error === 'not-allowed') {
                this.isListening = false;
                this.isEnabled = false;
                this.updateUI('error');
                return;
            }
            if (event.error === 'aborted' || event.error === 'network' || event.error === 'audio-capture') {
                if (this.isEnabled) {
                    this.isListening = false;
                    setTimeout(() => this.startListening(), 300);
                }
            }
        };

        this.recognition.onend = () => {
            this.isListening = false;
            if (this.isEnabled) {
                setTimeout(() => {
                    if (this.isEnabled) this.startListening();
                }, 150);
            } else {
                this.updateUI('idle');
            }
        };
    }

    initSpeechSynthesis() {
        if (this.synthesis) {
            this.loadVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = () => this.loadVoices();
            }
        }
    }

    loadVoices() {
        this.voices = this.synthesis.getVoices();
        this.selectedVoice =
            this.voices.find(v => v.lang.startsWith('en') && v.name.includes('Female')) ||
            this.voices.find(v => v.lang.startsWith('en')) ||
            this.voices[0];
    }

    startListening() {
        if (!this.recognition || this.isListening) return;
        try {
            this.recognition.start();
            this.isListening = true;
            this.restartAttempts = 0;
        } catch (error) {
            if (error.message && error.message.includes('already started')) {
                this.isListening = true;
            } else {
                this.isListening = false;
                if (this.isEnabled) setTimeout(() => this.startListening(), 500);
            }
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.isEnabled = false;
            this.recognition.stop();
            this.isListening = false;
        }
    }

    speakThen(text, callback) {
        if (!this.synthesis) {
            if (callback) callback();
            return;
        }

        this.synthesis.cancel();
        this.micBlocked = true;
        this.isSpeaking = true;

        const utterance = new SpeechSynthesisUtterance(text);
        if (this.selectedVoice) utterance.voice = this.selectedVoice;
        utterance.rate = 1.0;
        utterance.pitch = 1.1;
        utterance.volume = 1.0;

        utterance.onstart = () => {
            this.isSpeaking = true;
            this.micBlocked = true;
            this.updateUI('speaking');
            console.log(`Speaking: "${text}"`);
        };

        utterance.onend = () => {
            this.isSpeaking = false;
            this.blockMicFor(1200);
            this.updateUI('listening');
            if (callback) setTimeout(callback, 1200);
        };

        utterance.onerror = () => {
            this.isSpeaking = false;
            this.micBlocked = false;
            this.updateUI('listening');
            if (callback) callback();
        };

        this.synthesis.speak(utterance);
    }

    speak(text) {
        this.speakThen(text, null);
    }

    async processVoiceCommand(command) {
        this.displayCommand(command);
        try {
            const result = await aiClient.sendCommand(command);

            // Determine what to say — ONE response only
            let textToSpeak;

            if (result.success) {
                const response = result.ai_response || result.message || '';
                // Only use backend response if it's a real meaningful reply
                // Avoid generic backend "I'm not sure" type messages — use our own sorry instead
                const isUselessResponse =
                    response.trim().length === 0 ||
                    response.toLowerCase().includes("i'm not sure") ||
                    response.toLowerCase().includes("i don't understand") ||
                    response.toLowerCase().includes("don't know") ||
                    response.toLowerCase().includes("cannot") ||
                    response.toLowerCase().includes("can't understand");

                textToSpeak = isUselessResponse
                    ? this.getRandomResponse(this.sorryResponses)
                    : response;
            } else {
                textToSpeak = this.getRandomResponse(this.sorryResponses);
            }

            // Speak ONE thing then sleep
            this.speakThen(textToSpeak, () => {
                this.blockMicFor(1500);
                setTimeout(() => this.sleep(), 1500);
            });

            if (result.success) {
                await aiClient.syncDeviceStates();
                if (typeof apartment3D !== 'undefined' && apartment3D) {
                    apartment3D.updateDeviceStates();
                }
            }

        } catch (error) {
            console.error('Voice command error:', error);
            this.speakThen(this.getRandomResponse(this.sorryResponses), () => {
                this.blockMicFor(1500);
                setTimeout(() => this.sleep(), 1500);
            });
        }
    }

    toggle() {
        this.isEnabled = !this.isEnabled;
        if (this.isEnabled) {
            this.speak("Emma is ready. Say Hey Emma to start.");
            this.startKeepAlive();
            setTimeout(() => this.startListening(), 2000);
        } else {
            this.speak("Voice control disabled.");
            this.sleep();
            this.stopKeepAlive();
            this.stopListening();
            this.synthesis.cancel();
        }
        this.updateUI(this.isEnabled ? 'listening' : 'disabled');
        return this.isEnabled;
    }

    updateUI(state) {
        const button = document.getElementById('voice-control-btn');
        const indicator = document.getElementById('voice-indicator');
        const status = document.getElementById('voice-status');

        if (!button) return;
        button.className = 'voice-control-btn simulation-voice-btn';

        switch (state) {
            case 'listening':
                button.classList.add('listening');
                if (indicator) indicator.textContent = 'Listening...';
                if (status) status.textContent = 'Say "Hey Emma" to start';
                break;
            case 'waiting':
                button.classList.add('listening');
                if (indicator) indicator.textContent = '🟢 Speak your command...';
                if (status) status.textContent = 'Emma waiting — 15 seconds!';
                break;
            case 'speaking':
                button.classList.add('speaking');
                if (indicator) indicator.textContent = 'Emma Speaking...';
                if (status) status.textContent = 'Emma Speaking...';
                break;
            case 'idle':
                button.classList.add('active');
                if (indicator) indicator.textContent = 'Active';
                if (status) status.textContent = 'Active - Say "Hey Emma"';
                break;
            case 'disabled':
                button.classList.remove('active', 'listening', 'speaking');
                if (indicator) indicator.textContent = '🔇 Disabled';
                if (status) status.textContent = 'Click to enable';
                break;
            case 'error':
                button.classList.remove('active', 'listening', 'speaking');
                if (indicator) indicator.textContent = 'Error';
                if (status) status.textContent = 'Error - Check permissions';
                break;
        }
    }

    displayCommand(command) {
        const container = document.getElementById('voice-commands-log');
        if (!container) return;
        const timestamp = new Date().toLocaleTimeString();
        const entry = document.createElement('div');
        entry.className = 'voice-command-entry';
        entry.innerHTML = `
            <span class="voice-time">[${timestamp}]</span>
            <span class="voice-text">"${command}"</span>
        `;
        container.appendChild(entry);
        container.scrollTop = container.scrollHeight;
        while (container.children.length > 10) {
            container.removeChild(container.firstChild);
        }
    }

    startKeepAlive() {
        this.keepAliveInterval = setInterval(() => {
            if (this.isEnabled && !this.isListening && !this.isSpeaking && !this.micBlocked) {
                this.startListening();
            }
        }, 3000);

        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.isEnabled && !this.isListening) {
                setTimeout(() => {
                    if (this.isEnabled && !this.isListening) this.startListening();
                }, 500);
            }
        });

        window.addEventListener('focus', () => {
            if (this.isEnabled && !this.isListening) {
                setTimeout(() => {
                    if (this.isEnabled && !this.isListening) this.startListening();
                }, 500);
            }
        });
    }

    stopKeepAlive() {
        if (this.keepAliveInterval) {
            clearInterval(this.keepAliveInterval);
            this.keepAliveInterval = null;
        }
    }
}

const voiceControl = new VoiceControl();

document.addEventListener('DOMContentLoaded', () => {
    const voiceBtn = document.getElementById('voice-control-btn');
    if (voiceBtn) voiceBtn.addEventListener('click', () => voiceControl.toggle());

    const toggleBtn = document.getElementById('voice-toggle-btn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const enabled = voiceControl.toggle();
            toggleBtn.textContent = enabled ? 'Disable Voice' : 'Enable Voice';
            toggleBtn.style.background = enabled
                ? 'linear-gradient(135deg, #ef4444, #dc2626)'
                : 'linear-gradient(135deg, #10b981, #059669)';
        });
    }

    setTimeout(() => {
        voiceControl.isEnabled = true;
        voiceControl.startListening();
        if (voiceBtn) voiceBtn.classList.add('active', 'listening');
        if (toggleBtn) {
            toggleBtn.textContent = 'Disable Voice';
            toggleBtn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        }
        console.log('Emma ready. Say "Hey Emma".');
    }, 2000);
});