"""
Backward-compatible shim to the new location: apps/gradio/tts_app.py
Run: python -m apps.gradio.tts_app
"""

from apps.gradio.tts_app import demo

if __name__ == "__main__":
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch(share=True)
