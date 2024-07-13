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
        fodder (str): The word or phrase to be anagrammed.
        answer (str): The answer to the clue.

    >>> Anagram('shredded corset', 'shredded <fodder>', 'corset', 'ESCORT')
    Anagram(clue='shredded corset', indicator='shredded <fodder>', fodder='corset', answer='ESCORT')
    >>> Anagram('Mixed up clue', 'Mixed up <fodder>', 'clue', 'ANSWER')
    Traceback (most recent call last):
    ...
    ValueError: Answer "ANSWER" must be an anagram of "clue"
    """
    clue: str
    indicator: str
    fodder: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the fodder
        check_indicator_matches(self.clue, self.indicator, {'fodder': self.fodder}) 
       
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is an anagram of the fodder
        if sorted(normalize(self.fodder)) != sorted(self.answer):
            raise ValueError(f'Answer "{self.answer}" must be an anagram of "{self.fodder}"')

@dataclass(frozen=True)
class Hidden(ClueType):
    """
    A hidden word type clue. The answer is hidden within the clue text.

    Attributes:
        clue (str): The full text of the clue.
        indicator (str): The part of the clue that indicates a hidden word.
        left (str): The text before the hidden word.
        hidden (str): The hidden word (the answer).
        right (str): The text after the hidden word.
        answer (str): The answer to the clue.

    >>> Hidden('Found ermine, deer hides', '<left><hidden><right> hides', 'Found ', 'ermine, d', 'eer', 'ERMINED')
    Hidden(clue='Found ermine, deer hides', indicator='<left><hidden><right> hides', left='Found ', hidden='ermine, d', right='eer', answer='ERMINED')
    >>> Hidden('Introduction to do-gooder', 'Introduction to <hidden><right>', None, 'do-g', 'ooder', 'DOG')
    Hidden(clue='Introduction to do-gooder', indicator='Introduction to <hidden><right>', left=None, hidden='do-g', right='ooder', answer='DOG')
    >>> Hidden('Incorrect hidden clue', '<left><hidden><right> hides', 'Inc', 'orrect', ' hidden clue', 'WRONG')
    Traceback (most recent call last):
    ...
    ValueError: Indicator must match: clue: "Incorrect hidden clue", indicator: "<left><hidden><right> hides", parts: "{'left': 'Inc', 'hidden': 'orrect', 'right': ' hidden clue'}", indicator replaced with parts: "Incorrect hidden clue hides"
    """
    clue: str
    indicator: str
    left: str
    hidden: str
    right: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the hidden word
        check_indicator_matches(self.clue, self.indicator, {'left': self.left, 'hidden': self.hidden, 'right': self.right})

        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the hidden word produces the answer
        if normalize(self.hidden) != self.answer:
            raise ValueError(f'Hidden word "{self.hidden}" must produce answer "{self.answer}"')