import pyttsx3

from loguru import logger
from routes import ROOT_DIR
from project.audio.utils import voice_driver_by_os

EXPORT_DIR = ROOT_DIR + r"\\project\audio\exports"

class VoiceEngine:
    def __init__(self, rate = 140, lang="en"):
        # self.engine = pyttsx3.init(voice_driver_by_os())
        self.engine = pyttsx3.init(voice_driver_by_os())
        self.voice = None
        self.rate = rate
        self.lang = lang

        self.__set_properties()

    def __set_properties(self):
        self.engine.setProperty("rate", self.rate)

        for voice in self.engine.getProperty('voices'):
            language = voice.id.split('TTS_MS_')[1].split('_')[0]

            if self.lang == language.lower() or self.lang in language.lower():
                self.voice = voice
                logger.info("Selected audio language found!")
                break

        if self.voice == None:
            logger.warning("Selected audio language is not installed in the OS!")
            self.voice = self.engine.getProperty('voices')[0]

        self.engine.setProperty("voice", self.voice.id)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def save(self, text, route):
        self.engine.save_to_file(text, EXPORT_DIR + route)
        self.engine.runAndWait()
