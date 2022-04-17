import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from .utils import (
  ROOT_WORD, ABBREVIATION, stemming, change_abbreviation, is_stopwords, is_root)
from .token import Token
from .wordEmbedding import correction2

STOPWORDS = StopWordRemoverFactory().get_stop_words()

class Preprocessing:
  
  def __init__(self, text):
    self.text = text
    self.cleaned_text = None
    self.tokens = []

  def load_text(self, text):
    self.text = text

  def update_cleaned(self):
    self.cleaned_text = " ".join(
      [token.cleaned for token in self.tokens])

  def is_cleaned(self):
    return self.cleaned_text != None

  def clean(self):
    ###########
    # Convert to lower case
    cleaned = self.text.lower()

    ###########
    # Convert www.* or https?://* to URL
    # text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', "", text)
    # Another way https://gist.github.com/nishad/ff5d02394afaf8cca5818f023fb88a21
    regex1 = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""
    regex2 = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    cleaned = re.sub(regex1, "", cleaned)
    cleaned = re.sub(regex2, "", cleaned)

    ###########
    # Convert @username to AT_USER
    cleaned = re.sub('@[^\s]+', " ", cleaned)

    ###########
    # Remove hastags. ex: "asdfasdf #pastibisa #eifjaa" to "asdfasdf "
    cleaned = re.sub(r'#([^\s]+)', " ", cleaned)

    ###########
    # Remove duplicate character that more than 2
    # https://stackoverflow.com/questions/4574509/remove-duplicate-chars-using-regex
    cleaned = re.sub(r'([a-z])\1{2,}', r'\1', cleaned)
    
    ###########
    # Replace #word with word
    # text = re.sub(r'#([^\s]+)', r'\1', text)
    ###########
    # menghapus angka
    # text = re.sub(r"\d+", "", text)

    ###########
    # Remove character execpt
    #   (1) alphabetical character. from a to z
    #   (2) '-' character
    #   (3) ' ' character
    cleaned = re.sub('[^a-z- ]',' ', cleaned)

    ###########
    # Remove additional white spaces
    cleaned = re.sub('[\s]+', ' ', cleaned)

    ###########
    # remove spaces at the beginning and at the end of the string
    cleaned = cleaned.strip()

    for word in cleaned.split(" "):
      if word == "":
        continue

      token = Token(word)
      # change abbreviation
      is_abbreviation, res = change_abbreviation(word)
      if is_abbreviation:
        if not is_stopwords(res):
          token.cleaned = res
        continue

      w_stem = stemming(word)
      if is_root(w_stem):
        if not is_stopwords(w_stem):
          token.cleaned(w_stem)
          self.tokens.append(token)
        continue
      
      word = correction2(word)
      word = stemming(word)

      if is_stopwords(word):
        continue
      else:
        token.cleaned = word

      self.tokens.append(token)
    
    self.update_cleaned()

    
      
