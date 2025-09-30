#!/usr/bin/env python3
"""
Web deployment script for Cover Letter Generator.

This script provides different options for making the application accessible on the web.
"""

import gradio as gr
from app import create_interface

def main():
    """Launch the application with web access enabled."""
    print("🚀 Starting Cover Letter Generator for Web Access...")
    print("📱 Creating Gradio interface...")
    
    # Create the interface
    interface = create_interface()
    
    print("\n" + "="*60)
    print("🌍 WEB ACCESS OPTIONS:")
    print("="*60)
    print("1. LOCAL NETWORK ACCESS:")
    print("   - Access from other devices on your network")
    print("   - URL: http://YOUR_IP_ADDRESS:7860")
    print("   - Find your IP with: ipconfig (Windows) or ifconfig (Mac/Linux)")
    print()
    print("2. PUBLIC INTERNET ACCESS:")
    print("   - Gradio will create a public URL (e.g., https://xxxxx.gradio.live)")
    print("   - Anyone with the URL can access your app")
    print("   - URL will be displayed below when launched")
    print()
    print("3. CUSTOM DOMAIN (Advanced):")
    print("   - Deploy to cloud services like Hugging Face Spaces")
    print("   - Use services like ngrok for custom domains")
    print("="*60)
    print()
    
    # Launch with web access
    try:
        print("🚀 Launching with web access enabled...")
        interface.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=7860,
            share=True,  # Enable Gradio's public sharing
            show_error=True,
            quiet=False,
            inbrowser=True
        )
    except Exception as e:
        print(f"❌ Error launching: {e}")
        print("💡 Try running: python app.py (for local access only)")

if __name__ == "__main__":
    main()
