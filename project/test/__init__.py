
from project.audio.models.voice_engine import VoiceEngine

voice = VoiceEngine(rate=150)

text = 'ここでは、ブラッククローバーの最新のあらすじや、\n 個人的な考察をまとめています。'
voice.say(text)
voice.save(text, "example.mp3")