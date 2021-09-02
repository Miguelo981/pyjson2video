import random

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pydub import AudioSegment


def convert_audio_mp3_file(media_file, format="wav"):
    sound = AudioSegment.from_mp3(media_file)
    sound.export(media_file.replace('.mp3', '.'+format), format=format)

def get_song(songs, total_duration):
    random.shuffle(songs)

    for song in songs:
        song_duration = AudioFileClip(song['route']).duration

        if song_duration >= total_duration:
            return song

        # TODO join more than one music if not found