
class Token:

  def __init__(self, word):
    self.term = word
    self.cleaned = None

  def is_cleaned(self):
    return self.cleaned is not None

  # def __str__(self):
  #   return self.term if self.cleaned_term is None else self.cleaned_term
