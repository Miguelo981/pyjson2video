import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLE_DIR = os.path.join(DATA_DIR, "samples")
SAMPLE_INPUTS = os.path.join(SAMPLE_DIR, "inputs")
SAMPLE_OUTPUTS = os.path.join(SAMPLE_DIR, 'outputs')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.dirname(os.path.abspath(__file__) + "\exports")
#IMAGEMAGICK_BINARY = os.getenv ('IMAGEMAGICK_BINARY', 'C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe')

FFMPEG_BINARY = 'ffmpeg-imageio'
#~ IMAGEMAGICK_BINARY = 'auto-detect'
IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick.exe"