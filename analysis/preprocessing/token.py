
class Token:

  def __init__(self, word):
    self.term = word
    self.cleaned = None

  def is_cleaned(self) -> bool:
    return self.cleaned is not None

  def __eq__(self, __o: object) -> bool:
    return self.term == __o.term and self.cleaned == __o.cleaned

  def __hash__(self) -> int:
      return hash(f'{self.term}/{self.cleaned}')
