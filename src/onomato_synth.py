# -*- coding: utf-8 -*-
"""
onomato_synth.py: Lightweight Procedural Audio Synthesis Engine for OnomaDict.

Pure Python / NumPy / SciPy implementation of the Dual-Engine Hybrid Synthesizer:
  - Human Vocal Tract Model: Glottal pulse excitation + 2-pole resonant formant filters (F1, F2).
  - Physical Impact Model: Sub-Kick transient impulse (40-80Hz) + Modal Resonators (Wood/Metal/Glass) + Noise generator.
  - Cross-Modal Morphing: Seamlessly blends voice and physical sound via the 'vocalness' parameter (0.0 to 1.0).

Zero external WAV dependencies. Generates procedural onomatopoeia audio in real time.
"""

import math
import sys
from typing import Dict, Any, Tuple, Optional
import numpy as np
from scipy import signal
import scipy.io.wavfile as wavfile

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class OnomatoSynthesizer:
    """Procedural Onomatopoeia Synthesizer combining vocal tract formants and physical impact resonators."""

    # Standard vowel formants (F1, F2 in Hz)
    VOWEL_FORMANTS = {
        "a": (800, 1200),
        "i": (300, 2300),
        "u": (350, 1200),
        "e": (500, 1900),
        "o": (500, 900),
    }

    # Modal resonance profiles for material simulation (frequency multipliers & decay ratios)
    MODAL_PROFILES = {
        "wood": {"freqs": [1.0, 1.45, 2.1, 3.2], "decays": [1.0, 0.7, 0.4, 0.2]},
        "metal": {"freqs": [1.0, 2.76, 5.4, 8.9], "decays": [1.0, 0.9, 0.8, 0.6]},
        "glass": {"freqs": [1.0, 2.32, 4.15, 6.8], "decays": [1.0, 0.8, 0.5, 0.3]},
        "membrane": {"freqs": [1.0, 1.59, 2.14, 2.3], "decays": [1.0, 0.8, 0.6, 0.4]},
    }

    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate

    def classify_pattern(self, word: str) -> Dict[str, Any]:
        """Classifies onomatopoeia into physical/vocal synthesis routing patterns."""
        w = word.lower()
        # Pattern A: Heavy Physical Impact / Explosion (Sub-Kick ON, Vocal Tract BYPASS)
        if any(k in w for k in ["ドカン", "ドスン", "ズシン", "ボコッ", "バタン", "どかん", "ずしん", "쿵", "쾅", "boom", "bang"]):
            return {"pattern": "heavy_impact", "sub_kick": True, "material": "membrane", "base_freq": 65.0, "decay": 0.45, "bypass": True}

        # Pattern B: Crisp High-Frequency Physical Impact (Sub-Kick OFF, HPF, BYPASS)
        if any(k in w for k in ["カツン", "パリン", "カンカン", "チャリン", "キン", "かつん", "ぱりん", "탁", "챙", "clink", "snap"]):
            mat = "glass" if any(k in w for k in ["パリン", "ぱりん", "ガラス"]) else "metal"
            return {"pattern": "crisp_impact", "sub_kick": False, "material": mat, "base_freq": 1200.0, "decay": 0.25, "bypass": True}

        # Pattern C: Friction / Fluid / Ambient Texture (Noise + Filter)
        if any(k in w for k in ["サラサラ", "ザーザー", "シュー", "シトシト", "さらさら", "ざーざー", "스르르", "솨"]):
            return {"pattern": "texture_fluid", "sub_kick": False, "material": "wood", "base_freq": 400.0, "decay": 0.8, "bypass": False}

        # Pattern D: Human Vocalization / Emotional State
        return {"pattern": "vocal_state", "sub_kick": False, "material": "wood", "base_freq": 160.0, "decay": 0.5, "bypass": False}

    def generate_vocal_component(self, f0: float, vowel: str, duration: float) -> np.ndarray:
        """Synthesizes human vocal tract component using glottal pulse and 2-pole formant filters."""
        n_samples = int(self.sr * duration)
        t = np.linspace(0, duration, n_samples, endpoint=False)

        # Glottal pulse excitation (sawtooth-like pulse)
        phase = (t * f0) % 1.0
        excitation = np.where(phase < 0.2, phase / 0.2, (1.0 - phase) / 0.8 * -0.5)

        # Formant resonance filtering
        f1, f2 = self.VOWEL_FORMANTS.get(vowel, (600, 1400))
        audio = np.zeros_like(excitation)

        for freq, bw in [(f1, 80), (f2, 120)]:
            r = math.exp(-math.pi * bw / self.sr)
            theta = 2.0 * math.pi * freq / self.sr
            b = [1.0 - r]
            a = [1.0, -2.0 * r * math.cos(theta), r * r]
            audio += signal.lfilter(b, a, excitation)

        # Envelope
        env = np.exp(-t * 2.5)
        return audio * env

    def generate_physical_component(self, pattern_info: Dict[str, Any], duration: float) -> np.ndarray:
        """Synthesizes physical impact / resonance component."""
        n_samples = int(self.sr * duration)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        audio = np.zeros(n_samples, dtype=np.float32)

        # 1. Sub-Kick (Heavy physical shockwave transient: 40-80Hz pitch drop)
        if pattern_info["sub_kick"]:
            kick_f = np.exp(-t * 30.0) * 80.0 + 45.0
            phase = 2.0 * np.pi * np.cumsum(kick_f) / self.sr
            kick_env = np.exp(-t * 12.0)
            sub_kick = np.sin(phase) * kick_env
            # Soft saturation
            sub_kick = np.tanh(sub_kick * 2.0)
            audio += sub_kick * 0.9

        # 2. Shockwave transient spike (1.5ms)
        spike_len = int(self.sr * 0.002)
        if spike_len < n_samples:
            audio[:spike_len] += (np.random.rand(spike_len) * 2.0 - 1.0) * 0.8

        # 3. Modal Resonator Banks
        mat = pattern_info.get("material", "wood")
        profile = self.MODAL_PROFILES.get(mat, self.MODAL_PROFILES["wood"])
        base_f = pattern_info.get("base_freq", 200.0)
        decay_scale = pattern_info.get("decay", 0.4)

        for f_mult, d_ratio in zip(profile["freqs"], profile["decays"]):
            f_mode = min(base_f * f_mult, self.sr * 0.45)
            d_mode = max(1.0, 1.0 / (decay_scale * d_ratio))
            mode_sig = np.sin(2.0 * np.pi * f_mode * t) * np.exp(-t * d_mode * 8.0)
            audio += mode_sig * 0.35

        return audio

    def synthesize(self, word: str, duration: float = 0.5, vocalness: float = 0.4) -> np.ndarray:
        """
        Synthesizes procedural audio for the given onomatopoeia word.
        
        Args:
            word: The onomatopoeia string (e.g. 'ドカン', 'カツン', 'サラサラ', 'オギャー')
            duration: Total duration in seconds (default 0.5s)
            vocalness: Cross-modal blend ratio: 0.0 (Pure Physical) to 1.0 (Pure Voice)
        
        Returns:
            Normalized float32 numpy array [-1.0, 1.0] of audio samples.
        """
        pattern = self.classify_pattern(word)

        # Detect primary vowel
        primary_vowel = "a"
        for char in word:
            if char in "あかさたなはまやらわカサタナハマヤラワ":
                primary_vowel = "a"
                break
            elif char in "いきしちにひみりイキシチニヒミリ":
                primary_vowel = "i"
                break
            elif char in "うくすつぬふむゆるウクスツヌフムユル":
                primary_vowel = "u"
                break
            elif char in "えけせてねへめれエケセテネヘメレ":
                primary_vowel = "e"
                break
            elif char in "おこそとのほもよろオコソトノホモヨロ":
                primary_vowel = "o"
                break

        # Generate Engine A (Voice) & Engine B (Physical)
        voice_audio = self.generate_vocal_component(f0=180.0, vowel=primary_vowel, duration=duration)
        physical_audio = self.generate_physical_component(pattern_info=pattern, duration=duration)

        # Vocal Tract Bypass: If pattern requires bypass, physical impact stays uncolored
        if pattern["bypass"]:
            eff_vocalness = vocalness * 0.25
        else:
            eff_vocalness = vocalness

        # Cross-modal Morphing
        blended = (1.0 - eff_vocalness) * physical_audio + eff_vocalness * voice_audio

        # Peak normalization
        peak = np.max(np.abs(blended))
        if peak > 1e-4:
            blended = blended / peak * 0.95

        return blended.astype(np.float32)

    def save_wav(self, file_path: str, audio: np.ndarray):
        """Saves float32 audio as 16-bit PCM WAV."""
        clamped = np.clip(audio, -1.0, 1.0)
        int16_data = (clamped * 32767.0).astype(np.int16)
        wavfile.write(file_path, self.sr, int16_data)


# Convenience function for quick 1-line synthesis
def synthesize_onomatopoeia(word: str, duration: float = 0.5, vocalness: float = 0.4) -> np.ndarray:
    """Quick procedural synthesis function."""
    synth = OnomatoSynthesizer()
    return synth.synthesize(word, duration=duration, vocalness=vocalness)


if __name__ == "__main__":
    import os
    print("Testing OnomatoSynthesizer...")
    synth = OnomatoSynthesizer()
    test_words = ["ドカン", "カツン", "サラサラ", "オギャー"]
    for w in test_words:
        audio = synth.synthesize(w)
        peak = np.max(np.abs(audio))
        print(f"  [OK] Synthesized '{w}': {len(audio)} samples, Peak: {peak:.2f}")
    print("All tests passed successfully!")
