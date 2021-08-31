import json, os

import pyttsx3
from loguru import logger
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

from project.audio.audio_controller import *
from project.audio.models.voice_engine import VoiceEngine
from project.audio.editor.audio_editor import convert_audio_mp3_file, get_song
from project.audio.utils import use_lang
from project.video.editor.image_editor import create_text_clip
from conf import *

logger.add("logs/logs.log", backtrace=True, diagnose=True)

# TODO and .format in for endswidth and check all paths exists

def convert_song_files():
    with open(os.path.join(INPUTS_PATH, "example.json"), encoding="utf8") as file:
        try:
            data = json.load(file)

            for song in data['songs']:
                if '.mp3' in song['route'].lower():
                    convert_audio_mp3_file(song['route'], format=data['audio_format'])

                    filename, file_extension = os.path.splitext(song['route'])
                    song['route'] = song['route'].replace(file_extension, '.' + data['audio_format'])

            with open('example.json', 'w') as outfile:
                json.dump(data, outfile)
                outfile.close()

            logger.info("Structured file updated!")
            file.close()
        except Exception as error:
            logger.error(error)

def create_audio_files():
    with open(os.path.join(INPUTS_PATH, "example.json"), encoding="utf8") as file:
        try:
            data = json.load(file)
            voice = VoiceEngine(rate=data['voice_speed'], lang=data['video_short_language'])

            for i in range(0, len(data['phrases'])):
                file_route = data['title'] + '_audio_' + str(i) + '.' + data['audio_format']

                audio_path = os.path.join(AUDIO_EXPORTS_PATH, file_route)
                voice.save(data['phrases'][i]['text'], audio_path)
                data['phrases'][i]['audio']['route'] = audio_path
                data['phrases'][i]['audio']['duration'] = get_audio_duration(audio_path)
                data['phrases'][i]['audio']['volume'] = 0
                logger.info("Audio: " + audio_path + " created!")

            with open('example.json', 'w') as outfile:
                json.dump(data, outfile)
                outfile.close()

            logger.info("Structured file updated!")
            file.close()
        except Exception as error:
            logger.error(error)

def create_complete_audio():
    with open(os.path.join("example.json"), encoding="utf8") as file:
        try:
            data = json.load(file)
            full_audio_duration = 0

            complete_audio = AudioSegment.empty()

            for audio in data['phrases']:
                complete_audio += import_media(audio['audio']['route'], format=data['audio_format'])
                full_audio_duration += audio['audio']['duration']

            searched_song = get_song(data['songs'], full_audio_duration)
            song = import_media(searched_song['route'], format=data['audio_format'])
            song = change_volume(song, searched_song['volume'])

            final_audio = overlay_media(complete_audio, song)
            final_audio_route = os.path.join(AUDIO_EXPORTS_PATH, data['title'] + '_complete_audio.' + data['audio_format'])
            export_media(final_audio, final_audio_route, format=data['audio_format'])

            logger.info("Final audio created!" + final_audio_route)
            file.close()
        except Exception as error:
            logger.error(error)

def create_complete_video():
    with open(os.path.join("example.json"), encoding="utf8") as file:
        # try:
            data = json.load(file)
            final_video_route = os.path.join(VIDEO_EXPORTS_PATH, data['title'] + '.mp4')

            background_clip = ColorClip(color=(255, 255, 255), size=(1280, 1920))
            background_clip = background_clip.set_fps(30)
            full_audio_duration = 0

            for audio in data['phrases']:
                full_audio_duration += audio['audio']['duration']
                # txt_clip = create_text_clip(audio['text'], 20)
                #
                # overlay_clip = CompositeVideoClip([background_clip, txt_clip], size=txt_clip.size)
                # overlay_clip = overlay_clip.set_duration(audio['audio']['duration'] / 1000)
                # overlay_clip = overlay_clip.set_fps(30)
                # overlay_clip = overlay_clip.set_audio(None)
                # background_clip = concatenate_videoclips([background_clip, overlay_clip])

            background_clip = background_clip.set_duration(full_audio_duration / 1000)
            background_audio_clip = AudioFileClip(os.path.join(AUDIO_EXPORTS_PATH, data['title'] + '_complete_audio.' + data['audio_format']))
            full_video = background_clip.set_audio(background_audio_clip)

            full_video.write_videofile(final_video_route, codec='libx264', audio_codec="aac")
            logger.info("Final video created! " + final_video_route)
            file.close()
        # except Exception as error:
        #     logger.error(error)


# convert_song_files()
# create_audio_files()
# create_complete_audio()
create_complete_video()