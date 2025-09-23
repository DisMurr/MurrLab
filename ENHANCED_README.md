# 🎭 Enhanced AI Voice Platform

**The Ultimate Open Source Voice Synthesis & AI Platform**

Powered by the MurrLab Voice stack (MurrTTS + MurrVC) with integrated open-source datasets, advanced AI models, and multiple interfaces.

## 🌟 Features

### Core Voice Technologies
- **🎤 Advanced Text-to-Speech** - Emotion control, multiple voices, real-time generation
- **🔄 Voice Conversion & Cloning** - Convert speech between different speakers
- **🎙️ Speech Recognition** - Powered by OpenAI Whisper
- **🔧 Audio Enhancement** - Noise reduction, normalization, quality improvement
- **📊 Voice Analysis** - Comprehensive audio feature extraction

### AI & Datasets
- **📁 Integrated Datasets** - Mozilla Common Voice, LibriSpeech, LJ Speech, VCTK
- **🤖 Multiple AI Models** - MurrTTS, Whisper ASR, Voice Conversion
- **🌍 Multi-language Support** - English, Spanish, French, German, and more
- **🎯 Custom Voice Profiles** - Create and save personalized voice settings

### Interfaces & APIs
- **🌐 Streamlit Web Platform** - Full-featured interactive interface
- **🚀 FastAPI REST Service** - Professional API for integration
- **📱 Real-time Processing** - Live audio recording and processing

## 🚀 Quick Start

### 1. Launch Everything
```bash
# Run the comprehensive setup and launcher
python launch_platform.py
```

This will:
- Set up all AI models
- Download voice datasets (optional)
- Launch all web interfaces
- Create desktop shortcuts
- Open the main platform in your browser

### 2. Available Interfaces

After running the launcher, you'll have access to:

| Interface | URL | Purpose |
|-----------|-----|---------|
| 🌟 **Main Platform** | http://localhost:8501 | Full-featured Streamlit interface |
| 🚀 **API Server** | http://localhost:8000 | REST API for developers |
| 📚 **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| 🎤 **TTS Interface** | http://localhost:7860 | Simple text-to-speech |
| 🔄 **Voice Conversion** | http://localhost:7861 | Voice cloning interface |

## 📁 Project Structure

```
MurrLab/
├── enhanced_voice_platform.py          # Shim to apps/streamlit/enhanced_voice_platform.py
├── apps/
│   ├── api/advanced_voice_api.py       # FastAPI REST service
│   └── streamlit/enhanced_voice_platform.py  # Streamlit UI
├── examples/
│   ├── example_tts.py
│   └── example_vc.py
├── src/chatterbox/                     # Core engines (module path kept for compat)
├── launch_platform.py                  # Orchestration script
├── voice_dataset_manager.py            # Dataset utilities
└── *.wav                               # Generated audio files
```

## 🎯 Usage Examples

### Basic Text-to-Speech
```python
from chatterbox import MurrTTS

model = MurrTTS.from_pretrained(device="mps")
wav = model.generate("Hello, world!", exaggeration=0.7, cfg_weight=0.4)
```

### Voice Conversion
```python
from chatterbox import MurrVC

model = MurrVC.from_pretrained(device="mps")
converted = model.generate(
    audio="source.wav",
    target_voice_path="target_voice.wav"
)
```

### API Usage
```bash
# Text-to-speech via API
curl -X POST "http://localhost:8000/tts/" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello API!", "exaggeration": 0.8}' \
     --output speech.wav

# Voice conversion via API
curl -X POST "http://localhost:8000/voice-conversion/" \
     -F "source_audio=@source.wav" \
     -F "target_audio=@target.wav" \
     --output converted.wav
```

## 🎛️ Voice Control Parameters

### Exaggeration (0.0 - 2.0+)
- **0.2-0.4**: Calm, meditative
- **0.5**: Neutral (default)
- **0.8-1.0**: Expressive, emotional
- **1.2+**: Highly dramatic, excited

### CFG Weight (0.0 - 1.0)
- **0.3**: Fast, dynamic speech
- **0.5**: Balanced (default)
- **0.7+**: Stable, controlled

## 🗃️ Integrated Datasets

### Mozilla Common Voice
- **Languages**: 100+ languages
- **Size**: Varies by language
- **Use**: Multi-speaker, diverse accents

### LibriSpeech
- **Content**: English audiobook readings
- **Size**: 960 hours
- **Use**: High-quality English speech

### LJ Speech
- **Speaker**: Single female speaker (Linda Johnson)
- **Size**: 24 hours
- **Use**: Consistent voice training

### VCTK Corpus
- **Speakers**: 110 English speakers
- **Size**: 44 hours
- **Use**: Multi-speaker English

## 🔧 Advanced Features

### Custom Voice Profiles
Create personalized voice settings:
```python
platform.create_voice_profile(
    name="my_character",
    exaggeration=1.0,
    cfg_weight=0.4,
    description="Energetic character voice"
)
```

### Batch Processing
Process entire datasets:
```bash
python voice_dataset_manager.py
```

### Audio Enhancement
Improve audio quality:
- Noise reduction
- Audio normalization
- Dynamic range optimization

### Real-time Features
- Live audio recording
- Streaming TTS generation
- Real-time voice conversion

## 🛠️ API Endpoints

### Text-to-Speech
- `POST /tts/` - Generate speech from text
- `POST /tts/stream/` - Stream speech generation

### Voice Conversion
- `POST /voice-conversion/` - Convert voice between speakers

### Analysis
- `POST /analyze-voice/` - Extract voice features
- `POST /enhance-audio/` - Improve audio quality
- `POST /transcribe/` - Speech-to-text

### Management
- `GET /voice-profiles/` - List voice profiles
- `POST /voice-profiles/` - Create voice profile
- `DELETE /voice-profiles/{name}` - Delete profile

## 🔬 Research & Development

### Experiment with Models
```python
# Try different model configurations
from enhanced_voice_platform import EnhancedVoicePlatform

platform = EnhancedVoicePlatform()
platform.initialize_models()

# Batch process datasets
results = platform.batch_process_dataset("common_voice", "tts")
```

### Custom Training Data
Use the dataset manager to prepare training data:
```python
from voice_dataset_manager import VoiceDatasetManager

manager = VoiceDatasetManager()
manager.download_common_voice("en", max_samples=1000)
manager.create_training_splits(dataset_path)
```

## 🤝 Contributing

This enhanced platform builds upon:
- [MurrLab Voice (TTS/VC) models packaged under chatterbox module path]
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Mozilla Common Voice](https://commonvoice.mozilla.org/)
- [LibriSpeech](http://www.openslr.org/12/)

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## 🎯 Next Steps

1. **Start with the main platform**: `python launch_platform.py`
2. **Explore the Streamlit interface** for full functionality
3. **Try the API** for integration projects
4. **Download datasets** for enhanced training data
5. **Create custom voice profiles** for your specific needs

## 🆘 Troubleshooting

### Common Issues
- **Memory errors**: Reduce batch sizes or use CPU instead of GPU
- **Audio format issues**: Ensure audio files are in WAV format
- **Port conflicts**: Change ports in the launch script if needed
- **Dataset downloads**: Skip dataset download if it takes too long

### Performance Tips
- Use **MPS** (Apple Silicon) or **CUDA** (NVIDIA) for faster processing
- **Limit sample rates** to 22050 Hz for faster generation
- **Use shorter texts** for real-time applications

---

🎭 **Enhanced AI Voice Platform** - Transform text into natural speech with the power of open-source AI!
