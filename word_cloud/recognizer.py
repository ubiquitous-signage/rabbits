#!/usr/bin/env python3
import speech_recognition as sr
import os
import enum
import json
from os import path

BING_KEY = os.environ["MS_BING_SPEECH_API_KEY"]  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
IBM_USERNAME = os.environ["IBM_USERNAME"]
IBM_PASSWORD = os.environ["IBM_PASSWORD"]
GOOGLE_CLOUD_SPEECH_CREDENTIALS_PATH = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

ENRGY_THRESOHLD = 0 # associated with the perceived loudness of the sound; if 0, automatically ajjusted
TIMEOUT_SEC = 10 # maximum number of seconds that this will allow a phrase to continue
LANGUAGE = 'ja-JP'

API_OPTIONS = enum.Enum("API_OPTIONS", "BING GOOGLE GOOGLE_CLOUD IBM")

# obtain audio from the microphone
def live(API_OPTION):
  r = sr.Recognizer()
  if ENRGY_THRESOHLD == 0:
    r.dynamic_energy_threshold = True
  else:
    r.enrgy_threshold = ENRGY_THRESOHLD

  with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, phrase_time_limit=TIMEOUT_SEC)

  return recognize(r,audio,API_OPTION)
  
def recorded(API_OPTION,file_name):
  AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), file_name)
  r = sr.Recognizer()
  with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
    BING_KEY = os.environ["MS_BING_SPEECH_API_KEY"]  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
  return recognize(r,audio,API_OPTION)

def recognize(r, audio, API_OPTION):
  if API_OPTION is API_OPTIONS.BING:
    try:
      text = r.recognize_bing(audio, key=BING_KEY, language=LANGUAGE)
      print("Microsoft Bing Voice Recognition: " + text)
      return text
    except sr.UnknownValueError:
      print("Microsoft Bing Voice Recognition could not understand audio")
      return None
    except sr.RequestError as e:
      print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

  elif API_OPTION is API_OPTIONS.GOOGLE:
    try:
      text = r.recognize_google(audio, language=LANGUAGE)
      print("Google Speech Recognition: " + text)
      return text
    except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
      return None
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

  elif API_OPTION is API_OPTIONS.GOOGLE_CLOUD:
    with open(GOOGLE_CLOUD_SPEECH_CREDENTIALS_PATH) as f:
      GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(json.load(f))
    try:
      text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language=LANGUAGE)
      print("Google Cloud Speech: " + text)
      return text
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

  elif API_OPTION is API_OPTIONS.IBM:
    try:
      text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD, language=LANGUAGE)
      print("IBM Speech to Text: " + text)
      return text
    except sr.UnknownValueError:
      print("IBM Speech to Text could not understand audio")
      return None
    except sr.RequestError as e:
      print("Could not request results from IBM Speech to Text service; {0}".format(e)) 

if __name__ == "__main__":
  api = API_OPTIONS.BING
  # print(live(api))
  recorded(API_OPTIONS.BING, "records/test_1.wav")
  recorded(API_OPTIONS.GOOGLE, "records/test_1.wav")
  recorded(API_OPTIONS.GOOGLE_CLOUD, "records/test_1.wav")
  recorded(API_OPTIONS.IBM, "records/test_1.wav")