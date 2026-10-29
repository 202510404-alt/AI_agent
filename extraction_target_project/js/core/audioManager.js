// Small synthesized soundtrack: no external audio assets or downloads required.
export class AudioManager {
    constructor() {
        this.context = null;
        this.enabled = localStorage.getItem('gameAudioMuted') !== 'true';
        this.playing = false;
        this.beat = 0;
        this.timer = null;
        this.lastShot = 0;
    }

    unlock() {
        const Context = window.AudioContext || window.webkitAudioContext;
        if (!Context) return;
        if (!this.context) this.context = new Context();
        if (this.context.state === 'suspended') {
            this.context.resume().then(() => {
                if (this.playing) this.startBeat();
            }).catch(() => {});
        } else if (this.playing) this.startBeat();
    }

    setEnabled(enabled) {
        this.enabled = enabled;
        localStorage.setItem('gameAudioMuted', String(!enabled));
        if (enabled) this.unlock();
        if (!enabled) this.stopBeat();
        else if (this.playing) this.startBeat();
    }

    setPlaying(playing) {
        this.playing = playing;
        this.stopBeat();
        if (playing && this.enabled) this.startBeat();
    }

    stopBeat() {
        if (this.timer) clearInterval(this.timer);
        this.timer = null;
    }

    startBeat() {
        if (this.timer || !this.context || this.context.state !== 'running') return;
        this.timer = setInterval(() => {
            if (!this.enabled || !this.playing) return;
            const notes = [110, 0, 164.81, 0, 130.81, 0, 196, 0];
            const note = notes[this.beat % notes.length];
            if (note) this.tone(note, 0.22, 'triangle', 0.035);
            if (this.beat % 4 === 0) this.tone(55, 0.12, 'sine', 0.055);
            this.beat++;
        }, 240);
    }

    tone(frequency, duration, wave = 'sine', volume = 0.08, slide = 0) {
        if (!this.enabled || !this.context || this.context.state !== 'running') return;
        const now = this.context.currentTime;
        const oscillator = this.context.createOscillator();
        const gain = this.context.createGain();
        oscillator.type = wave;
        oscillator.frequency.setValueAtTime(frequency, now);
        if (slide) oscillator.frequency.exponentialRampToValueAtTime(Math.max(1, frequency + slide), now + duration);
        gain.gain.setValueAtTime(Math.max(0.0001, volume), now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
        oscillator.connect(gain);
        gain.connect(this.context.destination);
        oscillator.start(now);
        oscillator.stop(now + duration);
    }

    play(effect) {
        if (effect === 'shoot') {
            if (performance.now() - this.lastShot < 140) return;
            this.lastShot = performance.now();
            this.tone(420, 0.07, 'square', 0.014, -180);
        } else if (effect === 'skill') {
            this.tone(440, 0.32, 'sawtooth', 0.07, 440);
            this.tone(660, 0.24, 'sine', 0.055, 330);
        } else if (effect === 'hit') {
            this.tone(190, 0.18, 'sawtooth', 0.06, -140);
        }
    }
}
