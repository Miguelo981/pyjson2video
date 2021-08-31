FROM jonathangoorin/moviepy:latest

WORKDIR /usr/src/app
#RUN apt-get update && apt-get install -y ffmpeg imagemagick
RUN apt-get update && apt-get install -y espeak-ng-espeak libespeak-ng-libespeak1 open-jtalk #espeak speech-dispatcher-espeak
COPY . .
RUN pip install -r requirements.txt
