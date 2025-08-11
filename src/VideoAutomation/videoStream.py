#!/usr/bin/env python3

"""
Enhanced Video Stream Module with Directory Management and Auto-Setup

This module provides complete video generation functionality with:
- Automatic directory creation
- Background video generation
- Robust error handling
- OpenCV standard text rendering (no freetype dependency)
"""

import sys
sys.path.append("..")

import cv2
import os
import subprocess
from src.VideoAutomation.VideoConstants import *
from src.VideoAutomation.photoFrameUtils import *
from src.VideoAutomation.screenTextHandler import *
from . import videoUtils as vu
from src.AudioManager.AudioUtils import *
from src.AudioManager.AudioConstants import *


def ensure_directories_exist():
    """Create all necessary directories if they don't exist."""
    directories = [
        VIDEO_LOCATION_STATIC,
        VIDEO_LOCATION_RENDERED,
        AUDIO_LOCATION_DYNAMIC_NORMAL,
        os.path.dirname(MEDIA_LOCATION)
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                print(f"❌ Error creating directory {directory}: {e}")
                raise


def create_background_video(output_path, duration=120, width=1920, height=1080, color='black'):
    """Create a background video using ffmpeg if it doesn't exist."""
    if os.path.exists(output_path):
        return True
        
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        print(f"🎬 Creating background video: {output_path}")
        
        cmd = [
            'ffmpeg', '-f', 'lavfi',
            '-i', f'color=size={width}x{height}:duration={duration}:rate=25:color={color}',
            '-c:v', 'libx264', '-t', str(duration), '-pix_fmt', 'yuv420p', '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.returncode == 0
    except:
        return False


def validate_background_video(video_path):
    """Validate that the background video exists and is readable."""
    if not os.path.exists(video_path):
        print(f"⚠️  Background video not found: {video_path}")
        return create_background_video(video_path)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        try:
            os.remove(video_path)
        except:
            pass
        return create_background_video(video_path)
    else:
        cap.release()
        print(f"✅ Background video validated: {video_path}")
        return True


def set_screen_text_simple(frame, data):
    """Simplified text rendering using standard OpenCV."""
    wrap = StringManipulator()
    lines = wrap.wrap_in_lines([data], TEXT_CHAR_WRAP)
    text_x = TEXT_POS_X
    text_y = TEXT_POS_Y
    increase_y = 0
    
    for text in lines:
        text = text.strip()
        if text:
            cv2.putText(frame, text, (text_x, text_y + increase_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, TEXT_COLOR, 2, cv2.LINE_AA)
            increase_y += TEXT_HORIZONTAL_SEPARATE
    return frame


def get_title_dimensions(title, left_boundary_pos, right_boundary_pos):
    """Calculate title position and size."""
    title_size = DEFAULT_TITLE_SIZE
    if len(title) > 20:
        div = len(title)/20
        title_size = int(title_size//div)
    start_pos_x = left_boundary_pos[0] + 80
    start_pos_y = left_boundary_pos[1] + (right_boundary_pos[1] - left_boundary_pos[1])//2
    return [(start_pos_x, start_pos_y), title_size]


def render_video(cap, out, rdata, screen_time_map):
    """Render video with enhanced error handling."""
    print("Rendering Video")
    if not all([cap, out, rdata, screen_time_map]):
        print("Something is None in render Video")
        return

    screen_time_map_keys = list(screen_time_map.keys())
    time_per_screen = list(screen_time_map.values())
    detail_per_second = time_per_screen[0] * FRAME_RATE

    keyCount = 0
    frameCount = 0.0
    video_time = int(get_audio_duration(MAIN_AUDIO))
    current_screen_type = screen_time_map_keys[keyCount].split('_')[0]
    current_screen_type_count = 0
    print(f"Video duration: {video_time} seconds")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Add UI elements
        frame = put_rectangle_on_img(frame, MAIN_RECT_TOP_LEFT, MAIN_RECT_TOP_RIGHT, MAIN_RECT_COLOR, MAIN_RECT_OPACITY)
        frame = put_boundary_in_rectangle(frame, MAIN_RECT_TOP_LEFT, MAIN_RECT_TOP_RIGHT, BOUNDARY_COLOR)
        
        # Render content based on screen type
        if current_screen_type.lower() == "title":
            screen_text = rdata['title']
            title_position, title_size = get_title_dimensions(screen_text, MAIN_RECT_TOP_LEFT, MAIN_RECT_TOP_RIGHT)
            cv2.putText(frame, screen_text, title_position, cv2.FONT_HERSHEY_SIMPLEX, 
                       title_size/50, DEFAULT_TITLE_COLOR, 2, cv2.LINE_AA)

        elif current_screen_type.lower() == "body":
            if current_screen_type_count < len(rdata['body']):
                screen_text = rdata['body'][current_screen_type_count]
                frame = set_screen_text_simple(frame, screen_text)

        # Handle screen transitions
        if keyCount < len(screen_time_map_keys) - 1 and frameCount > detail_per_second:
            keyCount += 1
            current_screen_type = screen_time_map_keys[keyCount].split('_')[0]
            current_screen_type_count = int(screen_time_map_keys[keyCount].split('_')[1].replace('.mp3', ''))
            frameCount = 0.0
            detail_per_second = time_per_screen[keyCount] * FRAME_RATE
            print(f"Switched to: {current_screen_type} {current_screen_type_count}")

        frameCount += 1.0
        out.write(frame)
        cv2.imshow('frame', frame)

        # Exit conditions
        if (cap.get(cv2.CAP_PROP_POS_FRAMES) + 1 >= FRAME_RATE * video_time or 
            cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def create_video(screen_time_map, rdata):
    """Create video with proper validation."""
    ensure_directories_exist()
    
    if not validate_background_video(BG_VIDEO):
        raise RuntimeError("Failed to create or validate background video")
    
    cap_background = cv2.VideoCapture(BG_VIDEO)
    if not cap_background.isOpened():
        raise RuntimeError(f"Cannot open background video: {BG_VIDEO}")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_filename = os.path.join(VIDEO_LOCATION_RENDERED, 'test1' + OUTPUT_VIDEO_FORMAT)
    
    out = cv2.VideoWriter(output_filename, fourcc, FRAME_RATE, OUTPUT_VIDEO_DIMENSIONS)
    if not out.isOpened():
        cap_background.release()
        raise RuntimeError(f"Cannot create video writer for: {output_filename}")
    
    print(f"🎬 Starting video creation: {output_filename}")
    
    try:
        render_video(cap_background, out, rdata, screen_time_map)
        print(f"✅ Video rendering completed: {output_filename}")
        
        output_filename_music = vu.add_audio_to_video(output_filename)
        print(f"✅ Audio added successfully: {output_filename_music}")
        
    except Exception as e:
        print(f"❌ Error during video creation: {e}")
        raise


def main_video_operator(screen_time_map, rdata):
    initialize_video_environment()
    """Main video processing function with comprehensive error handling."""
    print("🚀 Starting video generation pipeline...")
    print(f"📊 Screen time mapping: {screen_time_map}")
    
    try:
        create_video(screen_time_map, rdata)
        print("✅ Video generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def initialize_video_environment():
    """Initialize the video generation environment."""
    print("🔧 Initializing video generation environment...")
    
    try:
        ensure_directories_exist()
        
        if validate_background_video(BG_VIDEO):
            print("✅ Video environment initialized successfully!")
            return True
        else:
            print("❌ Failed to initialize video environment")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing video environment: {e}")
        return False
