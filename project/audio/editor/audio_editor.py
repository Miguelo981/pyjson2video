import random

from pydub import AudioSegment

from project.audio.audio_controller import get_audio_duration


def convert_audio_mp3_file(media_file, format="wav"):
    sound = AudioSegment.from_mp3(media_file)
    sound.export(media_file.replace('.mp3', '.'+format), format=format)

def get_song(songs, total_duration):
    random.shuffle(songs)

    for song in songs:
        song_duration = get_audio_duration(song['route'])

        if song_duration >= total_duration:
            return song

        # TODO join more than one music if not found