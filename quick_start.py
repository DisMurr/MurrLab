#!/usr/bin/env python3
"""
Fixed Enhanced Voice Platform - Quick Start Script
Handles errors gracefully and provides working interfaces
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
            print(f"❌ Missing {file} - make sure you're in the chatterbox directory")
            return False
    
    print("✅ Environment check passed")
    return True

def start_basic_interface():
    """Start the most basic working interface"""
    print("\n🎯 Starting Basic TTS Interface...")
    
    # Create a simple working script
    simple_script = """
import sys
import torch
import torchaudio
import gradio as gr
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path.cwd() / "src"))

try:
    from chatterbox.tts import ChatterboxTTS
    
    # Global model
    model = None
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    def load_model():
        global model
        if model is None:
            model = ChatterboxTTS.from_pretrained(device=device)
        return model
    
    def generate_speech(text, exaggeration=0.5, cfg_weight=0.5):
        try:
            if not text.strip():
                return None, "Please enter some text"
            
            tts_model = load_model()
            wav = tts_model.generate(text, exaggeration=exaggeration, cfg_weight=cfg_weight)
            
            # Save to file
            output_path = "generated_speech.wav"
            torchaudio.save(output_path, wav, tts_model.sr)
            
            return output_path, f"✅ Generated speech for: {text[:50]}..."
            
        except Exception as e:
            return None, f"❌ Error: {str(e)}"
    
    # Create Gradio interface
    with gr.Blocks(title="🎤 Chatterbox TTS") as interface:
        gr.Markdown("# 🎤 Chatterbox TTS - Simple Interface")
        gr.Markdown("Enter text below and adjust settings to generate speech")
        
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="Text to synthesize",
                    placeholder="Enter your text here...",
                    lines=3
                )
                
                with gr.Row():
                    exag_slider = gr.Slider(
                        minimum=0.0, 
                        maximum=2.0, 
                        value=0.5, 
                        step=0.1,
                        label="Exaggeration (Emotion)"
                    )
                    cfg_slider = gr.Slider(
                        minimum=0.0, 
                        maximum=1.0, 
                        value=0.5, 
                        step=0.1,
                        label="CFG Weight (Stability)"
                    )
                
                generate_btn = gr.Button("🎵 Generate Speech", variant="primary")
            
            with gr.Column():
                audio_output = gr.Audio(label="Generated Speech")
                status_output = gr.Textbox(label="Status", interactive=False)
        
        generate_btn.click(
            fn=generate_speech,
            inputs=[text_input, exag_slider, cfg_slider],
            outputs=[audio_output, status_output]
        )
        
        # Add examples
        gr.Examples(
            examples=[
                ["Hello! This is Chatterbox TTS in action.", 0.5, 0.5],
                ["I'm really excited about this new technology!", 1.2, 0.3],
                ["Welcome to our professional presentation.", 0.4, 0.6],
                ["Once upon a time in a magical land...", 0.7, 0.4]
            ],
            inputs=[text_input, exag_slider, cfg_slider]
        )
    
    print(f"🎤 Starting TTS interface on device: {device}")
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
    
except Exception as e:
    print(f"❌ Failed to start interface: {e}")
    print("📋 Please check that all dependencies are installed correctly")
"""
    
    # Write the script
    script_path = Path("simple_tts_interface.py")
    with open(script_path, "w") as f:
        f.write(simple_script)
    
    # Run it
    python_cmd = sys.executable
    command = f"{python_cmd} simple_tts_interface.py"
    
    print(f"🚀 Running: {command}")
    print("🌐 Interface will be available at: http://localhost:7860")
    print("⌨️ Press Ctrl+C to stop")
    
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Interface stopped")

def main():
    """Main function"""
    print("🎭 CHATTERBOX TTS - QUICK START")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return
    
    print("\n📋 What would you like to do?")
    print("1. 🎤 Start Simple TTS Interface (Recommended)")
    print("2. 🔧 Generate a few test audio files")
    print("3. 📊 Check system status")
    
    try:
        choice = input("\nEnter choice (1-3, default=1): ").strip()
        if not choice:
            choice = "1"
        
        if choice == "1":
            start_basic_interface()
        
        elif choice == "2":
            print("\n🎵 Generating test audio files...")
            test_script = f"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "src"))

import torch
import torchaudio
from chatterbox.tts import ChatterboxTTS

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {{device}}")

model = ChatterboxTTS.from_pretrained(device=device)

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
                from chatterbox.tts import ChatterboxTTS
                print("✅ Chatterbox TTS can be imported")
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
