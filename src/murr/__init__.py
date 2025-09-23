try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # For Python <3.8

# Package distribution name updated
__version__ = version("murrlab-voice")

# Export public API
from .tts import MurrTTS
from .vc import MurrVC
