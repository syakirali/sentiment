import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from IPython.display import display

from analysis.utils import progress
from .preprocessing import Preprocessing

STOPWORDS = StopWordRemoverFactory().get_stop_words()

class PreprocessingFactory:
  
  def __init__(self, d=None):
    self.data = []
    if d is not None:
      self.load_data(d)

  def get_unique_tokens(self):
    return list(set(
      [
        token
        for p in self.data
        for token in p.tokens
      ]))

  def load_data(self, d):
    self.data = [ Preprocessing(tweet) for tweet in d ]

  def get_cleaned_data(self):
    return [ p.cleaned_text for p in self.data if p.is_cleaned ]

  def clean_all(self, show_progress=True):
    if show_progress:
      p = display(progress(0, 100), display_id=True)
    for i, r in enumerate(self.data):
      if show_progress:
        p.update(progress(
          (i + 1) * 100 / len(self.data), 100
        ))
      r.clean()
    return self.get_cleaned_data(cached=False)
