# 🎭 MurrLab - AI Voice Platform

An open-source local TTS and Voice Conversion stack. No API keys required.

## Features
- Text-to-Speech (MurrTTS) with emotion control
- Voice Conversion (MurrVC)
- Streamlit UI and FastAPI server
- Apple Silicon (MPS), CUDA, or CPU

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -e .[web,api]
# Optional ASR: pip install .[asr]
```

## Quick start
```python
from murr import MurrTTS
import torchaudio

model = MurrTTS.from_pretrained(device="mps")
wav = model.generate("Hello from MurrLab!")
torchaudio.save("audio/output.wav", wav, model.sr)
```

## Run the UI
```bash
streamlit run enhanced_voice_platform.py
```

## Run the API
```bash
uvicorn apps.api.advanced_voice_api:app --reload
# Docs: http://localhost:8000/docs
```

## Project layout
```
src/murr/                 # Core library
apps/api/advanced_voice_api.py
apps/streamlit/enhanced_voice_platform.py
examples/example_tts.py   # Single example
audio/                    # Sample outputs
```

## Changelog
See CHANGELOG.md for release notes.
