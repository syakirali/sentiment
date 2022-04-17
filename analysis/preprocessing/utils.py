from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()
ROOT_WORD = stemmer_factory.get_words_from_file()
STOPWORDS = StopWordRemoverFactory().get_stop_words()

def get_abbreviation():
  abbreviation = []
  with open(ROOT_PATH / "data" / "singkatan-lib.csv", 'r') as f:
    for line in f.read().split("\n"):
      t = line.split(",")
      if len(t) == 2:
        abbreviation.append(
            tuple([c for c in t]))
  return abbreviation

ABBREVIATION = get_abbreviation()

def stemming(text):
  return stemmer.stem(text)

def change_abbreviation(word):
  match = [r for r in ABBREVIATION if r[0] == word]
  if len(match) > 0:
    return True, match[0][1]
  return False, None

def is_stopwords(word):
  return word in STOPWORDS

def is_root(word):
  return word in ROOT_WORD

def remove_stopwords(text):
  terms = []
  for term in text.split(" "):
    if term not in STOPWORDS:
      terms.append(term)
  return " ".join(terms)
