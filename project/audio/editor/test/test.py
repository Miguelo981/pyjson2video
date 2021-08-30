from pydub import AudioSegment
from main import ROOT_DIR

song = AudioSegment.from_mp3(ROOT_DIR + r"\exports\example.wav")

# pydub does things in milliseconds
ten_seconds = 10 * 1000

first_10_seconds = song[:ten_seconds]
last_5_seconds = song[-5000:]

# boost volume by 6dB
beginning = first_10_seconds + 6
# reduce volume by 3dB
end = last_5_seconds - 3

with_style = beginning.append(end, crossfade=1500)
do_it_over = with_style * 2
awesome = do_it_over.fade_in(2000).fade_out(3000)
awesome.export("mashup.wav", format="wav")