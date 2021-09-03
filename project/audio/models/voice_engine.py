import platform, pyttsx3

from gtts import gTTS
from loguru import logger
from project.audio.editor.audio_editor import convert_audio_mp3_file


class VoiceEngine:
    def __init__(self, rate = 140, lang="en"):
        self.engine = pyttsx3.init()
        self.voice = None
        self.rate = rate
        self.lang = lang

        self.__set_properties()

    def __set_properties(self):
        self.engine.setProperty("rate", self.rate)

        for voice in self.engine.getProperty('voices'):
            language = None

            if platform.system() == 'Linux':
                language = voice.languages[0].decode("utf-8")

            elif platform.system() == 'Windows':
                language = voice.id.split('TTS_MS_')[1].split('_')[0]

            elif platform.system() == 'Darwin':
                pass

            if language is not None and self.lang == language.lower() or self.lang in language.lower():
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
        if platform.system() == 'Linux':
            tts = gTTS(text=text, lang=self.lang)
            tts.save(route)
            convert_audio_mp3_file(route)
        elif platform.system() == 'Windows':
            self.engine.save_to_file(text, route)
            self.engine.runAndWait()