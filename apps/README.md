# Apps

This folder contains runnable applications:

- streamlit/enhanced_voice_platform.py — Streamlit UI for TTS/VC
- api/advanced_voice_api.py — FastAPI server exposing TTS/VC/ASR endpoints
- gradio/tts_app.py — Gradio TTS demo
- gradio/vc_app.py — Gradio voice conversion demo

Run examples:

- Streamlit: streamlit run apps/streamlit/enhanced_voice_platform.py
- API: uvicorn apps.api.advanced_voice_api:app --reload
- Gradio TTS: python -m apps.gradio.tts_app
- Gradio VC: python -m apps.gradio.vc_app

Top-level shims remain for backward compatibility.