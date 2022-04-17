import re
import logging
import gensim
from collections import Counter
from datetime import timedelta
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from gensim.models.wrappers import FastText # module yang lama
from gensim.models.fasttext import FastText # module yang lebih baru
from collections import Counter

logging.basicConfig(level=logging.INFO)

model = FastText.load_fasttext_format('drive/My Drive/Skripsi/Google Colab/cc.id.300.bin')


dictionary1 = list(model.wv.vocab)
dictionary1 = [term for term in dictionary1 
                  if len(term) > 1 and re.search(r'[^a-z-]', term.lower()) is None]
dictionary1 += [
                "pemilu","pilpres","kpu", ""]

factory = StemmerFactory()
dictionary2 = factory.get_words()

words1 = Counter(dictionary1)
words2 = Counter(dictionary2)

def words(text): return re.findall(r'\w+', text.lower())

# WORDS = Counter(
#     list(set(dictionary1 + dictionary2)))
WORDS = words1
# WORDS = Counter(words(open('katadasar.txt').read()))

def P(word, N=sum(WORDS.values())):
    # "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    # "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    # "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def correction2(word):
    global WORDS, words1, words2
    WORDS = words1
    res = correction(word)
    if res == word:
      WORDS = words2
      res = correction(word)
    return res

def known(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    # "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)] # [('', 'kemarin'), ('k', 'emarin'), ('ke', 'marin'), dst]
    deletes    = [L + R[1:]               for L, R in splits if R] # ['emarin', 'kmarin', 'kearin', dst]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1] # ['ekmarin', 'kmearin', 'keamrin', dst]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters] # ['aemarin', 'bemarin', 'cemarin', dst]
    inserts    = [L + c + R               for L, R in splits for c in letters] # ['akemarin', 'bkemarin', 'ckemarin', dst]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    # "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def text_correction(text):
    res = []
    for word in text.split(" "):
      res.append(
          correction2(word))
    return " ".join(res)
    
