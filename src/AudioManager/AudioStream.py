from . import AssistantUtils as asu
from . import AudioUtils as adu
from . import AudioConstants as ac

screenCount = 0
MP3 = '.mp3'


def attach_blank(screen_time_map, key, time):
    screenkey = key + '_blank_'+str(time) + '.mp3'
    screen_time_map[screenkey] = [adu.get_audio_duration(ac.AUDIO_LOCATION_BLANK + 'blank_' + str(time) + '.mp3'), ac.AUDIO_LOCATION_BLANK + 'blank_' + str(time) + '.mp3']
    return screen_time_map


def get_intro_static_audio(screen_time_map):
    global screenCount
    screenCount += 1
    screenkey = ac.SCREEN + str(screenCount) + MP3
    screen_time_map[screenkey] = [adu.get_audio_duration(ac.AUDIO_LOCATION_STATIC_GENDER + screenkey), ac.AUDIO_LOCATION_STATIC_GENDER + screenkey]

    screenCount += 1
    screenkey = ac.SCREEN + str(screenCount) + MP3
    screen_time_map[screenkey] = [adu.get_audio_duration(ac.AUDIO_LOCATION_STATIC_GENDER + screenkey), ac.AUDIO_LOCATION_STATIC_GENDER + screenkey]

    return screen_time_map


def get_list_audio_concat(screen_time_map):
    audio_location_list = []
    for key in screen_time_map.keys():
        audio_location_list.append(ac.AUDIO_LOCATION_DYNAMIC_NORMAL+key)
    return audio_location_list


def remove_location_screen_time_map(screen_time_map):
    for key in list(screen_time_map.keys()):
        screen_time_map[key] = screen_time_map[key][0]
    return screen_time_map



def create_audio_map(rdata):
    screen_time_map = dict()

    # screen_time_map = get_intro_static_audio(screen_time_map)

    title = rdata['title']
    body = rdata['body']

    titlekey = 'TITLE_0' + '.mp3'
    for i in body:
        print(i)
    asu.assistant_speaks(title, ac.AUDIO_LOCATION_DYNAMIC_NORMAL + titlekey)
    screen_time_map[titlekey] = adu.get_audio_duration(ac.AUDIO_LOCATION_DYNAMIC_NORMAL + titlekey)

    for i, line in enumerate(body):
        key = 'BODY_{}.mp3'.format(i)
        asu.assistant_speaks(line, ac.AUDIO_LOCATION_DYNAMIC_NORMAL + key)
        screen_time_map[key] = adu.get_audio_duration(ac.AUDIO_LOCATION_DYNAMIC_NORMAL + key)
    return screen_time_map



def audio_controller(rdata):

    screen_time_map = create_audio_map(rdata)
    # screen_time_map = {'TITLE_0.mp3': 1.704, 'BODY_0.mp3': 31.128, 'BODY_1.mp3': 16.056, 'BODY_2.mp3': 21.696}
    print(screen_time_map)
    audio_location_list = get_list_audio_concat(screen_time_map)
    [print(i) for i in audio_location_list]
    adu.concat_audios(audio_location_list, ac.AUDIO_LOCATION_DYNAMIC_NORMAL + ac.MAIN_AUDIO_WITHOUT_MUSIC)
    # screen_time_map = remove_location_screen_time_map(screen_time_map)
    return screen_time_map

#
# def set_static_commands():
#     assistant_speaks(screen_1, AUDIO_LOCATION_STATIC_FEMALE+'screen_1.mp3')
#     assistant_speaks(screen_2, AUDIO_LOCATION_STATIC_FEMALE + 'screen_2.mp3')
#     assistant_speaks("ding dong!", AUDIO_LOCATION_STATIC_FEMALE + 'bell.mp3')
#     for i in range(1, 51):
#         create_blank_audio(AUDIO_LOCATION_BLANK, i)


# if __name__ == '__main__':
#     # rdata = redditApi.RedditCrawler()
#     # rdata = rdata.get_static_post()
#     rdata = {'title': 'And the thunder rolls?', 'body': "I was 3 years old and living in a trailer in Kansas.  Tornado Alley seems to have shifted east and a bit more south in the years since I was a toddler but tornados were a serious seasonal  threat of which even at a young age I was very aware of.  I remember standing on the steps of our trailer watching them far off in the distance.  Scared the crap out of me.\n\nOne evening I was outside with my mom and our next door neighbor.  A thunderstorm was blowing in and I was upset and worried.  My mom and neighbor said not to worry because the thunder was just God unloading potatoes out of his dump truck.  And the lightning?  He's gotta back up you know...\n\nWe went inside, had a bit of rain but nothing else happened. Or so I thought.\n\nTurns out our neighbor had gone back outside and scattered potatoes all over her yard and ours leaving me to find all of them the next morning when I went out to play.\n\nI believed that stuff until 8th grade.", 'url': 'https://www.reddit.com/r/funnystories/comments/vlo304/and_the_thunder_rolls/'}
#     rdata['body'] = split_body_per_screen(rdata['body'])
#     screen_time_map = audio_controller(rdata)
#     print(screen_time_map)