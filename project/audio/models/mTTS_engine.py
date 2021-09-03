from decouple import config
from loguru import logger

from project.audio.models.audio_engine import VoiceEngine
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

class MSSEngine(VoiceEngine):
    def __init__(self, rate=140, lang="en", gender="male"):
        VoiceEngine.__init__(self, rate, lang, gender)
        self.voice = None
        self.tts = None

        self.__set_properties()

    def __set_properties(self):
        self.tts = SpeechConfig(subscription=config('MSS_SECRET_KEY'), region=config('MSS_REGION'))
        synthesizer = SpeechSynthesizer(speech_config=self.tts)

        list = synthesizer.get_voices_async().get()

        for voice in list.voices:
            if self.lang in voice.locale and self.gender.lower() in voice.gender.name.lower():
                self.voice = voice
                self.tts.speech_synthesis_voice_name = self.voice.name
                logger.info("Selected audio language found!")
                break

        if self.voice is None:
            logger.warning("Selected audio language is not installed in the OS!")
            self.voice = voice

    def say(self, text):
        synthesizer = SpeechSynthesizer(speech_config=self.tts)
        synthesizer.speak_text_async(text).get()

    def save(self, text, route):
        synthesizer = SpeechSynthesizer(speech_config=self.tts, audio_config=AudioOutputConfig(filename=route))
        synthesizer.speak_text_async(text).get()