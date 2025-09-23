# 🚀 MurrLab Setup Guide

## 📋 **Prerequisites**

- Python 3.9+ (3.13 recommended)
- macOS with Apple Silicon (for MPS support) or any OS with CUDA/CPU
- Git installed
- 4GB+ RAM recommended
- 2GB+ disk space

## 🛠️ **Quick Setup (5 minutes)**

### 1. **Clone Repository**
```bash
git clone https://github.com/DisMurr/MurrLab.git
cd MurrLab
```

### 2. **Create Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### 3. **Install Core Package**
```bash
pip install -e .
```

### 4. **Install Enhanced Features**
```bash
pip install streamlit fastapi uvicorn
pip install openai-whisper pyannote.audio noisereduce
pip install pandas plotly matplotlib seaborn
```

### 5. **Test Installation**
```bash
python quick_start.py
```

## 🎯 **Quick Test Commands**

### **Verify Core System**
```bash
python -c "from chatterbox import MurrTTS; print('✅ Core TTS working!')"
```

### **Generate Test Audio**
```bash
python test_tts_fixes.py
```

### **Launch Web Interface**
```bash
# Streamlit platform
streamlit run enhanced_voice_platform.py
```

## 🌐 **Interface Options**

### **📊 Enhanced Streamlit Platform**
```bash
streamlit run enhanced_voice_platform.py
# Opens at: http://localhost:8501
```

### **🔌 FastAPI REST Service**
```bash
python advanced_voice_api.py
# API docs at: http://localhost:8000/docs
```

### **💻 Interactive CLI**
```bash
python quick_start.py
# Follow menu prompts
```

## 🎵 **Usage Examples**

### **Basic Text-to-Speech**
```python
from chatterbox import MurrTTS
import torchaudio

# Load model
model = MurrTTS.from_pretrained(device="mps")  # or "cpu"

# Generate speech
text = "Welcome to MurrLab AI voice platform!"
wav = model.generate(text)

# Save audio
torchaudio.save("my_speech.wav", wav, model.sr)
print("Audio saved as my_speech.wav")
```

### **Voice Conversion**
```python
from chatterbox import MurrVC

vc = MurrVC.from_pretrained(device="mps")
# Note: Requires reference audio files
```

### **Advanced TTS with Emotion**
```python
model = MurrTTS.from_pretrained(device="mps")

# Generate with emotion control
wav = model.generate(
    text="This is emotional speech!",
    exaggeration=0.8,  # Higher = more emotional
    temperature=0.7    # Lower = more consistent
)
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# If chatterbox module not found (installed via -e .):
pip install -e .

# If dependencies missing:
pip install -r requirements.txt  # (if available)
```

#### **Device Issues**
```python
# Check device availability
import torch
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Force CPU if needed
model = MurrTTS.from_pretrained(device="cpu")
```

#### **Audio Issues**
```bash
# Install audio backends
pip install soundfile librosa torchaudio

# macOS specific
brew install ffmpeg
```

### **Performance Tips**

#### **Apple Silicon (MPS)**
- Use `device="mps"` for best performance
- Ensure macOS 12.3+ for MPS support
- 8GB+ RAM recommended

#### **Memory Management**
```python
# Clear cache if memory issues
import torch
torch.mps.empty_cache()  # For MPS
# torch.cuda.empty_cache()  # For CUDA
```

## 📁 **File Organization**

### **Keep These Files**
- `src/` - Core system code
- `*.py` - Interface and example files
- `README_MURRLAB.md` - Main documentation
- `pyproject.toml` - Package configuration
- `LICENSE` - MIT license

### **Optional to Remove**
- `*.wav` files (if not needed as examples)
- `.venv/` (virtual environment)
- `__pycache__/` directories
- `.DS_Store` files

## 🌟 **Next Steps**

1. **Explore Interfaces**: Try different web and CLI interfaces
2. **Generate Audio**: Create your own TTS samples
3. **Experiment**: Use `my_tts_experiments.py` as starting point
4. **Customize**: Modify parameters for your use case
5. **Develop**: Build on the platform for your projects

## 🆘 **Support**

If you encounter issues:

1. Check the comprehensive audit: `COMPREHENSIVE_FILE_AUDIT.md`
2. Review error fixes: `ERROR_FIXES_COMPLETE.md`
3. Try the quick start: `python quick_start.py`
4. Check Python version: `python --version` (needs 3.9+)

## 🎉 **Success!**

When setup is complete, you should be able to:
- ✅ Import MurrTTS without errors
- ✅ Generate audio files
- ✅ Launch web interfaces
- ✅ Use CLI tools

**Welcome to MurrLab! 🎭🚀**
