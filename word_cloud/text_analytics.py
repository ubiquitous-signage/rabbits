import requests
import json
import os
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

URL     = 'https://eastasia.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
API_KEY = os.environ['MS_TEXT_ANALYTICS_API_KEY']

def extractKeyPhrases(text):
  headers = {
    'Ocp-Apim-Subscription-Key': API_KEY,
    'Content-Type':              'application/json',
    'Accept':                    'application/json',
  }
  payload = {
    'documents': [
      {
        'id':       '123',
        'text':     text,
        'language': 'ja',
      }
    ]
  }
  r = requests.post(URL, data=json.dumps(payload), headers=headers)
  return r.json()["documents"][0]["keyPhrases"]

def syntax_text(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
        language='ja-JP'
    )

    # Detects syntax in the document. You can also analyze HTML with:
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    res = []

    for token in tokens:
      if pos_tag[token.part_of_speech.tag] is 'NOUN':
        res.append(token.text.content)

    return res

if __name__=='__main__':
  text = 'Twitter API の Search API でアカウントやキーワード検索のデータを取得したいが、手間がかかる。さらに分析してレポート作成するとなると．．．。そんな時。Microsoft Flow を使うと、クリック操作だけで'
  # print(extractKeyPhrases(text))
  print(syntax_text(text))