#!/usr/bin/env python3
"""
Cache Cleanup Script for AI Projects
Removes Python cache files and Gradio temporary files
"""

import os
import shutil
import glob
from pathlib import Path

def clean_python_cache():
    """Remove Python __pycache__ directories and .pyc files"""
    print("🧹 Cleaning Python cache files...")
    
    # Find and remove __pycache__ directories
    pycache_dirs = []
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                pycache_dirs.append(pycache_path)
    
    # Remove __pycache__ directories
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            print(f"  ✅ Removed: {pycache_dir}")
        except Exception as e:
            print(f"  ❌ Error removing {pycache_dir}: {e}")
    
    # Find and remove .pyc files
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"  ✅ Removed: {pyc_file}")
        except Exception as e:
            print(f"  ❌ Error removing {pyc_file}: {e}")

def clean_gradio_cache():
    """Remove Gradio cache and temporary files"""
    print("🧹 Cleaning Gradio cache files...")
    
    # Common Gradio cache locations
    gradio_cache_paths = [
        os.path.expanduser("~/.gradio/"),
        os.path.expanduser("~/.cache/gradio/"),
        "./gradio_cached_examples/",
        "./tmp/"
    ]
    
    for cache_path in gradio_cache_paths:
        if os.path.exists(cache_path):
            try:
                shutil.rmtree(cache_path)
                print(f"  ✅ Removed: {cache_path}")
            except Exception as e:
                print(f"  ❌ Error removing {cache_path}: {e}")

def clean_temp_files():
    """Remove temporary files created during development"""
    print("🧹 Cleaning temporary files...")
    
    # Common temporary file patterns
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*.log",
        "*.pid",
        ".DS_Store"
    ]
    
    for pattern in temp_patterns:
        temp_files = glob.glob(pattern, recursive=True)
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
                print(f"  ✅ Removed: {temp_file}")
            except Exception as e:
                print(f"  ❌ Error removing {temp_file}: {e}")

def show_cache_info():
    """Show information about cache files"""
    print("📊 Cache File Information:")
    print("=" * 50)
    
    # Python cache info
    pycache_count = 0
    pyc_count = 0
    
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_count += 1
        for file in files:
            if file.endswith('.pyc'):
                pyc_count += 1
    
    print(f"📁 __pycache__ directories: {pycache_count}")
    print(f"🐍 .pyc files: {pyc_count}")
    
    # Gradio cache info
    gradio_caches = []
    for cache_path in [os.path.expanduser("~/.gradio/"), os.path.expanduser("~/.cache/gradio/")]:
        if os.path.exists(cache_path):
            gradio_caches.append(cache_path)
    
    print(f"🎨 Gradio cache locations: {len(gradio_caches)}")
    for cache in gradio_caches:
        print(f"   - {cache}")

def main():
    """Main cleanup function"""
    print("🚀 AI Projects Cache Cleanup Tool")
    print("=" * 40)
    
    # Show current cache info
    show_cache_info()
    print()
    
    # Ask user what to clean
    print("What would you like to clean?")
    print("1. Python cache files (__pycache__, .pyc)")
    print("2. Gradio cache files")
    print("3. Temporary files")
    print("4. Everything")
    print("5. Show cache info only")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            clean_python_cache()
        elif choice == '2':
            clean_gradio_cache()
        elif choice == '3':
            clean_temp_files()
        elif choice == '4':
            clean_python_cache()
            clean_gradio_cache()
            clean_temp_files()
        elif choice == '5':
            show_cache_info()
        else:
            print("❌ Invalid choice. Please run the script again.")
            return
        
        print("\n✅ Cleanup completed!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Cleanup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")

if __name__ == "__main__":
    main()

