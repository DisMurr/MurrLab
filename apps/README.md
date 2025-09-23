# Apps

This folder contains runnable applications:

- streamlit/enhanced_voice_platform.py — Streamlit UI for TTS/VC
- api/advanced_voice_api.py — FastAPI server exposing TTS/VC/ASR endpoints

Run examples:

- Streamlit: streamlit run apps/streamlit/enhanced_voice_platform.py
- API: uvicorn apps.api.advanced_voice_api:app --reload

Top-level shims remain for backward compatibility.