"""
Backward-compatible shim to the new location: apps/gradio/vc_app.py
Run: python -m apps.gradio.vc_app
"""

from apps.gradio.vc_app import demo

if __name__ == "__main__":
    demo.launch()
