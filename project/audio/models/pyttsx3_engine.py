import platform, pyttsx3

from loguru import logger
from project.audio.models.audio_engine import VoiceEngine


class Pyttsz3Engine(VoiceEngine):
    def __init__(self, rate=140, lang="en", gender="male"):
        VoiceEngine.__init__(self, rate, lang, gender)
        self.engine = None
        self.voice = None

        self.__set_properties()

    def __set_properties(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", self.rate)

        for voice in self.engine.getProperty('voices'):
            if platform.system() == 'Linux':
                language = voice.languages[0].decode("utf-8")
                gender = None # TODO find this in linux

            elif platform.system() == 'Windows':
                language = voice.id.split('TTS_MS_')[1].split('_')[0]
                gender = voice.gender
                #TODO get the way to get OS voice interpeters gender

            elif platform.system() == 'Darwin':
                pass

            if (language is not None and self.lang in language.lower()): # and (gender is not None and self.gender in gender.lower())
                self.voice = voice
                logger.info("Selected audio language found!")
                break

        if self.voice is None:
            logger.warning("Selected audio language is not installed in the OS!")
            self.voice = self.engine.getProperty('voices')[0]

        self.engine.setProperty("voice", self.voice.id)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def save(self, text, route):
            self.engine.save_to_file(text, route)
            self.engine.runAndWait()