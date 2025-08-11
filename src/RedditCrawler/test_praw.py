#!/usr/bin/env python3

import sys
sys.path.append(".")

from src.RedditCrawler.RedditApi import PrawRedditCrawler

def test_praw_connection():
    """Test the PRAW Reddit crawler."""
    try:
        print("Initializing PrawRedditCrawler...")
        praw_crawler = PrawRedditCrawler()
        
        print("Testing connection...")
        if praw_crawler.test_connection():
            print("✅ Connection successful!")
            
            print("\n🔍 Testing random post fetch...")
            random_post = praw_crawler.get_random_post("confessions")
            if 'error' not in random_post:
                print(f"✅ Random post: {random_post.get('title', 'No title')[:50]}...")
                print(f"   Body preview: {random_post.get('body', [''])[0][:100] if random_post.get('body') else 'No body'}...")
            else:
                print(f"❌ Error getting random post: {random_post['error']}")
                
            print("\n🔥 Testing hot post fetch...")
            hot_post = praw_crawler.get_hot_post("confessions", limit=5)
            if 'error' not in hot_post:
                print(f"✅ Hot post: {hot_post.get('title', 'No title')[:50]}...")
            else:
                print(f"❌ Error getting hot post: {hot_post['error']}")
                
        else:
            print("❌ Connection failed. Check your credentials.")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_praw_connection()
