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
streamlit run run_ui_streamlit.py
```

## Run the API
```bash
uvicorn apps.api.advanced_voice_api:app --reload
# or: python run_api_server.py
# Docs: http://localhost:8000/docs
```

## Tools
- Dev quickstart menu: `python dev_quickstart.py`
- Launch both UI and API: `python run_all_services.py`
- Download sample datasets: `python datasets_download_and_split.py`

## Project layout
```
src/murr/                 # Core library
apps/api/advanced_voice_api.py
apps/streamlit/enhanced_voice_platform.py
examples/example_tts.py   # Single example
run_ui_streamlit.py       # Streamlit shim
run_api_server.py         # FastAPI shim
dev_quickstart.py         # Dev helper menu
run_all_services.py       # Starts UI + API
datasets_download_and_split.py  # Optional dataset tool
audio/                    # Sample outputs
```

## Changelog
See CHANGELOG.md for release notes.
