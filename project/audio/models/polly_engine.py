import boto3

from decouple import config
from loguru import logger

from project.audio.editor.audio_editor import convert_audio_mp3_file
from project.audio.models.audio_engine import VoiceEngine


class PollyVoice():
    def __init__(self, Gender, Id, LanguageCode, LanguageName, Name, SupportedEngines=None):
        self.gender = Gender
        self.id = Id
        self.language_name = LanguageName
        self.language_code = LanguageCode
        self.name = Name

class PollyEngine(VoiceEngine):
    def __init__(self, rate=140, lang="en", gender="male"):
        VoiceEngine.__init__(self, rate, lang, gender)
        self.voice = None
        self.client = None

        self.__set_properties()

    def __set_properties(self):
        self.client = boto3.resource('s3')

        self.client = boto3.client('polly',
                              aws_access_key_id=config('POLLY_USER_ID'),
                              aws_secret_access_key=config('POLLY_SECRET_KEY'),
                              region_name=config('REGION_NAME'))
        list = self.client.describe_voices()['Voices']

        for voice in list:
            if self.lang in voice['LanguageCode'].lower() and self.gender.lower() in voice['Gender'].lower():
                self.voice = PollyVoice(**voice)
                logger.info("Selected audio language found!")
                break

        if self.voice is None:
            logger.warning("Selected audio language is not installed in the OS!")
            self.voice = PollyVoice(**list[0])

    def save(self, text, route):
        response = self.client.synthesize_speech(VoiceId=self.voice.id,
                                                  OutputFormat='mp3',
                                                  Text=text)

        with open(route, 'wb') as file:
            file.write(response['AudioStream'].read())
            convert_audio_mp3_file(route)
