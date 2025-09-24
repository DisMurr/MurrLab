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
# Or: pip install -r requirements.txt (installs everything)
```

## TL;DR: Run
- UI: `streamlit run run_ui_streamlit.py` → http://localhost:8501
- API: `uvicorn apps.api.advanced_voice_api:app --reload` → http://localhost:8000/docs
- Both: `python run_all_services.py`

## Weights
- The models first look for local weights under `weights/` (or the directory pointed to by env var `MURR_WEIGHTS_DIR`).
- If not found, they try to download from Hugging Face repo `DisMurr/murr-voice`.
- If that repo is private, either:
  - Place `ve.safetensors`, `t3_cfg.safetensors`, `s3gen.safetensors`, `tokenizer.json`, `conds.pt` in a local `weights/` folder, or
  - Authenticate with Hugging Face (`huggingface-cli login`) and ensure access to the repo.

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

## Cloudflare Pages (static landing)
This repo now includes a static landing page in `public/` so Cloudflare Pages won’t be blank.
- Framework preset: None
- Build command: (leave empty)
- Build output directory: public
- Root directory: /

Pages only serves static files; the Streamlit/UI and FastAPI/API must run on compute (VM/PaaS) or be exposed via Cloudflare Tunnel. See Weights and Run sections above.

## Changelog
See CHANGELOG.md for release notes.
