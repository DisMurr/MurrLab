#!/usr/bin/env python3
"""
Enhanced Voice Platform Setup & Launcher
Automatically downloads datasets, sets up models, and launches all interfaces
"""

import subprocess
import sys
import os
import threading
import time
from pathlib import Path
import webbrowser

def run_command(command, description):
    """Run a command with description"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_python_environment():
    """Check if we're in the correct Python environment"""
    python_path = sys.executable
    if ".venv" in python_path or "chatterbox" in python_path:
        print(f"✅ Using Python environment: {python_path}")
        return True
    else:
        print(f"⚠️  Warning: Not using virtual environment: {python_path}")
        return True

def download_datasets():
    """Download voice datasets"""
    print("\n📁 Setting up voice datasets...")
    
    # Run dataset manager
    dataset_command = f"{sys.executable} voice_dataset_manager.py"
    return run_command(dataset_command, "Downloading voice datasets")

def launch_streamlit_app():
    """Launch the main Streamlit interface"""
    print("\n🌐 Launching Streamlit interface...")
    
    def run_streamlit():
        command = f"{sys.executable} -m streamlit run enhanced_voice_platform.py --server.port 8501"
        subprocess.run(command, shell=True)
    
    thread = threading.Thread(target=run_streamlit, daemon=True)
    thread.start()
    return thread

def launch_fastapi_server():
    """Launch the FastAPI server"""
    print("\n🚀 Launching FastAPI server...")
    
    def run_fastapi():
        command = f"{sys.executable} advanced_voice_api.py"
        subprocess.run(command, shell=True)
    
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    return thread

def launch_gradio_interfaces():
    """Launch Gradio interfaces"""
    print("\n🎭 Launching Gradio interfaces...")
    
    def run_tts_gradio():
        command = f"{sys.executable} gradio_tts_app.py"
        subprocess.run(command, shell=True)
    
    def run_vc_gradio():
        command = f"{sys.executable} gradio_vc_app.py"
        subprocess.run(command, shell=True)
    
    # Start TTS interface on port 7860
    tts_thread = threading.Thread(target=run_tts_gradio, daemon=True)
    tts_thread.start()
    
    time.sleep(5)  # Wait a bit before starting second interface
    
    # Start VC interface on different port
    vc_thread = threading.Thread(target=run_vc_gradio, daemon=True)
    vc_thread.start()
    
    return tts_thread, vc_thread

def create_desktop_shortcuts():
    """Create desktop shortcuts for easy access"""
    print("\n🔗 Creating access shortcuts...")
    
    shortcuts = {
        "Streamlit_Voice_Platform.url": "http://localhost:8501",
        "FastAPI_Voice_API.url": "http://localhost:8000",
        "Gradio_TTS.url": "http://localhost:7860",
        "API_Documentation.url": "http://localhost:8000/docs"
    }
    
    for filename, url in shortcuts.items():
        try:
            with open(filename, 'w') as f:
                f.write(f"[InternetShortcut]\nURL={url}\n")
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Failed to create {filename}: {e}")

def show_interface_urls():
    """Display all available interfaces"""
    print("\n" + "="*60)
    print("🎭 ENHANCED AI VOICE PLATFORM - ALL INTERFACES READY!")
    print("="*60)
    
    interfaces = [
        ("🌟 Main Streamlit Platform", "http://localhost:8501", "Full-featured voice platform"),
        ("🚀 FastAPI Server", "http://localhost:8000", "REST API for voice services"),
        ("📚 API Documentation", "http://localhost:8000/docs", "Interactive API docs"),
        ("🎤 Gradio TTS Interface", "http://localhost:7860", "Text-to-speech web UI"),
        ("🔄 Gradio Voice Conversion", "http://localhost:7861", "Voice conversion web UI"),
    ]
    
    for name, url, description in interfaces:
        print(f"\n{name}")
        print(f"   URL: {url}")
        print(f"   Info: {description}")
    
    print("\n" + "="*60)
    print("💡 FEATURES AVAILABLE:")
    print("   • Text-to-Speech with emotion control")
    print("   • Voice conversion and cloning")
    print("   • Real-time audio recording")
    print("   • Voice analysis and enhancement")
    print("   • Multiple open-source datasets")
    print("   • Custom voice profiles")
    print("   • Batch processing")
    print("   • Multi-language support")
    print("   • REST API for integration")
    print("="*60)

def main():
    """Main setup and launch function"""
    print("🎭 ENHANCED AI VOICE PLATFORM SETUP")
    print("="*50)
    
    # Check environment
    if not check_python_environment():
        print("⚠️  Environment check failed, but continuing...")
    
    # Download datasets (optional, can be skipped if taking too long)
    print("\n📋 Setup Options:")
    download_choice = input("Download voice datasets? (y/n, default=n): ").lower().strip()
    
    if download_choice == 'y':
        download_datasets()
    else:
        print("⏭️  Skipping dataset download (you can run voice_dataset_manager.py later)")
    
    # Create shortcuts
    create_desktop_shortcuts()
    
    print("\n🚀 Launching all interfaces...")
    
    # Launch all services
    streamlit_thread = launch_streamlit_app()
    time.sleep(3)
    
    fastapi_thread = launch_fastapi_server()
    time.sleep(3)
    
    gradio_threads = launch_gradio_interfaces()
    time.sleep(5)
    
    # Show URLs
    show_interface_urls()
    
    # Auto-open main interface
    try:
        webbrowser.open("http://localhost:8501")
        print("\n🌐 Opened main interface in your default browser")
    except:
        print("\n🌐 Please open http://localhost:8501 in your browser")
    
    print("\n⌨️  Press Ctrl+C to stop all services")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all services...")
        print("👋 Thank you for using Enhanced AI Voice Platform!")

if __name__ == "__main__":
    main()
