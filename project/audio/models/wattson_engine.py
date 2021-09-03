from decouple import config
from loguru import logger

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from project.audio.editor.audio_editor import convert_audio_mp3_file
from project.audio.models.audio_engine import VoiceEngine


class WattsonVoice():
    def __init__(self, gender, supported_features, customizable, name, description, language, url):
        self.gender = gender
        self.supported_features = supported_features
        self.customizable = customizable
        self.name = name
        self.description = description
        self.language = language
        self.url = url

class WattsonEngine(VoiceEngine):
    def __init__(self, rate=140, lang="en", gender="male"):
        VoiceEngine.__init__(self, rate, lang, gender)
        self.voice = None

        self.__set_properties()

    def __set_properties(self):
        self.tts = TextToSpeechV1(
            authenticator= IAMAuthenticator(config('TT_WATSON_API_KEY'))
        )
        self.tts.set_service_url(config('TT_WATSON_URL'))


        list = self.tts.list_voices().result['voices']

        for voice in list:
            if self.lang in voice['language'].lower() and self.gender.lower() in voice['gender'].lower():
                self.voice = WattsonVoice(**voice)
                logger.info("Selected audio language found!")
                break

        if self.voice is None:
            logger.warning("Selected audio language is not installed in the OS!")
            self.voice = WattsonVoice(**list[0])

    def save(self, text, route, format="wav"):
        with open(route, 'wb') as audio_file:
            audio_file.write(self.tts.synthesize(text, voice=self.voice.name, accept='audio/mp3').get_result().content)
            convert_audio_mp3_file(route)