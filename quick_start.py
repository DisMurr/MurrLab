#!/usr/bin/env python3
"""
MurrLab Voice - Quick Start Script
Clean, dependency-light quick start without Gradio.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command_safe(command, description, timeout=30):
    """Safely run a command with timeout and error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"⚠️ {description} completed with warnings: {result.stderr[:100]}...")
            return True  # Still continue for non-critical errors
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out, but continuing...")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_environment():
    """Check Python environment"""
    python_path = sys.executable
    print(f"🐍 Python: {python_path}")
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    expected_files = ["src/chatterbox/tts.py", "pyproject.toml"]
    
    for file in expected_files:
        if not (current_dir / file).exists():
            print(f"❌ Missing {file} - make sure you're in the MurrLab project directory")
            return False
    
    print("✅ Environment check passed")
    return True

def launch_streamlit_platform():
    """Launch the Streamlit platform app"""
    print("\n� Launching Streamlit platform (apps/streamlit/enhanced_voice_platform.py)...")
    python_cmd = sys.executable
    target = Path("enhanced_voice_platform.py")
    if not target.exists():
        print("❌ Could not find enhanced_voice_platform.py at project root")
        return
    try:
        subprocess.run(f"{python_cmd} {target}", shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit platform stopped")

def main():
    """Main function"""
    print("🎭 MurrLab Voice - Quick Start")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return
    
    print("\n📋 What would you like to do?")
    print("1. � Launch Streamlit platform (recommended)")
    print("2. 🔧 Generate a few test audio files")
    print("3. 📊 Check system status")
    
    try:
        choice = input("\nEnter choice (1-3, default=1): ").strip()
        if not choice:
            choice = "1"
        
        if choice == "1":
            launch_streamlit_platform()
        
        elif choice == "2":
            print("\n🎵 Generating test audio files...")
            test_script = f"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "src"))

import torch
import torchaudio
from chatterbox import MurrTTS

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {{device}}")

model = MurrTTS.from_pretrained(device=device)

tests = [
    ("Hello world! This is a test.", 0.5, 0.5, "test_neutral"),
    ("Wow! This is amazing!", 1.0, 0.3, "test_excited"),
    ("Good morning. Welcome to our presentation.", 0.3, 0.6, "test_professional")
]

for text, exag, cfg, name in tests:
    print(f"Generating {{name}}...")
    wav = model.generate(text, exaggeration=exag, cfg_weight=cfg)
    torchaudio.save(f"{{name}}.wav", wav, model.sr)
    print(f"✅ Saved {{name}}.wav")

print("🎉 Test files generated!")
"""
            
            # Run test generation
            result = subprocess.run(
                [sys.executable, "-c", test_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Test files generated successfully!")
                print("📁 Check the current directory for .wav files")
            else:
                print(f"❌ Error generating files: {result.stderr}")
        
        elif choice == "3":
            print("\n📊 System Status:")
            print(f"Python: {sys.executable}")
            print(f"Working Directory: {Path.cwd()}")
            print(f"PyTorch available: {__import__('torch').__version__}")
            
            try:
                import torch
                print(f"CUDA available: {torch.cuda.is_available()}")
                print(f"MPS available: {torch.backends.mps.is_available()}")
            except:
                pass
            
            # Check if models can be imported
            try:
                sys.path.insert(0, str(Path.cwd() / "src"))
                from chatterbox import MurrTTS
                print("✅ MurrTTS can be imported")
            except Exception as e:
                print(f"❌ Import error: {e}")
        
        else:
            print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
