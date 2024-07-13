from dataclasses import dataclass
from cryptic_strings import *

class ClueType:
    """
    Base class of all clue types. All clues have the form
    SomeClueType(clue: Text, ..., answer: Answer)
    """
    pass

@dataclass(frozen=True)
class Definition(ClueType):
    """
    A definition type clue. This is the simplest form of clue where the clue
    directly defines the answer.

    Attributes:
        clue (str): The definition part of the clue.
        answer (str): The answer to the clue.

    >>> Definition('Chaperone', 'ESCORT')
    Definition(clue='Chaperone', answer='ESCORT')
    >>> Definition('Chaperone', 'escort')
    Traceback (most recent call last):
    ...
    ValueError: "escort" must be in "answer" form: only uppercase, spaces and hyphens
    >>> Definition('Quick movement', 'DART')
    Definition(clue='Quick movement', answer='DART')
    >>> Definition('Celestial body', 'STAR')
    Definition(clue='Celestial body', answer='STAR')
    """
    clue: str
    answer: str

    def __post_init__(self):
        # Validate that the answer is in the correct format
        check_answer(self.answer)

@dataclass(frozen=True)
class Anagram(ClueType):
    """
    An anagram type clue. The clue contains a word or phrase that can be
    rearranged to form the answer.

    Attributes:
        clue (str): The full text of the clue.
        indicator (str): The part of the clue that indicates an anagram should be performed.
        target (str): The word or phrase to be anagrammed.
        answer (str): The answer to the clue.

    >>> Anagram('shredded corset', 'shredded <target>', 'corset', 'ESCORT')
    Anagram(clue='shredded corset', indicator='shredded <target>', target='corset', answer='ESCORT')
    >>> Anagram('Mixed up clue', 'Mixed up <target>', 'clue', 'ANSWER')
    Traceback (most recent call last):
    ...
    ValueError: Answer "ANSWER" must be an anagram of "clue"
    """
    clue: str
    indicator: str
    target: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the target
        if not indicator_matches(self.clue, self.indicator, { 'target': self.target }):
            raise ValueError(f'Anagram indicator "{self.indicator}" must match "{self.clue}" and produce "{self.target}"')
        
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is an anagram of the target
        if sorted(normalize(self.target)) != sorted(self.answer):
            raise ValueError(f'Answer "{self.answer}" must be an anagram of "{self.target}"')