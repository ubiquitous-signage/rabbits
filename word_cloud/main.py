import recognizer
import text_analytics
import sensitive_filter
import os
import requests
import json

URL="http://localhost:9000/api/word-cloud"

def loop():
  while True:
    run()
    print('---------------------------------------------')

def run():
  text = recognizer.live(recognizer.API_OPTIONS.GOOGLE_CLOUD)
  if text == None:
    return
  words = text_analytics.syntax_text(text)
  if not words:
    print('could not analyze words')
    return
  print('recognized words: ' + str(words))
  filtered_words = sensitive_filter.filter(words)
  print('filterd words:    ' + str(filtered_words))
  post(filtered_words)

def post(words):
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
    print('post status code: ' + str(r))
  except requests.exceptions.ConnectionError:
    print("please run hamster!")

if __name__ == '__main__':
  loop()
  # run()