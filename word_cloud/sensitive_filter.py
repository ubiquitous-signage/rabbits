import os
import requests
import json
import urllib

URL = 'https://api.apigw.smt.docomo.ne.jp/truetext/v1/sensitivecheck'
APIKEY = os.environ['DOCOMO_APIKEY']

ENDPOINT = URL + '?APIKEY=' + APIKEY

def isFiltered(word):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  payload = 'text=' + urllib.parse.quote(word)
  r = requests.post(ENDPOINT, data=payload, headers=headers)
  return 'quotients' in r.json()

def filter(words):
  res = []
  for word in words:
    if not isFiltered(word):
      res.append(word)
  return res


if __name__ == "__main__":
  words = ['下ネタ',  '犬', '家族']
  print(words)
  print(filter(words))