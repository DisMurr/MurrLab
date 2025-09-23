#!/usr/bin/env python3
"""
Test script to verify TTS fixes are working
"""

from murr import MurrTTS

def test_tts_functionality():
    print("🎭 Testing TTS Functionality")
    print("=" * 50)
    
    try:
        # Test model loading
        print("📦 Loading TTS model...")
        model = MurrTTS.from_pretrained(device="mps")
        print("✅ Model loaded successfully!")
        
        # Test basic generation without voice reference
        print("\n🎤 Testing text-to-speech generation...")
        text = "Hello! This is a test of the MurrLab TTS system."
        
        # Generate without audio prompt (uses built-in voice)
        wav = model.generate(text)
        print(f"✅ Generated audio tensor with shape: {wav.shape}")
        
        # Save the test audio
        import torch
        import torchaudio
        output_path = "test_generation.wav"
        torchaudio.save(output_path, wav, model.sr)
        print(f"✅ Audio saved to: {output_path}")
        
        print("\n🎉 All TTS functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_tts_functionality()
    if success:
        print("\n🚀 TTS system is working correctly!")
    else:
        print("\n⚠️  TTS system has issues")
