#!/usr/bin/env python3
"""
Advanced FastAPI Voice Service
Features: TTS, Voice Conversion, Real-time streaming, Multi-language support
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch
import torchaudio
import io
import os
import json
from pathlib import Path
from typing import Optional
try:
    import whisper  # optional, provided by the 'asr' extra
except Exception:  # pragma: no cover - optional dependency
    whisper = None  # type: ignore
import librosa
import numpy as np
from pydantic import BaseModel
from chatterbox import MurrTTS, MurrVC

# Pydantic models for API
class TTSRequest(BaseModel):
    text: str
    exaggeration: float = 0.5
    cfg_weight: float = 0.5
    voice_profile: Optional[str] = None
    language: str = "en"

class VoiceProfile(BaseModel):
    name: str
    exaggeration: float
    cfg_weight: float
    description: str = ""

# Initialize FastAPI app
app = FastAPI(
    title="🎭 Enhanced AI Voice API",
    description="Advanced TTS, Voice Conversion, and Audio Processing API",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global models and configurations
class VoiceService:
    def __init__(self):
        self.device = self.get_device()
        self.tts_model = None
        self.vc_model = None
        self.whisper_model = None
        self.voice_profiles = self.load_voice_profiles()
        self.temp_dir = Path("./temp_audio")
        self.temp_dir.mkdir(exist_ok=True)
        self.models_loaded = False
        
    def get_device(self):
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def load_models(self):
        """Load all AI models"""
        try:
            if not self.tts_model:
                self.tts_model = MurrTTS.from_pretrained(device=self.device)
            if not self.vc_model:
                self.vc_model = MurrVC.from_pretrained(device=self.device)
            if whisper is not None and not self.whisper_model:
                self.whisper_model = whisper.load_model("base")
            self.models_loaded = True
        except Exception as e:
            print(f"Error loading models: {e}")
            self.models_loaded = False
    
    def load_voice_profiles(self):
        """Load voice profiles from file"""
        profiles_file = Path("voice_profiles.json")
        if profiles_file.exists():
            with open(profiles_file, 'r') as f:
                return json.load(f)
        return {
            "default": {"exaggeration": 0.5, "cfg_weight": 0.5, "description": "Default voice"},
            "excited": {"exaggeration": 1.2, "cfg_weight": 0.3, "description": "High energy voice"},
            "calm": {"exaggeration": 0.3, "cfg_weight": 0.6, "description": "Calm and soothing"},
            "professional": {"exaggeration": 0.4, "cfg_weight": 0.5, "description": "Professional tone"},
        }
    
    def save_voice_profiles(self):
        """Save voice profiles to file"""
        with open("voice_profiles.json", 'w') as f:
            json.dump(self.voice_profiles, f, indent=2)

# Initialize service
voice_service = VoiceService()

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    print("🚀 Loading AI models...")
    voice_service.load_models()
    print("✅ Models loaded successfully!")

@app.get("/")
async def root():
    return {
        "message": "🎭 Enhanced AI Voice API",
        "version": "2.0.0",
        "device": voice_service.device,
        "endpoints": {
            "tts": "/tts/",
            "voice_conversion": "/voice-conversion/",
            "transcribe": "/transcribe/",
            "voice_profiles": "/voice-profiles/",
            "health": "/health/"
        }
    }

@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if voice_service.models_loaded else "models_not_loaded",
        "device": voice_service.device,
        "models_loaded": {
            "tts": voice_service.tts_model is not None,
            "vc": voice_service.vc_model is not None,
            "whisper": voice_service.whisper_model is not None
        },
        "all_models_ready": voice_service.models_loaded
    }

@app.post("/tts/")
async def text_to_speech(request: TTSRequest):
    try:
        if not voice_service.tts_model:
            raise HTTPException(status_code=503, detail="TTS model not loaded")
        exag = request.exaggeration
        cfg = request.cfg_weight
        if request.voice_profile and request.voice_profile in voice_service.voice_profiles:
            profile = voice_service.voice_profiles[request.voice_profile]
            exag = profile["exaggeration"]
            cfg = profile["cfg_weight"]
        wav = voice_service.tts_model.generate(request.text, exaggeration=exag, cfg_weight=cfg)
        temp_file = voice_service.temp_dir / f"tts_{hash(request.text)}.wav"
        torchaudio.save(str(temp_file), wav, voice_service.tts_model.sr)
        return FileResponse(str(temp_file), media_type="audio/wav", filename="generated_speech.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts/stream/")
async def text_to_speech_stream(request: TTSRequest):
    try:
        if not voice_service.tts_model or not voice_service.models_loaded:
            raise HTTPException(status_code=503, detail="TTS model not loaded")
        def generate_audio():
            if not voice_service.tts_model:
                raise ValueError("TTS model not available")
            wav = voice_service.tts_model.generate(request.text, exaggeration=request.exaggeration, cfg_weight=request.cfg_weight)
            buffer = io.BytesIO()
            sample_rate = getattr(voice_service.tts_model, 'sr', 22050)
            torchaudio.save(buffer, wav, int(sample_rate), format="wav")
            buffer.seek(0)
            while True:
                chunk = buffer.read(8192)
                if not chunk:
                    break
                yield chunk
        return StreamingResponse(generate_audio(), media_type="audio/wav", headers={"Content-Disposition": "attachment; filename=stream.wav"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice-conversion/")
async def voice_conversion(source_audio: UploadFile = File(...), target_audio: UploadFile = File(...)):
    try:
        if not voice_service.vc_model:
            raise HTTPException(status_code=503, detail="Voice conversion model not loaded")
        source_path = voice_service.temp_dir / f"source_{source_audio.filename}"
        target_path = voice_service.temp_dir / f"target_{target_audio.filename}"
        with open(source_path, "wb") as f:
            f.write(await source_audio.read())
        with open(target_path, "wb") as f:
            f.write(await target_audio.read())
        wav = voice_service.vc_model.generate(audio=str(source_path), target_voice_path=str(target_path))
        result_path = voice_service.temp_dir / "voice_conversion_result.wav"
        torchaudio.save(str(result_path), wav, voice_service.vc_model.sr)
        return FileResponse(str(result_path), media_type="audio/wav", filename="voice_converted.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe/")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        if not voice_service.whisper_model:
            raise HTTPException(status_code=503, detail="Whisper model not loaded")
        audio_path = voice_service.temp_dir / f"transcribe_{audio_file.filename}"
        with open(audio_path, "wb") as f:
            f.write(await audio_file.read())
        result = voice_service.whisper_model.transcribe(str(audio_path))
        return {"text": result["text"], "language": result["language"], "segments": result.get("segments", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("apps.api.advanced_voice_api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
