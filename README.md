# 🎭 MurrLab - Enhanced AI Voice Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

An advanced, fully-enhanced AI voice platform with comprehensive error fixes, multiple interfaces, and professional-grade features.

## 🚀 **What Makes MurrLab Special**

- **🔧 Zero Errors**: All 11 critical TTS errors fixed for rock-solid stability
- **🌐 Multiple Interfaces**: Streamlit, FastAPI, and CLI options
- **🎵 High Quality**: Professional-grade text-to-speech and voice conversion
- **🔧 Apple Silicon Optimized**: Native MPS support for M1/M2/M3 Macs
- **📦 Enhanced Features**: Open-source dataset integration and advanced AI tools
- **🎛️ Real-time Control**: Emotion, voice style, and quality parameters

## ✨ **Features**

### 🎤 **Core TTS Engine**
- High-quality text-to-speech generation
- Emotion control and voice modulation
- Multiple voice styles and personalities
- Real-time audio processing

### 🔄 **Voice Conversion**
- Transform voice characteristics
- Style transfer between speakers
- Professional voice cloning
- Batch processing capabilities

### 🌐 **Multiple Interfaces**
- **Streamlit Platform**: Full-featured web interface
- **FastAPI Service**: Professional REST API
- **CLI Tools**: Command-line interfaces for automation

### 📊 **Enhanced AI Features**
- Open-source dataset integration (Common Voice, LibriSpeech, LJ Speech, VCTK)
- Real-time audio analysis and enhancement
- Voice activity detection
- Audio quality metrics and visualization

## 🛠️ **Installation**

### **Quick Start**
```bash
git clone https://github.com/DisMurr/MurrLab.git
cd MurrLab
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### **Enhanced Installation with All Features**
```bash
pip install streamlit gradio fastapi datasets accelerate
pip install openai-whisper pyannote.audio noisereduce
pip install pandas plotly matplotlib seaborn
```

## 🎯 **Quick Usage**

### **🎤 Text-to-Speech**
```python
from chatterbox.tts import ChatterboxTTS

# Load model
model = ChatterboxTTS.from_pretrained(device="mps")  # or "cpu"

# Generate speech
wav = model.generate("Hello! Welcome to MurrLab AI voice platform.")

# Save audio
import torchaudio
torchaudio.save("output.wav", wav, model.sr)
```

### **🌐 Launch Web Interface**
```bash
# Streamlit Platform
streamlit run enhanced_voice_platform.py

# Quick Start Menu (optional)
python quick_start.py
```

### **🔄 Voice Conversion**
```python
from chatterbox.vc import ChatterboxVC

vc = ChatterboxVC.from_pretrained(device="mps")
converted_audio = vc.convert("source.wav", "target_voice.wav")
```

## 🎛️ **Interface Options**

| Interface | Type | URL | Features |
|-----------|------|-----|----------|
| **Enhanced Platform** | Streamlit | `streamlit run enhanced_voice_platform.py` | Full AI platform |
| **API Service** | FastAPI | `python advanced_voice_api.py` | REST API |
| **CLI Menu** | Terminal | `python quick_start.py` | Interactive CLI |

## 📁 **Project Structure**

```
MurrLab/
├── 🎤 Core System
│   ├── src/chatterbox/          # Main TTS/VC engines
│   ├── src/chatterbox/models/   # AI model architectures
│   └── pyproject.toml           # Project configuration
├── 🌐 Interfaces
│   ├── enhanced_voice_platform.py  # Full Streamlit platform
│   ├── advanced_voice_api.py       # FastAPI REST service
│   └── quick_start.py              # Interactive CLI
├── 🔧 Tools & Examples
│   ├── example_tts.py              # Basic TTS example
│   ├── example_vc.py               # Voice conversion example
│   ├── my_tts_experiments.py       # Custom experiments
│   └── voice_dataset_manager.py    # Dataset tools
├── 📊 Documentation
│   ├── README.md                   # This file
│   ├── ENHANCED_README.md          # Detailed features
│   ├── ERROR_FIXES_COMPLETE.md     # Fix documentation
│   └── COMPREHENSIVE_FILE_AUDIT.md # System validation
└── 🎵 Generated Audio
    ├── demo_*.wav                  # Example outputs
    └── *.wav                       # Generated samples
```

## 🔧 **Technical Improvements**

### **🐛 Error Fixes Applied**
- ✅ Fixed 11 critical type and tensor conversion errors
- ✅ Added comprehensive None checking and validation
- ✅ Improved device compatibility (MPS, CUDA, CPU)
- ✅ Enhanced error handling and recovery
- ✅ Optimized memory management

### **🚀 Performance Enhancements**
- Apple Silicon (MPS) optimization
- Efficient tensor operations
- Streaming audio processing
- Memory-optimized model loading

### **🔒 Production Features**
- Robust error handling
- Health monitoring
- Configuration management
- Logging and debugging

## 🎵 **Audio Examples**

The repository includes various audio samples demonstrating capabilities:
- `demo_neutral.wav` - Basic TTS output
- `demo_excited.wav` - Emotional expression
- `demo_emotional.wav` - Advanced emotion control
- `converted_to_professional.wav` - Voice conversion demo

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Hugging Face** for transformers and diffusers libraries
- **PyTorch** team for the deep learning framework
- **Open Source Community** for datasets and tools

## 📈 **System Status**

- ✅ **Core Engine**: All errors fixed, fully operational
- ✅ **Interfaces**: Multiple options available and tested
- ✅ **Audio Generation**: 11+ samples created successfully
- ✅ **Device Support**: MPS, CUDA, CPU all supported
- ✅ **Documentation**: Comprehensive guides included

---

**🚀 MurrLab - Where AI Voices Come to Life!**

*Built with ❤️ for the AI community*
