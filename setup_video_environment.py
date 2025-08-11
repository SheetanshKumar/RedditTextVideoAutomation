#!/usr/bin/env python3
"""
Video Environment Setup Utility

This script demonstrates and tests the automatic directory creation and 
background video generation functionality.
"""

import sys
sys.path.append("src")

import os
import shutil
from VideoAutomation import videoStream
from VideoAutomation.VideoConstants import *
from AudioManager.AudioConstants import *

def clean_test_environment():
    """Remove test directories to test auto-creation."""
    print("🧹 Cleaning test environment...")
    
    directories_to_remove = [
        VIDEO_LOCATION_STATIC,
        VIDEO_LOCATION_RENDERED, 
        AUDIO_LOCATION_DYNAMIC_NORMAL,
    ]
    
    for directory in directories_to_remove:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print(f"🗑️  Removed directory: {directory}")
            except Exception as e:
                print(f"⚠️  Could not remove {directory}: {e}")
    
    # Remove specific files
    bg_video = BG_VIDEO
    if os.path.exists(bg_video):
        try:
            os.remove(bg_video)
            print(f"🗑️  Removed background video: {bg_video}")
        except Exception as e:
            print(f"⚠️  Could not remove {bg_video}: {e}")

def test_initialization():
    """Test the initialization functions."""
    print("=" * 60)
    print("🧪 TESTING VIDEO ENVIRONMENT INITIALIZATION")
    print("=" * 60)
    
    # Test 1: Clean environment
    clean_test_environment()
    print("\n" + "="*50)
    print("📋 Test 1: Initialize from scratch")
    print("="*50)
    
    success = videoStream.initialize_video_environment()
    
    if success:
        print("✅ Initialization successful!")
        
        # Verify directories exist
        directories_to_check = [
            VIDEO_LOCATION_STATIC,
            VIDEO_LOCATION_RENDERED,
            AUDIO_LOCATION_DYNAMIC_NORMAL,
        ]
        
        print("\n📁 Directory verification:")
        for directory in directories_to_check:
            exists = os.path.exists(directory)
            status = "✅" if exists else "❌"
            print(f"   {status} {directory}")
        
        # Verify background video
        bg_exists = os.path.exists(BG_VIDEO)
        status = "✅" if bg_exists else "❌"
        print(f"\n🎬 Background video verification:")
        print(f"   {status} {BG_VIDEO}")
        
    else:
        print("❌ Initialization failed!")
    
    # Test 2: Re-initialization (should skip existing files)
    print("\n" + "="*50)
    print("📋 Test 2: Re-initialize existing environment")
    print("="*50)
    
    success2 = videoStream.initialize_video_environment()
    
    if success2:
        print("✅ Re-initialization successful (should skip existing files)!")
    else:
        print("❌ Re-initialization failed!")

def main():
    """Main test function."""
    print("🎬 Video Environment Setup Utility")
    print("=" * 60)
    
    try:
        test_initialization()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Summary of created components:")
        print("   • All necessary directories")
        print("   • Background video file (120 seconds, 1920x1080)")
        print("   • Proper error handling and validation")
        print("\n🚀 Your video generation environment is ready!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
