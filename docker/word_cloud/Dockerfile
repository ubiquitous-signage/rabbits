FROM python:3

WORKDIR /usr/src/app

# apt update
RUN apt-get update

# port audio
RUN apt-get -y install libasound-dev  alsa-utils sox libsox-fmt-all
RUN wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
RUN tar zxvf pa_stable_v19_20140130.tgz
WORKDIR /usr/src/app/portaudio
RUN ./configure && make
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/lib
RUN make install

RUN echo 'dtparam=audio=on' > /boot/config.txt

# python dependencies
RUN pip install --upgrade google-cloud SpeechRecognition pyaudio

# clone rabbits
WORKDIR /usr/src/app
RUN git clone --depth 1 https://github.com/ubiquitous-signage/rabbits.git

ENV MS_BING_SPEECH_API_KEY=$MS_BING_SPEECH_API_KEY
ENV MS_TEXT_ANALYTICS_API_KEY=$MS_TEXT_ANALYTICS_API_KEY
ENV IBM_USERNAME=$IBM_USERNAME
ENV IBM_PASSWORD=$IBM_PASSWORD
ENV GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
ENV DOCOMO_APIKEY=$DOCOMO_APIKEY

WORKDIR /usr/src/app/rabbits/word_cloud
CMD [ "python", "./main.py" ]
# CMD [ "sh", "/bin/bash"]
