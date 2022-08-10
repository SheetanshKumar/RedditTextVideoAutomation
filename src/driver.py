# from src.AudioManager import AudioStream
# from src.VideoAutomation import videoStream
from RedditCrawler import RedditApi
from AudioManager import AudioStream
import AudioManager.AudioUtils
# from AudioUtils import get_audio_duration
from VideoAutomation import videoStream

rdata = RedditApi.RedditCrawler()
rdata = rdata.get_static_post()
# rdata = rdata.get_random_post()
# screen_time_map = AudioStream.audio_controller(rdata)

#
# print(screen_time_map)
screen_time_map = {'TITLE_0.mp3': 1.704, 'BODY_0.mp3': 31.128, 'BODY_1.mp3': 16.056, 'BODY_2.mp3': 21.696}
videoStream.main_video_operator(screen_time_map, rdata)
