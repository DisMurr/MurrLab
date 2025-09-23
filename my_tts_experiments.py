#!/usr/bin/env python3
"""
Custom TTS Experiments with Chatterbox
"""

import torchaudio as ta
import torch
from chatterbox.tts import ChatterboxTTS

def setup_model():
    """Initialize the TTS model"""
    device = 'mps' if torch.backends.mps.is_available() else 'cpu'
    print(f"Using device: {device}")
    return ChatterboxTTS.from_pretrained(device=device)

def generate_podcast_intro(model):
    """Generate a podcast-style introduction"""
    text = """
    Welcome back to TechTalk, the podcast where we explore the cutting edge of artificial intelligence.
    I'm your host, and today we're diving deep into the fascinating world of text-to-speech technology.
    """
    wav = model.generate(text, exaggeration=0.6, cfg_weight=0.4)
    ta.save("podcast_intro.wav", wav, model.sr)
    print("✅ Generated podcast_intro.wav")

def generate_character_voices(model):
    """Generate different character voices for storytelling"""
    characters = [
        ("Hello there! I'm the friendly narrator of this tale.", 0.5, 0.5, "narrator"),
        ("Grr! I am the mighty dragon who guards the treasure!", 1.2, 0.3, "dragon"),
        ("Oh my! What a wonderful adventure this shall be!", 0.8, 0.4, "princess"),
        ("Indeed, m'lady. We must proceed with great caution.", 0.4, 0.6, "knight")
    ]
    
    for text, exag, cfg, character in characters:
        wav = model.generate(text, exaggeration=exag, cfg_weight=cfg)
        ta.save(f"character_{character}.wav", wav, model.sr)
        print(f"✅ Generated character_{character}.wav")

def generate_educational_content(model):
    """Generate educational narration"""
    text = """
    The process of photosynthesis is fascinating. Plants capture sunlight and convert carbon dioxide 
    and water into glucose and oxygen. This remarkable process sustains life on our planet.
    """
    wav = model.generate(text, exaggeration=0.4, cfg_weight=0.5)
    ta.save("educational_narration.wav", wav, model.sr)
    print("✅ Generated educational_narration.wav")

if __name__ == "__main__":
    print("🎭 Starting Custom TTS Experiments...")
    
    # Initialize model
    model = setup_model()
    
    # Generate different types of content
    generate_podcast_intro(model)
    generate_character_voices(model)
    generate_educational_content(model)
    
    print("🎉 All experiments complete!")
    print("📁 Check the generated .wav files in this directory")
