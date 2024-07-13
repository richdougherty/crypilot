from dataclasses import dataclass
from .clues import *
from .cryptic_strings import *
    
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
