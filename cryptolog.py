from dataclasses import dataclass
from typing import NewType, Tuple
import re

def normalize(s: str) -> str:
  """
  The normalized form is the display form converted to uppercase with
  non-letters removed. This gives the basis for how letters are treated
  in a crossword.

  >>> normalize('Hello world!')
  'HELLOWORLD'
  """
  return ''.join(c.upper() for c in s if c.isalnum())

def equals_normalized(a: str, b: str) -> bool:
  """
  Checks if thoe normalizd forms of the strings are equal.
  """
  return normalize(a) == normalize(b)

def is_normalized(s: str) -> bool:
  """
  Checks if a string is in normalized form.
  """
  return s == normalize(s)

def check_normalized(s: str) -> bool:
  if not is_normalized(s):
    raise ValueError(f'"{s}" must be in normalized form')

def is_answer(s: str) -> bool:
  """
  An answer is only uppercase, spaces and hyphens.
  """
  return re.match(r'^[A-Z \-]+$', s) is not None

def check_answer(s: str) -> bool:
  if not is_answer(s):
    raise ValueError(f'"{s}" must be in "answer" form: only uppercase, spaces and hyphens')

def normalize_answer(s: str) -> str:
  """
  The normalized form is the display form converted to uppercase with
  non-letters removed. This gives the basis for how letters are treated
  in a crossword.

  >>> normalize('HELLO WORLD')
  'HELLOWORLD'
  """
  if not is_answer(s):
    raise ValueError(f'Answers "{s}" must be only capitals, spaces and hyphens')
  return ''.join(c.upper() for c in s if c.isalpha())

def is_answer_pattern(s: str) -> bool:
  """
  An answer pattern is a string that is represents the letter pattern that the
  answer must fit into. It consists of uppercase letters, underscores
  for unknown letters as well as separators between words: spaces,
  dashes. E.g. 

  >>> is_answer_pattern("_____")
  True
  >>> is_answer_pattern("__-__")
  True
  >>> is_answer_pattern("U_-O_")
  True
  >>> is_answer_pattern("UH-OH")
  True
  >>> is_answer_pattern('Hello world')
  False
  >>> is_answer_pattern('ABC!')
  False
  """
  return re.match(r'^[A-Z_ \-]+$', s) is not None

def check_answer_pattern(s: str) -> bool:
  if not is_answer_pattern(s):
    raise ValueError(f'"{s}" must be in answer pattern form: only uppercase, spaces, hyphens and underscores')

def answer_matches_pattern(answer: str, answer_pattern: str):
  """
  >>> answer_matches_pattern('FOO', '___')
  True
  >>> answer_matches_pattern('F-OO', '___')
  True
  >>> answer_matches_pattern('FOO', '__ _')
  True
  >>> answer_matches_pattern('FO O', '_ __')
  True
  >>> answer_matches_pattern('FO-O', '_-_-_')
  True
  >>> answer_matches_pattern('FOO', '__ _')
  True
  >>> answer_matches_pattern('FOO', '_')
  False
  >>> answer_matches_pattern('FOO', '_____')
  False
  >>> answer_matches_pattern('FOO', 'F__')
  True
  >>> answer_matches_pattern('FOO', 'X__')
  False
  >>> answer_matches_pattern('FOO', '_OO')
  True
  """
  check_answer(answer)
  check_answer_pattern(answer_pattern)
  # Normalize the answer by removing non-alphabetic characters
  clean_answer = ''.join(c for c in answer if c.isalpha())
  
  # Create a regex pattern from the answer_pattern
  pattern = answer_pattern.replace('_', '.').replace(' ', r'\s*').replace('-', r'-?')
  pattern = f'^{pattern}$'
  
  # Match the clean answer against the pattern
  return bool(re.match(pattern, clean_answer, re.IGNORECASE))

def indicator_matches(clue: str, indicator: str, parts: dict[str, str]) -> bool:
    """
    Confirms whether an indicator string when applied to the given target
    string produces the given results.

    Args:
        clue (str): The original clue string.
        indicator (str): The indicator string with placeholders.
        parts (dict[str, str]): A dictionary of parts to replace in the indicator.

    Returns:
        bool: True if the indicator matches the clue after replacements, False otherwise.

    Raises:
        ValueError: If a bracketed key in the indicator is not found in the parts dictionary.

    >>> indicator_matches('shredded corset', 'shredded <anagram>', { 'anagram': 'corset' })
    True
    >>> indicator_matches('shredded pickle', 'shredded <anagram>', { 'anagram': 'corset' })
    False
    >>> indicator_matches(
    ...     'PAL outside of U',
    ...     '<left><right> outside of <middle>',
    ...     {
    ...         'left': 'P',
    ...         'right': 'AL',
    ...         'middle': 'U'
    ...     }
    ... )
    True
    """
    replaced_indicator = indicator
    for key, value in parts.items():
      bracketed_key = f'<{key}>'
      if bracketed_key not in replaced_indicator:
        raise ValueError(f"Bracketed key '{bracketed_key}' not found in indicator")
      replaced_indicator = replaced_indicator.replace(bracketed_key, value, 1)
    return equals_normalized(replaced_indicator, clue)

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
    
class SolutionType:
  pass

@dataclass(frozen=True)
class DoubleSolution(SolutionType):
  """

  >>> DoubleSolution(
  ...   clue = 'Chaperone shredded corset',
  ...   answer_pattern = '______',
  ...   solution1 = Definition('Chaperone', 'ESCORT'),
  ...   solution2 = Anagram('shredded corset', 'shredded <target>', 'corset', 'ESCORT'),
  ...   answer = 'ESCORT'
  ... )
  DoubleSolution(clue='Chaperone shredded corset', answer_pattern='______', solution1=Definition(clue='Chaperone', answer='ESCORT'), solution2=Anagram(clue='shredded corset', indicator='shredded <target>', target='corset', answer='ESCORT'), answer='ESCORT')
  """
  clue: str
  answer_pattern: str
  solution1: ClueType
  solution2: ClueType
  answer: str

  def __post_init__(self):
    check_answer_pattern(self.answer)
    check_answer(self.answer)
    joined_clues = self.solution1.clue + ' ' + self.solution2.clue
    if not equals_normalized(self.clue, joined_clues):
      raise ValueError(f'In a double solution, the clues for each solution should join to make the whole solution: "{self.clue}" != "{joined_clues}"')
    if self.solution1 == self.solution2:
      raise ValueError(f'In a double solution, the first solution ({self.solution1}) must be different to the second ({self.solution2})')
    if self.solution1 == self.solution2:
      raise ValueError(f'In a double solution, both solution answers must match: "{self.solution1.answer}" != "{self.solution2.answer}"')
    check_answer(self.answer)
