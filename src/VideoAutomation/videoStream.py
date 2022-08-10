import sys
sys.path.append("..")

import cv2
from src.VideoAutomation.VideoConstants import *
from src.VideoAutomation.photoFrameUtils import *
from src.VideoAutomation.screenTextHandler import *
# from . import photoFrameUtils as pf
from . import videoUtils as vu
from src.AudioManager.AudioUtils import *
from src.AudioManager.AudioConstants import *


def get_title_dimensions(title, left_boundary_pos, right_boundary_pos):
    # array_size = 100
    # length = len(title)
    # if length > array_size // 2:
    #     array_size = length * 2 - 1
    # blocksize = (right_boundary_pos[0] - left_boundary_pos[0])//array_size
    title_size = DEFAULT_TITLE_SIZE
    if len(title) > 20:
        div = len(title)/20
        title_size = int(title_size//div)
    start_pos_x = left_boundary_pos[0] + 80
    start_pos_y = left_boundary_pos[1] + (right_boundary_pos[1] - left_boundary_pos[1])//2
    return [(start_pos_x, start_pos_y), title_size]



def render_video(cap, out, rdata, screen_time_map):
    print("Rendering Video")
    if cap == None or out == None or rdata == None or screen_time_map == None:
        print("Something is None in render Video")
        return
    screen_time_map_keys = list(screen_time_map.keys())
    time_per_screen = list(screen_time_map.values())
    detail_per_second = time_per_screen[0] * FRAME_RATE

    keyCount = 0
    frameCount = 0.0
    video_time = int(get_audio_duration(MAIN_AUDIO))
    current_screen_type = screen_time_map_keys[keyCount].split('_')[0]
    current_screen_type_count = '0'
    print(video_time)
    screenft = cv2.freetype.createFreeType2()
    screenft.loadFontData(fontFileName=FONT_RALEWAY_MED, id=0)
    print(rdata)
    while True:
        ret, frame = cap.read()

        # cv2.rectangle(frame, (100, 100), (1820, 980), (48, 48, 48), -1)
        frame = put_rectangle_on_img(frame, MAIN_RECT_TOP_LEFT, MAIN_RECT_TOP_RIGHT, MAIN_RECT_COLOR, MAIN_RECT_OPACITY)
        frame = put_boundary_in_rectangle(frame, MAIN_RECT_TOP_LEFT, MAIN_RECT_TOP_RIGHT, BOUNDARY_COLOR)
        if current_screen_type.lower() == "title":
            screen_text = rdata['title']
            title_position, title_size = get_title_dimensions(screen_text, MAIN_RECT_TOP_LEFT, MAIN_RECT_TOP_RIGHT)
            screenft.putText(frame, screen_text, title_position, title_size, DEFAULT_TITLE_COLOR, -1, cv2.LINE_AA, True)

        if current_screen_type.lower() == "body":
            screen_text = rdata['body'][current_screen_type_count]
            frame = set_screen_text(frame, screenft, screen_text)
            # screenft.putText(frame, screen_text, (800//2, 600), 50, (200, 200, 200), -1, cv2.LINE_AA, True)


        if keyCount < len(screen_time_map_keys) and frameCount > detail_per_second:
            keyCount += 1
            current_screen_type = screen_time_map_keys[keyCount].split('_')[0]
            current_screen_type_count = int(screen_time_map_keys[keyCount].split('_')[1].replace('.mp3', ''))
            frameCount = 0.0
            detail_per_second = time_per_screen[keyCount] * FRAME_RATE
            print(current_screen_type, current_screen_type_count)
        frameCount += 1.0

        # write to video
        out.write(frame)
        cv2.imshow('frame', frame)

        # stop and conclude the video
        # print(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if cap.get(cv2.CAP_PROP_POS_FRAMES) + 1 >= FRAME_RATE * video_time or cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def create_video(screen_time_map, rdata):
    cap_backgroud = cv2.VideoCapture(BG_VIDEO)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_filename = VIDEO_LOCATION_RENDERED + 'test1' + OUTPUT_VIDEO_FORMAT
    out = cv2.VideoWriter(output_filename, fourcc, FRAME_RATE, OUTPUT_VIDEO_DIMENSIONS)
    render_video(cap_backgroud, out, rdata, screen_time_map)
    output_filename_music = vu.add_audio_to_video(output_filename)

def main_video_operator(screen_time_map, rdata):
    # screen_time_map, QuestionList = audio_controller()

    print(screen_time_map)
    create_video(screen_time_map, rdata)
