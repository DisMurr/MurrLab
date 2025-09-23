# Copilot Instructions for MurrLab

Use this guide to be productive quickly in this repo. Keep edits minimal, follow the existing patterns, and prefer aliases exposed in `src/chatterbox/__init__.py`.

## Architecture overview
- Package layout
  - `src/chatterbox/`: Core engines and public surface.
    - `tts.py` → ChatterboxTTS (aliased publicly as `MurrTTS`). Entry for text → tokens → audio; handles tokenizer, T3 (text-to-token), and S3Gen (token-to-audio) orchestration.
    - `vc.py` → ChatterboxVC (aliased publicly as `MurrVC`). Voice conversion pipeline.
    - `models/`: Model stack used by TTS/VC.
      - `t3/` → Text-to-token model (LLaMA backbone). Key file: `t3/t3.py` (custom inference loop; CFG supported).
      - `s3gen/` → Token-to-audio spectral models (decoder, vocoder, flow, etc.).
      - `voice_encoder/`, `tokenizers/`, `s3tokenizer/` → embeddings and tokenization.
- Apps
  - `apps/api/advanced_voice_api.py` → FastAPI app offering `/tts`, `/tts/stream`, `/voice-conversion`, optional `/transcribe` if Whisper installed.
  - `apps/streamlit/enhanced_voice_platform.py` → Streamlit UI (top-level `enhanced_voice_platform.py` is a shim).
- Examples
  - `examples/example_tts.py`, `examples/example_vc.py` → Minimal usage; import aliases `MurrTTS`, `MurrVC`.

Why this structure: we keep the on-disk module path `chatterbox` for compatibility, but all user-facing docs import `MurrTTS/MurrVC` aliases. Apps live under `apps/` with thin shims at repo root.

## Public API and patterns
- Import the high-level models via aliases:
  - `from chatterbox import MurrTTS, MurrVC`
  - Construct with `.from_pretrained(device=...)` (device: `"cuda"|"mps"|"cpu"`).
  - TTS: `wav = model.generate(text, exaggeration=..., cfg_weight=..., audio_prompt_path=...)`; save with `torchaudio.save(path, wav, model.sr)`.
  - VC: `wav = model.generate(audio=..., target_voice_path=...)`.
- Do not import deep internals from `models/` unless extending research code. Use the surface types above from apps and examples.
- CFG and sampling are handled internally (see `t3/t3.py`). If touching inference, keep batch duplication rules for CFG and positional embedding guards consistent with the current code.

## Developer workflows
- Install (editable):
  - `pip install -e .` (extras available: `web`, `api`, `asr`, `datasets`, `dev` in `pyproject.toml`).
- Run Streamlit UI:
  - `streamlit run enhanced_voice_platform.py` (shim → `apps/streamlit/...`).
- Run API:
  - `python advanced_voice_api.py` (shim → `apps/api/...`), or `uvicorn apps.api.advanced_voice_api:app --reload`.
- Quick menu / tests:
  - `python quick_start.py` → launches Streamlit or generates sample wavs via `MurrTTS`.
- CI basics:
  - `.github/workflows/ci.yml` runs Ruff lint and smoke-imports both `MurrTTS/MurrVC` and legacy `ChatterboxTTS/ChatterboxVC`.

## Conventions and decisions
- Branding: use `MurrTTS`/`MurrVC` in examples and docs. The package name remains `chatterbox-tts` for compatibility; do not change import roots.
- No watermarking: any Perth/watermark code and deps were removed; don’t reintroduce.
- No Gradio: Streamlit and FastAPI are the supported UIs; avoid adding Gradio code/deps.
- Devices: Prefer MPS on Apple Silicon, CUDA if available, else CPU; mirror the detection pattern in examples.
- Audio I/O: Use `torchaudio.save(..., wav, model.sr)`; `wav` is a torch tensor (1, N).

## Extension points (with examples)
- Add a new API endpoint: edit `apps/api/advanced_voice_api.py`; load models via the service class; return files with `FileResponse` and stream via `StreamingResponse`.
- Modify UI: update `apps/streamlit/enhanced_voice_platform.py`; models are lazily loaded via `MurrTTS/MurrVC` and cached in the instance.
- Core inference tweaks: touch `src/chatterbox/models/t3/t3.py` only if needed; respect:
  - Initial speech tokens are BOS; don’t add duplicate BOS.
  - CFG duplicates batch; uncond branch zeros the text segment; combine logits `cond + w*(cond - uncond)`.
  - Only add positional embeddings when `hp.input_pos_emb == "learned"`.

## Gotchas
- Keep repo id constant for weights in TTS/VC (`REPO_ID = "ResembleAI/chatterbox"` inside `tts.py`/`vc.py`).
- Examples and docs assume `from chatterbox import MurrTTS, MurrVC`; changing this breaks CI and tutorials.
- Don’t commit build artifacts (`src/chatterbox_tts.egg-info/*` were removed; `.gitignore` excludes them).

## File map you’ll touch most
- Public surface: `src/chatterbox/__init__.py`, `src/chatterbox/tts.py`, `src/chatterbox/vc.py`.
- Apps: `apps/api/advanced_voice_api.py`, `apps/streamlit/enhanced_voice_platform.py`.
- Docs/Guides: `README.md`, `SETUP_GUIDE.md`, `ENHANCED_README.md`.

Keep changes minimal and aligned with these patterns. If adding features, update both a Streamlit UI action and an API endpoint for parity.
