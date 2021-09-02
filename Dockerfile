FROM balenalib/raspberry-pi-python:3-latest

WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y ffmpeg imagemagick espeak-ng-espeak libespeak-ng-libespeak1
#espeak speech-dispatcher-espeak open-jtalk
COPY . .
RUN mkdir /usr/share/fonts/custom
COPY ./assets/fonts /usr/share/fonts/custom
RUN fc-cache -v /usr/share/fonts
#RUN pip install -r requirements_docker.txt
RUN pip install --upgrade pip
RUN apt-get install -y python3-numpy
RUN pip3 install pydub gTTS pyttsx3 Pillow loguru moviepy

#RUN git clone --depth 1 git://git.videolan.org/x264
#RUN cd x264
#RUN ./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl
#RUN make -j 4
#RUN make install
#
#RUN git clone --depth=1 git://source.ffmpeg.org/ffmpeg.git
#RUN cd ffmpeg
#RUN ./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree
#RUN make -j4
#RUN make install