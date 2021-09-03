from gtts import gTTS

from project.audio.editor.audio_editor import convert_audio_mp3_file
from project.audio.models.audio_engine import VoiceEngine


class gTTSEngine(VoiceEngine):
    def __init__(self, rate=140, lang="en", gender="male"):
        VoiceEngine.__init__(self, rate, lang, gender)

    def save(self, text, route):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(route)
        convert_audio_mp3_file(route)