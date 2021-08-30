import pyttsx3

from routes import ROOT_DIR
from project.audio.utils import voice_driver_by_os

EXPORT_DIR = ROOT_DIR + r"\\project\audio\exports"

class VoiceEngine:
    def __init__(self, rate = 140):
        # self.engine = pyttsx3.init(voice_driver_by_os())
        self.engine = pyttsx3.init(voice_driver_by_os())
        self.voice = None
        self.rate = rate

        self.__set_properties()

    def __set_properties(self):
        self.engine.setProperty("rate", self.rate)
        self.voice = self.engine.getProperty('voices')[2].id
        self.engine.setProperty("voice", self.voice)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def save(self, text, route):
        self.engine.save_to_file(text, EXPORT_DIR + route)
        self.engine.runAndWait()
