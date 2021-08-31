FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN apt-get -y install ffmpeg imagemagick
COPY . .
