import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from .utils import (
  ROOT_WORD, ABBREVIATION, stemming, change_abbreviation, is_stopwords, is_root)
from .token import Token
from .preprocessing import Preprocessing
from .wordEmbedding import correction2

STOPWORDS = StopWordRemoverFactory().get_stop_words()

class PreprocessingFactory:
  
  def __init__(self, d=None):
    self.data = []
    if d is not None:
      self.load_data(d)
    self.cleaned_data = []

  def load_data(self, d):
    self.data = [ Preprocessing(text) for text in d ]

  def get_cleaned_data(self):
    return [ p.cleaned_text for p in self.data if p.is_cleaned ]

  def clean_all(self):
    for p in self.data:
      p.clean()
    return self.get_cleaned_data()
