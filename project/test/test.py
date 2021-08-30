# from gtts import gTTS
# tts = gTTS('ここでは、ブラッククローバーの最新のあらすじや、\n 個人的な考察をまとめています。', lang='ja')
# tts.save('test.mp3')

import pyttsx3

try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[2].id)
    engine.runAndWait()
    print(engine.getProperty('voice'))
    engine.setProperty('rate', 140)
    text = 'ここでは、ブラッククローバーの最新のあらすじや、\n 個人的な考察をまとめています。'
    engine.say(text)
    #engine.save_to_file(text, "output.mp3")
    engine.runAndWait()
except Exception as error:
    print(error)