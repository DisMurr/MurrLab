#!/usr/bin/env python3
"""
Backward-compatible shim. The FastAPI service moved to apps/api/advanced_voice_api.py
Run: uvicorn apps.api.advanced_voice_api:app --reload
"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.advanced_voice_api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
