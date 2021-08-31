import json, os

from loguru import logger
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

from project.audio.audio_controller import *
from project.audio.models.voice_engine import VoiceEngine, EXPORT_DIR
from project.audio.editor.audio_editor import convert_audio_mp3_file, get_song
from project.video.editor.image_editor import create_text_clip
from conf import *

logger.add("logs.log", backtrace=True, diagnose=True)

# TODO use path joins to join paths and .format in for endswidth

def convert_song_files():
    with open(ROOT_DIR + r"\inputs\example.json", encoding="utf8") as file:
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
    with open(ROOT_DIR + r"\inputs\example.json", encoding="utf8") as file:
        try:
            data = json.load(file)
            voice = VoiceEngine(rate=data['voice_speed'], lang=data['audio_language'])

            for i in range(0, len(data['phrases'])):
                file_route = '\\' + data['title'] + '_audio_' + str(i) + '.' + data['audio_format']

                voice.save(data['phrases'][i]['text'], file_route)
                data['phrases'][i]['audio']['route'] = EXPORT_DIR + file_route
                data['phrases'][i]['audio']['duration'] = get_audio_duration(EXPORT_DIR + file_route)
                data['phrases'][i]['audio']['volume'] = 0
                logger.info("Audio: " + EXPORT_DIR + file_route + " created!")

            with open('example.json', 'w') as outfile:
                json.dump(data, outfile)
                outfile.close()

            logger.info("Structured file updated!")
            file.close()
        except Exception as error:
            logger.error(error)

def create_complete_audio():
    with open(ROOT_DIR + r"./example.json", encoding="utf8") as file:
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

            final_audio_route = EXPORT_DIR + '\\' + 'complete_audio.' + data['audio_format']

            export_media(final_audio, final_audio_route, format= data['audio_format'])

            logger.info("Final audio updated!", final_audio_route)
            file.close()
        except Exception as error:
            logger.error(error)

# TODO change routes to config and save there the default project configuration

def create_comlete_video():
    with open(ROOT_DIR + r"./example.json", encoding="utf8") as file:
        # try:
            data = json.load(file)
            final_video_route = EXPORT_DIR + '\\' + 'complete_video.mp4'

            background_clip = ColorClip(color='white', size=(1280, 1920))
            background_clip.set_fps(30)
            full_audio_duration = 0

            for audio in data['phrases']:
                full_audio_duration += audio['audio']['duration']
                txt_clip = create_text_clip(audio['text'], 20)

                overlay_clip = CompositeVideoClip([background_clip, txt_clip], size=txt_clip.size)
                overlay_clip = overlay_clip.set_duration(audio['audio']['duration'] / 1000)
                overlay_clip = overlay_clip.set_fps(30)
                overlay_clip = overlay_clip.set_audio(None)
                background_clip = concatenate_videoclips([background_clip, overlay_clip])

            #background_clip.set_duration(full_audio_duration)
            background_audio_clip = AudioFileClip(EXPORT_DIR + '\\' + 'complete_audio.' + data['audio_format'])
            music = background_audio_clip.subclip(0, full_audio_duration)
            full_video = background_clip.set_audio(music)

            full_video.write_videofile(final_video_route, codec='libx264', audio_codec="aac")
            logger.info("Final video updated!", final_video_route)
            file.close()
        # except Exception as error:
        #     logger.error(error)

#convert_song_files()
#create_audio_files()
#create_complete_audio()
create_comlete_video()