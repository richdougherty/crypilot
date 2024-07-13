from dataclasses import dataclass
from clues import *
from cryptic_strings import *
from clue_text import *
    
class SolutionType:
    """
    Base class for all solution types.
    """
    pass

@dataclass(frozen=True)
class DoubleSolution(SolutionType):
    """
    Represents a solution that combines two different clue types to form a single answer.

    Attributes:
        clue (str): The full text of the clue.
        answer_pattern (str): The pattern that the answer should match.
        solution1 (ClueType): The first part of the solution.
        solution2 (ClueType): The second part of the solution.
        answer (str): The final answer to the clue.

    >>> DoubleSolution(
    ...   clue = 'Not seeing window covering',
    ...   answer_pattern = '_____',
    ...   solution1 = Definition('Not seeing', 'BLIND'),
    ...   solution2 = Definition('window covering', 'BLIND'),
    ...   answer = 'BLIND'
    ... )
    DoubleSolution(clue='Not seeing window covering', answer_pattern='_____', solution1=Definition(clue='Not seeing', answer='BLIND'), solution2=Definition(clue='window covering', answer='BLIND'), answer='BLIND')

    >>> DoubleSolution(
    ...   clue = 'Eastern European buff',
    ...   answer_pattern = '______',
    ...   solution1 = Definition('Eastern European', 'POLISH'),
    ...   solution2 = Definition('buff', 'POLISH'),
    ...   answer = 'POLISH'
    ... )
    DoubleSolution(clue='Eastern European buff', answer_pattern='______', solution1=Definition(clue='Eastern European', answer='POLISH'), solution2=Definition(clue='buff', answer='POLISH'), answer='POLISH')

    >>> DoubleSolution(
    ...   clue = 'Lap dancing friend',
    ...   answer_pattern = '___',
    ...   solution1 = Anagram('Lap dancing', '<fodder> dancing', 'Lap', 'PAL'),
    ...   solution2 = Definition('friend', 'PAL'),
    ...   answer = 'PAL'
    ... )
    DoubleSolution(clue='Lap dancing friend', answer_pattern='___', solution1=Anagram(clue='Lap dancing', indicator='<fodder> dancing', fodder='Lap', answer='PAL'), solution2=Definition(clue='friend', answer='PAL'), answer='PAL')

    >>> DoubleSolution(
    ...   clue = 'Returned beer fit for a king',
    ...   answer_pattern = '_____',
    ...   solution1 = Reversal(
    ...       Combination(
    ...           'Returned beer',
    ...           'Returned ', Definition('beer', 'LAGER'), '',
    ...           'Returned LAGER'
    ...       ),
    ...       'Returned <fodder>', 'LAGER', 'REGAL'
    ...   ),
    ...   solution2 = Definition('fit for a king', 'REGAL'),
    ...   answer = 'REGAL'
    ... )
    DoubleSolution(clue='Returned beer fit for a king', answer_pattern='_____', solution1=Reversal(clue=Combination(input='Returned beer', prefix='Returned ', combined=Definition(clue='beer', answer='LAGER'), suffix='', output='Returned LAGER'), indicator='Returned <fodder>', fodder='LAGER', answer='REGAL'), solution2=Definition(clue='fit for a king', answer='REGAL'), answer='REGAL')

    >>> # Test for error when solutions don't match
    >>> DoubleSolution(
    ...   clue = 'Incorrect clue example',
    ...   answer_pattern = '___',
    ...   solution1 = Definition('Incorrect clue', 'BAD'),
    ...   solution2 = Definition('example', 'EGG'),
    ...   answer = 'BAD'
    ... )
    Traceback (most recent call last):
    ...
    ValueError: In a double solution, both solution answers must match: "BAD" != "EGG"

    >>> # Test for error when solutions are the same type
    >>> DoubleSolution(
    ...   clue = 'Repeated Repeated',
    ...   answer_pattern = '___',
    ...   solution1 = Definition('Repeated', 'DUP'),
    ...   solution2 = Definition('Repeated', 'DUP'),
    ...   answer = 'DUP'
    ... )
    Traceback (most recent call last):
    ...
    ValueError: In a double solution, the first solution (Definition(clue='Repeated', answer='DUP')) must be different to the second (Definition(clue='Repeated', answer='DUP'))

    >>> # Test for error when answer doesn't match pattern
    >>> DoubleSolution(
    ...   clue = 'Mismatch pattern test',
    ...   answer_pattern = '_____',
    ...   solution1 = Definition('Mismatch pattern', 'FAIL'),
    ...   solution2 = Definition('test', 'FAIL'),
    ...   answer = 'FAIL'
    ... )
    Traceback (most recent call last):
    ...
    ValueError: The answer "FAIL" does not match the answer pattern "_____"
    """
    clue: str
    answer_pattern: str
    solution1: ClueType
    solution2: ClueType
    answer: str

    def __post_init__(self):
        # Validate the answer pattern
        check_answer_pattern(self.answer_pattern)
        
        # Validate the answer
        check_answer(self.answer)
        
        # Check if the combined clues match the full clue
        joined_clues = clue_input(self.solution1.clue) + ' ' + clue_input(self.solution2.clue)
        if not equals_normalized(self.clue, joined_clues):
            raise ValueError(f'In a double solution, the clues for each solution should join to make the whole solution: "{self.clue}" != "{joined_clues}"')
        
        # Check if the two solutions are different
        if self.solution1 == self.solution2:
            raise ValueError(f'In a double solution, the first solution ({self.solution1}) must be different to the second ({self.solution2})')
        
        # Check if both solution answers match
        if self.solution1.answer != self.solution2.answer:
            raise ValueError(f'In a double solution, both solution answers must match: "{self.solution1.answer}" != "{self.solution2.answer}"')
        
        # Check if the solution answers match the final answer
        if self.solution1.answer != self.answer:
            raise ValueError(f'In a double solution, the solution answers must match the final answer: "{self.solution1.answer}" != "{self.answer}"')
        
        # Validate that the answer matches the answer pattern
        if not answer_matches_pattern(self.answer, self.answer_pattern):
            raise ValueError(f'The answer "{self.answer}" does not match the answer pattern "{self.answer_pattern}"')