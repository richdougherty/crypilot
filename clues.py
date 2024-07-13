from dataclasses import dataclass
from .cryptic_strings import *

class ClueType:
  """
  Base class of all clue types. All clues have the form
  SomeClueType(clue: Text, ..., answer: Answer)
  """
  pass

@dataclass(frozen=True)
class Definition(ClueType):
  """
  A definition type clue

  >>> Definition('Chaperone', 'ESCORT')
  Definition(clue='Chaperone', answer='ESCORT')
  """
  clue: str
  answer: str

  def __post_init__(self):
    check_answer(self.answer)

@dataclass(frozen=True)
class Anagram(ClueType):
  """
  >>> Anagram('shredded corset', 'shredded <target>', 'corset', 'ESCORT')
  Anagram(clue='shredded corset', indicator='shredded <target>', target='corset', answer='ESCORT')
  """
  clue: str
  indicator: str
  target: str
  answer: str

  def __post_init__(self):
    if not indicator_matches(self.clue, self.indicator, { 'target': self.target }):
      raise ValueError(f'Anagram indicator "{self.indicator}" must match "{self.clue}" and produce "{self.target}"')
    check_answer(self.answer)
    if sorted(normalize(self.target)) != sorted(self.answer):
      raise ValueError(f'Answer "{self.answer}" must be an anagram of "{self.target}"')