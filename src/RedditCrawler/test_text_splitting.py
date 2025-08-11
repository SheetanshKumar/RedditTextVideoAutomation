#!/usr/bin/env python3

import sys
sys.path.append("../..")

from src.RedditCrawler.RedditApi import RedditCrawler, PrawRedditCrawler
from src.VideoAutomation.screenTextHandler import StringManipulator
from src.VideoAutomation.VideoConstants import TEXT_CHAR_WRAP, LINES_PER_SCREEN

def test_split_body_per_screen():
    """Test the split_body_per_screen function with sample text."""
    
    # Sample long text to test
    sample_text = """I was 3 years old and living in a trailer in Kansas. Tornado Alley seems to have shifted east and a bit more south in the years since I was a toddler but tornados were a serious seasonal threat of which even at a young age I was very aware of. I remember standing on the steps of our trailer watching them far off in the distance. Scared the crap out of me. One evening I was outside with my mom and our next door neighbor. A thunderstorm was blowing in and I was upset and worried. My mom and neighbor said not to worry because the thunder was just God unloading potatoes out of his dump truck. And the lightning? He's gotta back up you know... We went inside, had a bit of rain but nothing else happened. Or so I thought. Turns out our neighbor had gone back outside and scattered potatoes all over her yard and ours leaving me to find all of them the next morning when I went out to play. I believed that stuff until 8th grade."""
    
    print("🔍 Testing split_body_per_screen function")
    print("=" * 60)
    
    print(f"📊 Constants:")
    print(f"   TEXT_CHAR_WRAP: {TEXT_CHAR_WRAP}")
    print(f"   LINES_PER_SCREEN: {LINES_PER_SCREEN}")
    print()
    
    print(f"📝 Original text length: {len(sample_text)} characters")
    print(f"📝 Original text preview: {sample_text[:100]}...")
    print()
    
    # Test with RedditCrawler
    crawler = RedditCrawler()
    screens = crawler.split_body_per_screen(sample_text)
    
    print(f"✨ Result: Split into {len(screens)} screen(s)")
    print("=" * 60)
    
    for i, screen in enumerate(screens):
        print(f"📺 Screen {i+1}:")
        print(f"   Length: {len(screen)} characters")
        print(f"   Lines: {len(screen.split())} words")
        print(f"   Content: {screen[:200]}{'...' if len(screen) > 200 else ''}")
        print()
    
    # Test text wrapping step by step
    print("🔧 Step-by-step breakdown:")
    print("=" * 60)
    
    wrap = StringManipulator()
    wrapped_lines = wrap.wrap_in_lines([sample_text], TEXT_CHAR_WRAP)
    
    print(f"📏 After text wrapping (max {TEXT_CHAR_WRAP} chars per line):")
    print(f"   Total lines: {len(wrapped_lines)}")
    
    for i, line in enumerate(wrapped_lines[:5]):  # Show first 5 lines
        print(f"   Line {i+1}: '{line}' ({len(line)} chars)")
    
    if len(wrapped_lines) > 5:
        print(f"   ... and {len(wrapped_lines) - 5} more lines")
    
    print()
    print(f"📺 Grouping into screens ({LINES_PER_SCREEN} lines per screen):")
    
    n = len(wrapped_lines)
    if n <= LINES_PER_SCREEN:
        print(f"   All {n} lines fit in 1 screen")
    else:
        screens_needed = (n + LINES_PER_SCREEN - 1) // LINES_PER_SCREEN
        print(f"   {n} lines need {screens_needed} screens")
        
        for screen_num in range(screens_needed):
            start_line = screen_num * LINES_PER_SCREEN
            end_line = min(start_line + LINES_PER_SCREEN, n)
            print(f"   Screen {screen_num + 1}: Lines {start_line + 1}-{end_line}")

def test_with_real_post():
    """Test with a real Reddit post."""
    print("\n" + "=" * 80)
    print("🌐 Testing with real Reddit post")
    print("=" * 80)
    
    try:
        praw_crawler = PrawRedditCrawler()
        post = praw_crawler.get_random_post("confessions")
        
        if 'error' in post:
            print(f"❌ Error getting post: {post['error']}")
            return
            
        print(f"📄 Post title: {post['title'][:60]}...")
        print(f"📏 Original body length: {len(post['body'][0] if isinstance(post['body'], list) else post['body'])} characters")
        
        # The body is already split, let's check the result
        if isinstance(post['body'], list):
            print(f"✨ Post split into {len(post['body'])} screen(s):")
            
            for i, screen in enumerate(post['body']):
                print(f"📺 Screen {i+1}:")
                print(f"   Length: {len(screen)} characters")
                print(f"   Preview: {screen[:150]}{'...' if len(screen) > 150 else ''}")
                print()
        else:
            print("⚠️  Body was not split into screens")
            
    except Exception as e:
        print(f"❌ Error testing with real post: {e}")

if __name__ == "__main__":
    test_split_body_per_screen()
    test_with_real_post()
