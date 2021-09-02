import json, os.path

from PIL import Image
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ColorClip, TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from project.audio.editor.audio_editor import convert_audio_mp3_file, get_song
from conf import *
from moviepy.video.fx.resize import resize

from project.audio.models.voice_engine import VoiceEngine
from project.image.image_editor import prepare_image, zoom_in_effect, resize_zoomin_func


def convert_song_files():
    with open(os.path.join(INPUTS_PATH, "example.json"), encoding="utf8") as file:
        try:
            data = json.load(file)

            for song in data['songs']:
                if '.mp3' in song['route'].lower():
                    convert_audio_mp3_file(song['route'], format=data['audio_format'])

                    filename, file_extension = os.path.splitext(song['route'])
                    song['route'] = song['route'].replace(file_extension, '.' + data['audio_format'])

            with open(os.path.join(OUTPUTS_PATH, 'example.json'), 'w') as outfile:
                json.dump(data, outfile, indent=4)
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
                data['phrases'][i]['audio']['volume'] = 0
                logger.info("Audio: " + audio_path + " created!")

            with open(os.path.join(OUTPUTS_PATH, 'example.json'), 'w') as outfile:
                json.dump(data, outfile, indent=4)
                outfile.close()

            logger.info("Structured file updated!")
            file.close()
        except Exception as error:
            logger.error(error)

def create_complete_video():
    with open(os.path.join(OUTPUTS_PATH, "example.json"), encoding="utf8") as file:
        try:
            data = json.load(file)
            final_video_route = os.path.join(VIDEO_EXPORTS_PATH, data['title'] + '.mp4')

            clip_time = 0
            video = ColorClip(color=(255, 255, 255), size=(data['dimensions']['width'], 1080))\
                .set_duration(0)\
                .set_fps(30)
            rest_clip = ColorClip(color=(255, 255, 255), size=(data['dimensions']['width'], data['dimensions']['height']))\
                .set_duration(0.5)

            for audio in data['phrases']:
                clip_audio = AudioFileClip(os.path.join(AUDIO_EXPORTS_PATH, audio['audio']['route']))
                audio_duration = clip_audio.duration #(audio['audio']['duration'] / 1000)

                #clip = background_clip.subclip(clip_time, clip_time + audio_duration)
                clip = ColorClip(color=(255, 255, 255), size=(data['dimensions']['width'], data['dimensions']['height']))\
                    .set_duration(audio_duration)

                if 'images' in audio:
                    for img in audio['images']:
                        img_clip = ImageClip(prepare_image(Image.open(os.path.join(ASSETS_PATH, img['route']))))\
                            .set_duration(img['duration'] / 1000)
                        img_clip = resize(img_clip, width=(img['size']['width']))
                        img_clip = resize_zoomin_func(img_clip)
                        #img_clip = zoom_in_effect(img_clip, 0.04)
                        img_clip = img_clip.set_pos('center')
                        clip = CompositeVideoClip([clip, img_clip])

                if data['subtitles']:
                    #Dela-Gothic-One-Regular
                    txt_clip = TextClip(audio['text'], font=audio['font'], fontsize=60, color='white', align='center', size=(data['dimensions']['width'], 150), stroke_color='black', stroke_width=5)
                    txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(audio_duration)
                    clip = CompositeVideoClip([clip, txt_clip])

                clip = clip.set_audio(clip_audio)
                video = concatenate_videoclips([video, clip, rest_clip])

                clip_time += audio_duration

            # background_audio_clip = AudioFileClip(os.path.join(AUDIO_EXPORTS_PATH, data['title'] + '_complete_audio.' + data['audio_format']))
            # video = video.set_audio(background_audio_clip)

            video.write_videofile(final_video_route, codec='libx264', audio_codec="aac")
            logger.info("Final video created! " + final_video_route)
            file.close()
        except Exception as error:
            logger.error(error)

convert_song_files()
create_audio_files()
create_complete_video()

# import moviepy.editor as mpe
#
# video = ColorClip(color=(255, 255, 255), size=(1920, 1080))\
#                 .set_duration(15)\
#                 .set_fps(30)\
#                 .set_audio(None)
# vtuber_clip = VideoFileClip(os.path.join(ASSETS_PATH, 'videos/test1.mp4'))
# masked_clip = vtuber_clip.fx(mpe.vfx.mask_color, color=[0,214,11], thr=100, s=5)\
#     .set_pos(('right', 'bottom'))\
#     .fx(mpe.vfx.loop, n=3)\
#     .fx(mpe.vfx.speedx, 4)\
#     .set_duration(13)
# final_clip = CompositeVideoClip([
#     video,
#     masked_clip
# ]).set_duration(vtuber_clip.duration)
# final_clip.write_videofile('test1.mp4')