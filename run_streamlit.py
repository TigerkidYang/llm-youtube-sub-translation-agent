#!/usr/bin/env python3
"""
Streamlit Web Application Launch Script
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_requirements():
    """Check necessary dependencies and configuration"""
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Please install Streamlit first: pip install streamlit")
        return False
    
    # Check OpenAI API Key
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not detected")
        print("Please set your OpenAI API Key:")
        print("Method 1: Create .env file and add OPENAI_API_KEY=your_key_here")
        print("Method 2: Set environment variable export OPENAI_API_KEY=your_key_here")
        
        # Allow user to input API Key
        api_key = input("\nOr enter API Key now (leave empty to skip): ").strip()
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            print("✅ API Key temporarily set")
        else:
            print("⚠️  No API Key will prevent translation functionality")
    else:
        print("✅ OpenAI API Key is configured")
    
    return True

def main():
    print("🎬 YouTube Subtitle AI Translator - Streamlit Version")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    print("\n🚀 Starting Streamlit application...")
    print("📝 The application will open in your default browser")
    print("🔗 If it doesn't open automatically, visit: http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "streamlit_app.py")
    
    try:
        # Launch Streamlit application
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.serverAddress", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

if __name__ == "__main__":
    main() 