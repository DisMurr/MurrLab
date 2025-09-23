#!/usr/bin/env python3
"""
Backward-compatible shim. The Streamlit app was moved to apps/streamlit/enhanced_voice_platform.py
Run: streamlit run apps/streamlit/enhanced_voice_platform.py
"""

from apps.streamlit.enhanced_voice_platform import main

if __name__ == "__main__":
    main()

import os
import torch
import torchaudio
import librosa
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import whisper
import noisereduce as nr
from pydub import AudioSegment
import matplotlib.pyplot as plt
import librosa.display  # needed for specshow
import seaborn as sns
from datasets import load_dataset
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import time
from chatterbox.tts import ChatterboxTTS
from chatterbox.vc import ChatterboxVC

class EnhancedVoicePlatform:
    def __init__(self):
        self.device = self.get_device()
        self.tts_model = None
        self.vc_model = None
        self.whisper_model = None
        self.datasets = {}
        self.voice_profiles = {}
        
    def get_device(self):
        """Auto-detect best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def initialize_models(self):
        """Initialize all AI models"""
        st.write("🔄 Loading AI models...")
        
        # TTS Model
        if not self.tts_model:
            self.tts_model = ChatterboxTTS.from_pretrained(device=self.device)
            st.success("✅ TTS Model loaded")
        
        # Voice Conversion Model
        if not self.vc_model:
            self.vc_model = ChatterboxVC.from_pretrained(device=self.device)
            st.success("✅ Voice Conversion Model loaded")
        
        # Whisper ASR Model
        if not self.whisper_model:
            self.whisper_model = whisper.load_model("base")
            st.success("✅ Whisper ASR Model loaded")
    
    def download_datasets(self):
        """Download and prepare popular voice datasets"""
        st.write("📁 Loading voice datasets...")
        
        try:
            # Common Voice Dataset
            common_voice = load_dataset("mozilla-foundation/common_voice_11_0", "en", split="train[:100]")
            self.datasets['common_voice'] = common_voice
            st.success("✅ Mozilla Common Voice dataset loaded")
            
            # LibriSpeech samples
            librispeech = load_dataset("librispeech_asr", "clean", split="train.100[:50]")
            self.datasets['librispeech'] = librispeech
            st.success("✅ LibriSpeech dataset loaded")
            
        except Exception as e:
            st.warning(f"Dataset loading error: {e}")
    
    def enhance_audio(self, audio_path):
        """AI-powered audio enhancement"""
        # Load audio
        audio, sr = librosa.load(audio_path, sr=22050)
        
        # Noise reduction
        reduced_noise = nr.reduce_noise(y=audio, sr=sr)
        
        # Normalize audio
        normalized = librosa.util.normalize(reduced_noise)
        
        # Save enhanced audio
        enhanced_path = audio_path.replace('.wav', '_enhanced.wav')
        torchaudio.save(enhanced_path, torch.tensor(normalized).unsqueeze(0), int(sr))
        
        return enhanced_path
    
    def analyze_voice(self, audio_path):
        """Comprehensive voice analysis"""
        audio, sr = librosa.load(audio_path)
        
        # Extract features
        features = {
            'duration': len(audio) / sr,
            'sample_rate': sr,
            'pitch_mean': np.mean(librosa.yin(audio, fmin=50, fmax=300)),
            'energy': np.mean(librosa.feature.rms(y=audio)),
            'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr)),
            'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(audio)),
        }
        
        return features
    
    def real_time_tts(self, text, voice_profile="default"):
        """Real-time text-to-speech with voice profiles"""
        if not self.tts_model:
            raise ValueError("TTS model not loaded. Please initialize models first.")
            
        if voice_profile in self.voice_profiles:
            exag, cfg = self.voice_profiles[voice_profile]
        else:
            exag, cfg = 0.5, 0.5
        
        wav = self.tts_model.generate(text, exaggeration=exag, cfg_weight=cfg)
        return wav
    
    def create_voice_profile(self, name, exaggeration, cfg_weight, description=""):
        """Create custom voice profiles"""
        self.voice_profiles[name] = (exaggeration, cfg_weight)
        return f"Voice profile '{name}' created successfully!"
    
    def batch_process_dataset(self, dataset_name, processing_type="tts"):
        """Batch process dataset samples"""
        if dataset_name not in self.datasets:
            return "Dataset not found"
        
        if not self.tts_model:
            return "TTS model not loaded"
        
        dataset = self.datasets[dataset_name]
        results = []
        
        for i, sample in enumerate(dataset):
            if i >= 10:  # Limit for demo
                break
                
            if processing_type == "tts":
                text = sample.get('sentence', sample.get('text', ''))
                if text:
                    wav = self.tts_model.generate(text)
                    output_path = f"dataset_output_{i}.wav"
                    torchaudio.save(output_path, wav, self.tts_model.sr)
                    results.append(output_path)
        
        return results

def main():
    st.set_page_config(
        page_title="🎭 Enhanced AI Voice Platform",
        page_icon="🎤",
        layout="wide"
    )
    
    st.title("🎭 Enhanced AI Voice Platform")
    st.markdown("**Powered by Open Source AI**")
    
    # Initialize platform
    if 'platform' not in st.session_state:
        st.session_state.platform = EnhancedVoicePlatform()
    
    platform = st.session_state.platform
    
    # Sidebar navigation
    st.sidebar.title("🎯 Features")
    tab = st.sidebar.selectbox("Choose Feature", [
        "🏠 Dashboard",
        "🎤 Advanced TTS",
        "🔄 Voice Conversion",
        "📊 Voice Analysis", 
        "🎭 Voice Profiles",
        "📁 Dataset Explorer",
        "🎙️ Real-time Recording",
        "🔧 Audio Enhancement",
        "📈 Batch Processing"
    ])
    
    # Initialize models button
    if st.sidebar.button("🚀 Initialize AI Models"):
        platform.initialize_models()
        platform.download_datasets()
    
    # Main content based on selected tab
    if tab == "🏠 Dashboard":
        st.header("🏠 AI Voice Platform Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Device", platform.device.upper())
            st.metric("TTS Model", "✅ Loaded" if platform.tts_model else "❌ Not Loaded")
        
        with col2:
            st.metric("Voice Profiles", len(platform.voice_profiles))
            st.metric("Datasets", len(platform.datasets))
        
        with col3:
            st.metric("VC Model", "✅ Loaded" if platform.vc_model else "❌ Not Loaded")
            st.metric("ASR Model", "✅ Loaded" if platform.whisper_model else "❌ Not Loaded")
        
        # Quick TTS demo
        st.subheader("🎤 Quick TTS Demo")
        demo_text = st.text_input("Enter text for quick synthesis:", "Hello! This is the enhanced AI voice platform!")
        
        if st.button("🎵 Generate Speech") and platform.tts_model:
            wav = platform.real_time_tts(demo_text)
            st.audio(wav.cpu().numpy(), sample_rate=platform.tts_model.sr)
    
    elif tab == "🎤 Advanced TTS":
        st.header("🎤 Advanced Text-to-Speech")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            text_input = st.text_area("Enter text to synthesize:", height=100)
            
            # Advanced controls
            st.subheader("🎛️ Voice Controls")
            exaggeration = st.slider("Emotion/Exaggeration", 0.0, 2.0, 0.5, 0.1)
            cfg_weight = st.slider("Stability/CFG Weight", 0.0, 1.0, 0.5, 0.1)
            
            # Voice style presets
            style = st.selectbox("Voice Style Preset", [
                "Custom", "Neutral", "Excited", "Calm", "Professional", 
                "Storyteller", "News Anchor", "Meditation"
            ])
            
            if style != "Custom":
                style_params = {
                    "Neutral": (0.5, 0.5),
                    "Excited": (1.2, 0.3),
                    "Calm": (0.3, 0.6),
                    "Professional": (0.4, 0.5),
                    "Storyteller": (0.7, 0.4),
                    "News Anchor": (0.6, 0.5),
                    "Meditation": (0.2, 0.7)
                }
                exaggeration, cfg_weight = style_params[style]
        
        with col2:
            st.subheader("🎯 Quick Actions")
            
            if st.button("🎵 Generate Speech", type="primary") and platform.tts_model:
                with st.spinner("Generating speech..."):
                    wav = platform.tts_model.generate(text_input, exaggeration=exaggeration, cfg_weight=cfg_weight)
                    
                    # Save and display
                    output_path = "advanced_tts_output.wav"
                    torchaudio.save(output_path, wav, platform.tts_model.sr)
                    
                    st.success("✅ Speech generated!")
                    st.audio(output_path)
                    
                    # Voice analysis
                    features = platform.analyze_voice(output_path)
                    st.json(features)
    
    elif tab == "📊 Voice Analysis":
        st.header("📊 Voice Analysis & Visualization")
        
        uploaded_file = st.file_uploader("Upload audio for analysis", type=['wav', 'mp3'])
        
        if uploaded_file:
            # Save uploaded file
            audio_path = f"uploaded_{uploaded_file.name}"
            with open(audio_path, "wb") as f:
                f.write(uploaded_file.read())
            
            st.audio(audio_path)
            
            # Analyze
            with st.spinner("Analyzing audio..."):
                features = platform.analyze_voice(audio_path)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📈 Audio Features")
                    for key, value in features.items():
                        st.metric(key.replace('_', ' ').title(), f"{value:.3f}")
                
                with col2:
                    st.subheader("🎵 Waveform Visualization")
                    audio, sr = librosa.load(audio_path)
                    
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
                    
                    # Waveform
                    ax1.plot(audio)
                    ax1.set_title("Waveform")
                    ax1.set_xlabel("Samples")
                    
                    # Spectrogram
                    D = librosa.stft(audio)
                    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
                    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', ax=ax2)
                    ax2.set_title("Spectrogram")
                    
                    st.pyplot(fig)
    
    elif tab == "🎭 Voice Profiles":
        st.header("🎭 Voice Profile Manager")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("➕ Create New Profile")
            
            profile_name = st.text_input("Profile Name")
            profile_exag = st.slider("Exaggeration", 0.0, 2.0, 0.5, key="profile_exag")
            profile_cfg = st.slider("CFG Weight", 0.0, 1.0, 0.5, key="profile_cfg")
            profile_desc = st.text_area("Description")
            
            if st.button("💾 Save Profile"):
                result = platform.create_voice_profile(profile_name, profile_exag, profile_cfg, profile_desc)
                st.success(result)
        
        with col2:
            st.subheader("📝 Existing Profiles")
            
            if platform.voice_profiles:
                for name, (exag, cfg) in platform.voice_profiles.items():
                    with st.expander(f"🎭 {name}"):
                        st.write(f"Exaggeration: {exag}")
                        st.write(f"CFG Weight: {cfg}")
                        
                        # Test profile
                        test_text = st.text_input(f"Test text for {name}:", f"Hello, this is the {name} voice profile!")
                        if st.button(f"🎵 Test {name}", key=f"test_{name}") and platform.tts_model:
                            wav = platform.real_time_tts(test_text, name)
                            st.audio(wav.cpu().numpy(), sample_rate=platform.tts_model.sr)
            else:
                st.info("No voice profiles created yet.")
    
    elif tab == "📁 Dataset Explorer":
        st.header("📁 Open Source Dataset Explorer")
        
        if platform.datasets:
            dataset_name = st.selectbox("Choose Dataset", list(platform.datasets.keys()))
            dataset = platform.datasets[dataset_name]
            
            st.write(f"**Dataset:** {dataset_name}")
            st.write(f"**Size:** {len(dataset)} samples")
            
            # Sample explorer
            sample_idx = st.slider("Sample Index", 0, min(len(dataset)-1, 99), 0)
            sample = dataset[sample_idx]
            
            st.subheader("📝 Sample Data")
            for key, value in sample.items():
                if key not in ['audio']:
                    st.write(f"**{key}:** {value}")
            
            # Play original audio if available
            if 'audio' in sample:
                st.subheader("🎵 Original Audio")
                audio_array = sample['audio']['array']
                sample_rate = sample['audio']['sampling_rate']
                st.audio(audio_array, sample_rate=sample_rate)
                
                # Generate TTS version
                if 'sentence' in sample or 'text' in sample:
                    text = sample.get('sentence', sample.get('text', ''))
                    if st.button("🎤 Generate TTS Version") and platform.tts_model:
                        wav = platform.tts_model.generate(text)
                        st.subheader("🎵 TTS Generated Version")
                        st.audio(wav.cpu().numpy(), sample_rate=platform.tts_model.sr)
        else:
            st.info("No datasets loaded. Click 'Initialize AI Models' in the sidebar.")
    
    elif tab == "🎙️ Real-time Recording":
        st.header("🎙️ Real-time Voice Recording & Processing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎤 Record Audio")
            
            duration = st.slider("Recording Duration (seconds)", 1, 10, 3)
            sample_rate = 44100
            
            if st.button("🔴 Start Recording"):
                with st.spinner(f"Recording for {duration} seconds..."):
                    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
                    sd.wait()
                    
                    # Save recording
                    recording_path = "real_time_recording.wav"
                    write(recording_path, sample_rate, recording)
                    
                    st.success("✅ Recording complete!")
                    st.audio(recording_path)
                    
                    # Auto-enhance
                    if st.checkbox("🔧 Auto-enhance audio"):
                        enhanced_path = platform.enhance_audio(recording_path)
                        st.subheader("🎵 Enhanced Audio")
                        st.audio(enhanced_path)
        
        with col2:
            st.subheader("🔄 Real-time Processing")
            
            # Speech-to-text with Whisper
            if st.button("📝 Transcribe with Whisper") and platform.whisper_model:
                if os.path.exists("real_time_recording.wav"):
                    result = platform.whisper_model.transcribe("real_time_recording.wav")
                    st.text_area("Transcription:", result["text"], height=100)
                    
                    # TTS from transcription
                    if st.button("🎵 Generate TTS from Transcription") and platform.tts_model:
                        wav = platform.tts_model.generate(result["text"])
                        st.audio(wav.cpu().numpy(), sample_rate=platform.tts_model.sr)
    
    # Footer
    st.markdown("---")
    st.markdown("🎭 **Enhanced AI Voice Platform** | Open Source AI")

if __name__ == "__main__":
    main()
