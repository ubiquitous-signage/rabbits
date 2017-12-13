import recognizer
import text_analytics
import sensitive_filter
import os
import requests
import json
import speech_recognition as sr
import time
import threading
import sys

ENRGY_THRESOHLD = 0 # associated with the perceived loudness of the sound; if 0, automatically ajjusted
TIMEOUT_SEC = 4 # maximum number of seconds that this will allow a phrase to continue
LANGUAGE = 'ja-JP'

# URL='http://localhost:9000/api/word-cloud'
URL='http://35.200.70.212:9000/api/word-cloud'

isFilter = True
if sys.argv[1] == 'off':
  isFilter = False


def post(words):
  threadId = str(threading.get_ident())
  headers = {
    'Content-Type': 'application/json',
    'Accept':       'application/json',
  }
  payload = {
    'Words': []
  }
  for word in words:
    payload['Words'].append(
      {
        'Text':  word,
        'Count': 1, 
      }
    )
  try:
    r = requests.post(URL, data=json.dumps(payload), headers=headers)
    print('(' + threadId + ')post status code: ' + str(r))
  except requests.exceptions.ConnectionError:
    print('(' + threadId + ')please run hamster!')

def callback(r,audio):
  threadId = str(threading.get_ident())
  print('(' + threadId + ')detect')
  try:
    text = r.recognize_google(audio, language=LANGUAGE)
    print('(' + threadId + ')Google Speech Recognition: ' + text)
    words = text_analytics.syntax_text(text)
    if not words:
      print('(' + threadId + ')could not analyze words')
      return True
    print('(' + threadId + ')recognized words: ' + str(words))
    if isFilter:
      filtered_words = sensitive_filter.filter(words)
      print("filtered!")
    else:
      filtered_words = words
    print('(' + threadId + ')filterd words:    ' + str(filtered_words))
    post(filtered_words)
    return True
  except sr.UnknownValueError:
    print('(' + threadId + ')Google Speech Recognition: could not understand audio')
    return True
  except sr.RequestError as e:
    print('(' + threadId + ')Could not request results from Google Speech Recognition service; {0}'.format(e))
    return True

if __name__ == '__main__':
  threadId = str(threading.get_ident())
  print('(' + threadId + ')Say something!')
  r = sr.Recognizer()
  m = sr.Microphone()

  if ENRGY_THRESOHLD == 0:
    r.dynamic_energy_threshold = True
  else:
    r.enrgy_threshold = ENRGY_THRESOHLD

  with m as source:
    r.adjust_for_ambient_noise(source)

  stop_listening = r.listen_in_background(m, callback, phrase_time_limit=TIMEOUT_SEC)

  while True:
    time.sleep(1)