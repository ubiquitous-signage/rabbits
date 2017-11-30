import recognizer
import text_analytics
import os
import requests
import json

URL="http://localhost:9000/api/word-cloud"

def loop():
  while True:
    run()

def run():
  text = recognizer.live(recognizer.API_OPTIONS.GOOGLE_CLOUD)
  if text == None:
    return
  words = text_analytics.syntax_text(text)
  print(words)
  post(words)

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
  r = requests.post(URL, data=json.dumps(payload), headers=headers)
  print(r)

if __name__ == '__main__':
  loop()