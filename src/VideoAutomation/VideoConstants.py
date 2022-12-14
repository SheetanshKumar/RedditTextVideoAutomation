# ------------------------ location ----------------------------------------
# PROJECT LOCATION
PROJECT_LOCATION = '/Users/sheetansh.kumar/PycharmProjects/RedditTextVideoAutomation/'

# MEDIA LOCATION

MEDIA_LOCATION = PROJECT_LOCATION + 'media/'


# video
VIDEO_LOCATION = MEDIA_LOCATION + 'video/'

# VIDEO_LOCATION_STOCK = VIDEO_LOCATION + 'stock/'
VIDEO_LOCATION_STATIC = VIDEO_LOCATION + 'static/'
VIDEO_LOCATION_RENDERED = MEDIA_LOCATION + 'rendered/'
# VIDEO_LOCATION_AVATARS = VIDEO_LOCATION + 'avatars/'

OUTPUT_VIDEO_FORMAT = '.mp4'
OUTPUT_VIDEO_DIMENSIONS = (1920, 1080)
FRAME_RATE = 25.0

#  video file locations

# AVATAR_VIDEO_GIRL = VIDEO_LOCATION_AVATARS + 'avatar_video_girl.mp4'
BLANK_WHITE_VIDEO = VIDEO_LOCATION_STATIC + 'blank_white_video.mp4'
BG_VIDEO = VIDEO_LOCATION_STATIC + 'gameplayvideo.mp4'
# AVATAR_VIDEO = AVATAR_VIDEO_GIRL

# photo location

PHOTO_LOCATION = MEDIA_LOCATION + 'photos/'


PHOTO_LOCATION_STATIC = PHOTO_LOCATION + 'static/'

# ------------------------ font ---------------------------------------------

FONT_LOCATION = MEDIA_LOCATION + 'fonts/'

FONT_UBUNTU = FONT_LOCATION + 'Ubuntu/'
FONT_UBUNTU_R = FONT_UBUNTU + 'Ubuntu-R.ttf'

FONT_RALEWAY = FONT_LOCATION + 'Raleway/'
FONT_RALEWAY_MED = FONT_RALEWAY + 'Raleway-Medium.ttf'

# # ------------------------ timer --------------------------------------------
#
# TIMER1_PHOTO = PHOTO_LOCATION_STATIC + 'timer1.png'
# TIMER2_PHOTO = PHOTO_LOCATION_STATIC + 'timer2.png'
#
# SIZE_HANDLER = 1
# TIMER_POS_X = 1500
# TIMER_POS_Y = 200
# TIMER_SIZE_X = 200 * SIZE_HANDLER
# TIMER_SIZE_Y = 200 * SIZE_HANDLER
# TIMER_TEXT_POSITION = (TIMER_POS_X + 70*SIZE_HANDLER, TIMER_POS_Y + 125*SIZE_HANDLER)
# TIMER_TEXT_SIZE = TIMER_SIZE_X//2
# TIMER_TEXT_COLOR = (0, 0, 255)

# # ------------------------ avatar -------------------------------------------
#
# AVATAR_LOCATION = PHOTO_LOCATION + 'avatars/'
#
# AVATAR_HEIGHT = 500
# AVATAR_WIDTH = 500
#
#
# AVATAR_POS_X = 300
# AVATAR_POS_Y = 300


# ------------------------ dimension ----------------------------------------



# DIMENSION_DICT = {"timer": (TIMER_POS_X, TIMER_POS_Y), "avatar": (AVATAR_POS_X, AVATAR_POS_Y)}
# THRES = 240
# MAXVAL = 255

# rectangle dimension

MAIN_RECT_TOP_LEFT = (100, 100)
MAIN_RECT_TOP_RIGHT = (1720, 880)
MAIN_RECT_OPACITY = 0.2
MAIN_RECT_COLOR = 50

BOUNDARY_RECT_TOP_LEFT = (120, 120)
BOUNDARY_TOP_RIGHT = (1800, 950)
BOUNDARY_OPACITY = 0.2
BOUNDARY_COLOR = (128, 128, 128)


# title

DEFAULT_TITLE_SIZE = 100
DEFAULT_TITLE_COLOR = (255, 255, 255)

# story lines TEXT

TEXT_POS_X = MAIN_RECT_TOP_LEFT[0] + 70
TEXT_POS_Y = MAIN_RECT_TOP_LEFT[1] + 100
TEXT_CHAR_WRAP = 60
TEXT_CHAR_SIZE = 50
TEXT_COLOR = (200, 200, 200)
TEXT_HORIZONTAL_SEPARATE = 70
LINES_PER_SCREEN = 10
