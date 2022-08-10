# import Oauth
# from . import *
import sys
sys.path.append("..")

import requests
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
        # print(res.json())
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
# redditobj = RedditCrawler()
# print(redditobj.get_random_post())