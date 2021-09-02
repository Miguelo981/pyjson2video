import os, platform

from loguru import logger
from moviepy.config import change_settings

logger.add("logs/logs.log", backtrace=True, diagnose=True)

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)

AUDIO_EXPORTS_PATH = os.path.join(BASE_DIR, r"project/audio/exports")
VIDEO_EXPORTS_PATH = os.path.join(BASE_DIR, r"project/video/exports")
IMAGE_EXPORTS_PATH = os.path.join(BASE_DIR, r"project/image/exports")
ASSETS_PATH = os.path.join(BASE_DIR, r"assets")
INPUTS_PATH = os.path.join(BASE_DIR, 'inputs')
OUTPUTS_PATH = os.path.join(BASE_DIR, 'outputs')

""" 
    Path to your ImageMagick binary converter file in case you are using Windows
"""
if platform.system() == 'Windows':
    change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/convert.exe"})