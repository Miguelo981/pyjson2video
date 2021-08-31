import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)

AUDIO_EXPORTS_PATH = os.path.join(BASE_DIR, r"project/audio/exports")
VIDEO_EXPORTS_PATH = os.path.join(BASE_DIR, r"project/video/exports")
INPUTS_PATH = os.path.join(BASE_DIR, 'inputs')
#IMAGEMAGICK_BINARY = os.getenv ('IMAGEMAGICK_BINARY', 'C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe')

FFMPEG_BINARY = 'ffmpeg-imageio'
#~ IMAGEMAGICK_BINARY = 'auto-detect'
IMAGEMAGICK_BINARY = r"C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick.exe"