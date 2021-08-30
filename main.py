import json

from project.audio.audio_controller import get_audio_duration
from project.audio.models.voice_engine import VoiceEngine, EXPORT_DIR
from routes import ROOT_DIR

with open(ROOT_DIR + r"\inputs\example.json", encoding="utf8") as file:
    data = json.load(file)
    voice = VoiceEngine(rate=data['voice_speed'])

    for i in range(0, len(data['phrases'])):
        file_route = '\\' + data['title']+'_audio_'+str(i) + data['audio_format']

        voice.save(data['phrases'][i]['text'], file_route)
        data['phrases'][i]['audio']['route'] = EXPORT_DIR + file_route
        data['phrases'][i]['audio']['duration'] = get_audio_duration(EXPORT_DIR + file_route)
        data['phrases'][i]['audio']['volume'] = 0

    with open('example.json', 'w') as outfile:
        json.dump(data, outfile)