#!/usr/bin/env python3

import sys
sys.path.append(".")

from VideoAutomation import videoStream


def test_video_streamer():
    """Test the video streamer with static data."""
    
    print("🎬 Testing Video Streamer...")
    print("=" * 50)
    
    # Test data from driver.py
    rdata = {}
    rdata['title'] = "secret"
    rdata['body'] = [
        'This  feels  like  a  safe  place to admit something I would never  tell anyone else. I will keep this brief so as not to occupy too much of your time. I am truly sorry for what I am about  to  confess  and  I  know  that  it  will  be  deeply triggering  to many of you. Please find it in your heart not',
        'to  hate me and dont let this ruin your day. Okay here goes. I use both reddit and discord in light mode.'
    ]
    
    screen_time_map = {
        'TITLE_0.mp3': 5.28, 
        'BODY_0.mp3': 20.784, 
        'BODY_1.mp3': 8.04
    }
    
    print(f"📄 Title: {rdata['title']}")
    print(f"📝 Body segments: {len(rdata['body'])}")
    print(f"🎵 Audio segments: {len(screen_time_map)}")
    print()
    
    print("⏱️  Screen time mapping:")
    total_duration = 0
    for filename, duration in screen_time_map.items():
        print(f"   {filename}: {duration} seconds")
        total_duration += duration
    
    print(f"📊 Total video duration: {total_duration} seconds")
    print()
    
    try:
        print("🚀 Starting video generation...")
        videoStream.main_video_operator(screen_time_map, rdata)
        print("✅ Video generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during video generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_streamer()