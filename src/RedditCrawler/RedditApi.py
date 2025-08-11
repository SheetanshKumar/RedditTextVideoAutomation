# import Oauth
# from . import *
import sys
sys.path.append("..")

import requests
import praw
import random
import time
from src.RedditCrawler.Oauth import *
from src.VideoAutomation.screenTextHandler import *
from src.VideoAutomation.VideoConstants import *

URL = "https://oauth.reddit.com"
HOT_API = "/r/python/hot"
RANDOM_API = "/r/confessions/random"

# print(res.json()[0]['data']['children'][0]['data']['selftext'])
# print(res.json()[0]['data']['children'][0]['data']['url'])
# df = pd.DataFrame()

# for post in res.json()['data']['children']:
#     # df = df.append({
#     #     'subreddit': post['data']['subreddit'],
#     #     'title': post['data']['title'],
#     #     'selftext': post['data']['selftext'],
#     #     'upvote_ratio': post['data']['upvote_ratio'],
#     #     'ups': post['data']['ups'],
#     #     'downs': post['data']['downs'],
#     #     'score': post['data']['score']
#     # }, ignore_index=True)
#     print(post['data']['permalink'])
#     print(post['data']['selftext'])
#
# # print(df.values)


class RedditCrawler:

    def __init__(self):
        self.auth = Oauth()
        self.headers = self.auth.get_headers_after_auth()
        self.retry_count = 4

    def _get_request(self, apiUrl):
        try:
            res = requests.get(apiUrl, headers=self.headers)
        except Exception as e:
            print(e)
            self.headers = self.auth.get_headers_after_auth()
        if res.status_code == 200:
            return res.json(), True
        print(res.json())
        return "Status not 200", False

    def _get_next_post(self, retry):
        res, status = self._get_request(apiUrl=URL+RANDOM_API)
        if not status:
            return {"error": res}, status
        newresult = dict()
        retry_flag = (False, "")
        try:
            newresult["title"] = res[0]['data']['children'][0]['data']['title']
            newresult["body"] = res[0]['data']['children'][0]['data']['selftext']
            newresult["url"] = res[0]['data']['children'][0]['data']['url']
        except Exception as e:
            print("Can't parse this post, exception: {}, retrying {} time".format(e, retry))
            if retry <= 4:
                return self._get_next_post(retry+1)
            retry_flag = (True, e)
        if retry_flag[0]:
            return {"error": "Can't parse, exception :{}, Retry limit exceeded".format(retry_flag[1])}, False

        return newresult, True

    def split_body_per_screen(self, body):
        wrap = StringManipulator()
        body = wrap.wrap_in_lines([body], vc.TEXT_CHAR_WRAP)
        linesperscreen = LINES_PER_SCREEN
        # body = body.replace('\n', '')
        # body = body.split('.')
        # linesperscreen = 5
        n = len(body)
        if n <= linesperscreen:
            return [' '.join(body)]
        i = 0
        j = linesperscreen
        res = []
        while (i < len(body)):
            res.append(' '.join(body[i:j]))
            i = j
            j += linesperscreen

        return res

    def get_random_post(self):
        post, ok = self._get_next_post(0)
        if not ok:
            print(post['error'])
        post['body'] = self.split_body_per_screen(post['body'])
        return post

    def get_static_post(self):
        post = {'title': 'And the thunder rolls?', 'body': "I was 3 years old and living in a trailer in Kansas.  Tornado Alley seems to have shifted east and a bit more south in the years since I was a toddler but tornados were a serious seasonal  threat of which even at a young age I was very aware of.  I remember standing on the steps of our trailer watching them far off in the distance.  Scared the crap out of me.\n\nOne evening I was outside with my mom and our next door neighbor.  A thunderstorm was blowing in and I was upset and worried.  My mom and neighbor said not to worry because the thunder was just God unloading potatoes out of his dump truck.  And the lightning?  He's gotta back up you know...\n\nWe went inside, had a bit of rain but nothing else happened. Or so I thought.\n\nTurns out our neighbor had gone back outside and scattered potatoes all over her yard and ours leaving me to find all of them the next morning when I went out to play.\n\nI believed that stuff until 8th grade.", 'url': 'https://www.reddit.com/r/funnystories/comments/vlo304/and_the_thunder_rolls/'}
        post['body'] = self.split_body_per_screen(post['body'])
        return post


class PrawRedditCrawler:
    """Reddit crawler using PRAW (Python Reddit API Wrapper) for better reliability and features."""
    
    def __init__(self, client_id=None, client_secret=None, user_agent=None):
        """
        Initialize PRAW Reddit instance.
        If credentials not provided, they will be loaded from environment variables via Oauth class.
        """
        self.oauth = Oauth()
        auth_details = self.oauth.get_auth_details()
        
        self.client_id = client_id or auth_details['client_id']
        self.client_secret = client_secret or auth_details['client_secret']
        self.user_agent = user_agent or "RedditVideoBot/1.0 by YourUsername"
        self.retry_count = 4
        self.retry_delay = 2  # seconds between retries
        
        # Validate credentials
        if not self.client_id or not self.client_secret:
            raise ValueError("Reddit API credentials not found. Please check your environment variables or provide them directly.")
        
        try:
            # Initialize Reddit instance
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret, 
                user_agent=self.user_agent
            )
            
            # Set to read-only mode
            self.reddit.read_only = True
            
            # Test the connection
            print(f"Connected to Reddit API as read-only user. Rate limit remaining: {self.reddit.auth.limits}")
            
        except Exception as e:
            print(f"Failed to initialize Reddit connection: {e}")
            raise
    
    def _fetch_post_with_retry(self, fetch_function, retry=0):
        """
        Generic retry mechanism for fetching posts.
        Takes a function that returns a post and retries on failure.
        """
        retry_flag = (False, "")
        
        try:
            post = fetch_function()
            if post is None:
                raise Exception("No post returned from fetch function")
            
            # Parse post data
            parsed_post = self._parse_post(post)
            return parsed_post, True
            
        except praw.exceptions.RedditAPIException as e:
            print(f"Reddit API exception: {e}, retry attempt: {retry}")
            if retry < self.retry_count:
                time.sleep(self.retry_delay)
                return self._fetch_post_with_retry(fetch_function, retry + 1)
            retry_flag = (True, f"Reddit API exception: {e}")
            
        except praw.exceptions.PRAWException as e:
            print(f"PRAW exception: {e}, retry attempt: {retry}")
            if retry < self.retry_count:
                time.sleep(self.retry_delay)
                return self._fetch_post_with_retry(fetch_function, retry + 1)
            retry_flag = (True, f"PRAW exception: {e}")
            
        except Exception as e:
            print(f"Error fetching post, exception: {e}, retry attempt: {retry}")
            if retry < self.retry_count:
                time.sleep(self.retry_delay)
                return self._fetch_post_with_retry(fetch_function, retry + 1)
            retry_flag = (True, e)
            
        if retry_flag[0]:
            return {"error": f"Failed to fetch post, exception: {retry_flag[1]}, retry limit exceeded"}, False
    
    def _parse_post(self, post):
        """Parse a PRAW post object into our standard format."""
        try:
            parsed_post = {
                "title": post.title,
                "body": post.selftext,
                "url": f"https://www.reddit.com{post.permalink}",
                "score": post.score,
                "author": str(post.author),
                "subreddit": str(post.subreddit),
                "created_utc": post.created_utc
            }
            return parsed_post
        except Exception as e:
            raise Exception(f"Error parsing post: {e}")
    
    def get_hot_post(self, subreddit_name="confessions", limit=10):
        """
        Fetch a random post from hot posts of the given subreddit.
        """
        def fetch_hot():
            subreddit = self.reddit.subreddit(subreddit_name)
            hot_posts = list(subreddit.hot(limit=limit))
            if not hot_posts:
                raise Exception(f"No hot posts found in r/{subreddit_name}")
            
            # Filter for text posts only
            text_posts = [post for post in hot_posts if post.selftext and len(post.selftext.strip()) > 50]
            if not text_posts:
                raise Exception(f"No suitable text posts found in hot posts from r/{subreddit_name}")
            
            return random.choice(text_posts)
        
        post, success = self._fetch_post_with_retry(fetch_hot)

        if success:
            post['body'] = self.split_body_per_screen(post['body'])
        return post
    
    def get_random_post(self, subreddit_name="confessions"):
        """
        Fetch a random post from the given subreddit.
        """
        def fetch_random():
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Try to get a random post first
            try:
                random_post = subreddit.random()
                if random_post and random_post.selftext and len(random_post.selftext.strip()) > 50:
                    return random_post
            except Exception as e:
                print(f"Random post method failed: {e}")
            
            # Fallback: get from new posts if random is not available
            print(f"Random post not available for r/{subreddit_name}, using fallback method...")
            new_posts = list(subreddit.new(limit=100))
            if not new_posts:
                raise Exception(f"No posts found in r/{subreddit_name}")
            
            # Filter for text posts with sufficient content
            text_posts = [post for post in new_posts if post.selftext and len(post.selftext.strip()) > 50]
            if not text_posts:
                raise Exception(f"No suitable text posts found in r/{subreddit_name}")
                
            return random.choice(text_posts)
        
        post, success = self._fetch_post_with_retry(fetch_random)
        if success:
            post['body'] = self.split_body_per_screen(post['body'])
        return post
    
    def get_top_post(self, subreddit_name="confessions", time_filter="week", limit=50):
        """
        Fetch a random post from top posts of the given subreddit and time period.
        """
        def fetch_top():
            subreddit = self.reddit.subreddit(subreddit_name)
            top_posts = list(subreddit.top(time_filter=time_filter, limit=limit))
            if not top_posts:
                raise Exception(f"No top posts found in r/{subreddit_name} for {time_filter}")
            
            # Filter for text posts only
            text_posts = [post for post in top_posts if post.selftext and len(post.selftext.strip()) > 50]
            if not text_posts:
                raise Exception(f"No suitable text posts found in top posts from r/{subreddit_name}")
            
            return random.choice(text_posts)
        
        post, success = self._fetch_post_with_retry(fetch_top)
        if success:
            post['body'] = self.split_body_per_screen(post['body'])
        return post
    
    def split_body_per_screen(self, body):
        """Split body text into screen-sized chunks (reusing existing logic)."""
        wrap = StringManipulator()
        body = wrap.wrap_in_lines([body], vc.TEXT_CHAR_WRAP)
        linesperscreen = LINES_PER_SCREEN

        
        n = len(body)
        if n <= linesperscreen:
            return [' '.join(body)]
        
        i = 0
        j = linesperscreen
        res = []
        while i < len(body):
            res.append(' '.join(body[i:j]))
            i = j
            j += linesperscreen
        return res


    def test_connection(self):
        """Test the Reddit API connection and print diagnostic information."""
        try:
            print("Testing Reddit API connection...")
            print(f"User agent: {self.user_agent}")
            print(f"Client ID: {self.client_id[:8]}..." if self.client_id else "No client ID")
            
            # Try to access a simple subreddit
            test_subreddit = self.reddit.subreddit("test")
            print(f"Successfully connected to r/test")
            print(f"Subreddit display name: {test_subreddit.display_name}")
            print(f"Rate limit remaining: {self.reddit.auth.limits}")
            
            # Try to get one post
            try:
                posts = list(test_subreddit.hot(limit=1))
                if posts:
                    print(f"Successfully fetched a test post: {posts[0].title[:50]}...")
                    return True
                else:
                    print("No posts found in test subreddit")
                    return False
            except Exception as post_error:
                print(f"Error fetching posts: {post_error}")
                return False
                
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


# redditobj = RedditCrawler()
# print(redditobj.get_random_post())

# Example usage of PrawRedditCrawler:
# praw_crawler = PrawRedditCrawler()
# 
# # Test the connection first
# if praw_crawler.test_connection():
#     print("Connection successful!")
#     
#     # Get a random post from r/confessions
#     random_post = praw_crawler.get_random_post("confessions")
#     print("Random post:", random_post)
#
#     # Get a hot post from r/tifu  
#     hot_post = praw_crawler.get_hot_post("tifu")
#     print("Hot post:", hot_post)
#
#     # Get a top post from this week
#     top_post = praw_crawler.get_top_post("AskReddit", time_filter="week")
#     print("Top post:", top_post)
# else:
#     print("Connection failed. Check your credentials and network connection.")