// Device Sound Effects System
class DeviceSounds {
    constructor() {
        this.audioContext = null;
        this.sounds = {};
        this.activeOscillators = {};
        this.init();
    }
    
    init() {
        // Create audio context
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.error('Web Audio API not supported');
        }
    }
    
    // Fan sound - low frequency hum
    playFanSound(deviceId, speed = 0.5) {
        if (!this.audioContext) return;
        
        // Stop existing sound
        this.stopSound(deviceId);
        
        // Create oscillator for fan hum
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(60 + (speed * 40), this.audioContext.currentTime);
        
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.03, this.audioContext.currentTime + 0.5);
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.start();
        
        this.activeOscillators[deviceId] = { oscillator, gainNode };
    }
    
    // AC sound - cooling hum
    playACSound(deviceId) {
        if (!this.audioContext) return;
        
        this.stopSound(deviceId);
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(80, this.audioContext.currentTime);
        
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.02, this.audioContext.currentTime + 1);
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.start();
        
        this.activeOscillators[deviceId] = { oscillator, gainNode };
    }
    
    // Fire alarm - loud siren
    async playFireAlarm(deviceId) {
        if (!this.audioContext) {
            console.error('Audio context not available');
            return;
        }
        
        // Resume audio context if suspended
        if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }
        
        this.stopSound(deviceId);
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.type = 'square';
        
        // Alternating siren sound
        const now = this.audioContext.currentTime;
        oscillator.frequency.setValueAtTime(800, now);
        oscillator.frequency.linearRampToValueAtTime(1200, now + 0.5);
        oscillator.frequency.linearRampToValueAtTime(800, now + 1);
        
        gainNode.gain.setValueAtTime(0.2, now); // Louder volume
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.start();
        
        console.log(`🚨 Fire alarm sound started for ${deviceId}`);
        
        // Loop the siren
        const interval = setInterval(() => {
            if (this.activeOscillators[deviceId]) {
                const t = this.audioContext.currentTime;
                oscillator.frequency.setValueAtTime(800, t);
                oscillator.frequency.linearRampToValueAtTime(1200, t + 0.5);
                oscillator.frequency.linearRampToValueAtTime(800, t + 1);
            } else {
                clearInterval(interval);
            }
        }, 1000);
        
        this.activeOscillators[deviceId] = { oscillator, gainNode, interval };
    }
    
    // Sound system - ambient music
    playSoundSystem(deviceId) {
        if (!this.audioContext) return;
        
        this.stopSound(deviceId);
        
        // Create multiple oscillators for chord
        const oscillators = [];
        const gainNode = this.audioContext.createGain();
        
        // C major chord (C, E, G)
        const frequencies = [261.63, 329.63, 392.00];
        
        frequencies.forEach(freq => {
            const osc = this.audioContext.createOscillator();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, this.audioContext.currentTime);
            osc.connect(gainNode);
            osc.start();
            oscillators.push(osc);
        });
        
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.02, this.audioContext.currentTime + 0.5);
        gainNode.connect(this.audioContext.destination);
        
        this.activeOscillators[deviceId] = { oscillators, gainNode };
    }
    
    // TV sound - white noise
    playTVSound(deviceId) {
        if (!this.audioContext) return;
        
        this.stopSound(deviceId);
        
        // Create white noise
        const bufferSize = 2 * this.audioContext.sampleRate;
        const noiseBuffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }
        
        const whiteNoise = this.audioContext.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;
        
        const gainNode = this.audioContext.createGain();
        gainNode.gain.setValueAtTime(0.005, this.audioContext.currentTime);
        
        whiteNoise.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        whiteNoise.start();
        
        this.activeOscillators[deviceId] = { source: whiteNoise, gainNode };
    }
    
    // Heater sound - gentle hum
    playHeaterSound(deviceId) {
        if (!this.audioContext) return;
        
        this.stopSound(deviceId);
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(50, this.audioContext.currentTime);
        
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.015, this.audioContext.currentTime + 2);
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.start();
        
        this.activeOscillators[deviceId] = { oscillator, gainNode };
    }
    
    // Door sound - beep
    playDoorSound(isOpen) {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(isOpen ? 800 : 600, this.audioContext.currentTime);
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.start();
        oscillator.stop(this.audioContext.currentTime + 0.2);
    }
    
    // Window sound - slide
    playWindowSound(isOpen) {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.type = 'sawtooth';
        
        if (isOpen) {
            oscillator.frequency.setValueAtTime(200, this.audioContext.currentTime);
            oscillator.frequency.linearRampToValueAtTime(400, this.audioContext.currentTime + 0.3);
        } else {
            oscillator.frequency.setValueAtTime(400, this.audioContext.currentTime);
            oscillator.frequency.linearRampToValueAtTime(200, this.audioContext.currentTime + 0.3);
        }
        
        gainNode.gain.setValueAtTime(0.05, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.start();
        oscillator.stop(this.audioContext.currentTime + 0.3);
    }
    
    // Stop sound
    stopSound(deviceId) {
        if (this.activeOscillators[deviceId]) {
            const sound = this.activeOscillators[deviceId];
            
            try {
                // Stop immediately for fire alarms
                if (deviceId.includes('fire')) {
                    if (sound.gainNode) {
                        sound.gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
                    }
                    
                    if (sound.oscillator) {
                        sound.oscillator.stop();
                    }
                    if (sound.oscillators) {
                        sound.oscillators.forEach(osc => osc.stop());
                    }
                    if (sound.source) {
                        sound.source.stop();
                    }
                    if (sound.interval) {
                        clearInterval(sound.interval);
                    }
                } else {
                    // Fade out for other devices
                    if (sound.gainNode) {
                        sound.gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 0.5);
                    }
                    
                    setTimeout(() => {
                        if (sound.oscillator) {
                            sound.oscillator.stop();
                        }
                        if (sound.oscillators) {
                            sound.oscillators.forEach(osc => osc.stop());
                        }
                        if (sound.source) {
                            sound.source.stop();
                        }
                        if (sound.interval) {
                            clearInterval(sound.interval);
                        }
                    }, 500);
                }
            } catch (e) {
                console.error('Error stopping sound:', e);
            }
            
            delete this.activeOscillators[deviceId];
        }
    }
    
    // Stop all sounds
    stopAllSounds() {
        Object.keys(this.activeOscillators).forEach(deviceId => {
            this.stopSound(deviceId);
        });
    }
}

// Global instance
const deviceSounds = new DeviceSounds();
