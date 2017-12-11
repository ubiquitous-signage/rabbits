import binascii
import nfc
import requests
import json
import signal
import sys

URL="http://localhost:9000/api/context"

class MyCardReader(object):
  map = {
    '013200022d171900': 'ja',
    '013200022d171a00': 'en',
  }

  def on_connect(self, tag):
    print("touched")
    self.idm = binascii.hexlify(tag.idm)
    self.post(self.idm)
    return True

  def on_release(self, tag):
    print("released")
    return True

  def read_id(self):
    clf = nfc.ContactlessFrontend('usb')
    try:
      clf.connect(rdwr={'on-connect': self.on_connect, 'on-release': self.on_release})
    finally:
      clf.close()

  def post(self, cardId):
    lang = self.map[cardId]
    print("detect: " + lang)
    headers = {
      'Content-Type': 'application/json',
      'Accept':       'application/json',
    }
    payload = {
      'Id'  : 0,
      'Lang': lang,
    }
    try:
      r = requests.post(URL, data=json.dumps(payload), headers=headers)
      print('post status code: ' + str(r))
    except requests.exceptions.ConnectionError:
      print("please run hamster!")

  def updateLang(self, cardId):
    print(cardId)
    client = pymongo.MongoClient('localhost', 27017)
    db = client['ubiquitous-signage']
    co = db.contexts
    lang = 'en'
    if cardId == '013200022d171900':
      print('ja!')
      lang = 'ja'
    elif cardId == '013200022d171a00':
      print('en!')
      lang = 'en'
    co.update({"id" : 0},{'$set': {'lang': lang}})
    # co = db.posts.insert_one(post)
    #co.insert_one(post)

def handler(signal, frame):
  print("exit")
  sys.exit(0)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, handler)
  cr = MyCardReader()
  while True:
    print("touch card:")
    cr.read_id()
    # cr.updateLang(cr.idm)
    # print cr.idm
