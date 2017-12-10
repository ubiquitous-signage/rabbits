import binascii
import nfc
import pymongo

class MyCardReader(object):

    def on_connect(self, tag):
        print "touched"
        self.idm = binascii.hexlify(tag.idm)
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()

    def updateLang(self, cardId):
        print cardId
        client = pymongo.MongoClient('localhost', 27017)
        db = client['ubiquitous-signage']
        co = db.contexts
        lang = 'en'
        if cardId == '013200022d171900':
            print 'ja!'
            lang = 'ja'
        elif cardId == '013200022d171a00':
            print 'en!'
            lang = 'en'
        co.update({"id" : 0},{'$set': {'lang': lang}})
        # co = db.posts.insert_one(post)
        #co.insert_one(post)

if __name__ == '__main__':
    cr = MyCardReader()
    while True:
        print "touch card:"
        cr.read_id()
        print "released"
        cr.updateLang(cr.idm)
        # print cr.idm
