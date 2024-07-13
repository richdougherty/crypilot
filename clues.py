from dataclasses import dataclass, field
from cryptic_strings import *

class ClueType:
    """
    Base class of all clue types. All clues have the form
    SomeClueType(clue: Text, ..., answer: Answer)
    """
    pass

@dataclass(frozen=True)
class Anagram(ClueType):
    """
    An anagram type clue. The clue contains a word or phrase that can be
    rearranged to form the answer.

    Attributes:
        indicator (str): The part of the clue that indicates an anagram should be performed.
        fodder (str): The word or phrase to be anagrammed.
        answer (str): The answer to the clue.
        clue (str): The full text of the clue, derived from indicator and fodder.

    >>> Anagram('shredded <fodder>', 'corset', 'ESCORT')
    Anagram(indicator='shredded <fodder>', fodder='corset', answer='ESCORT', clue='shredded corset')
    >>> Anagram('Mixed up <fodder>', 'clue', 'ANSWER')
    Traceback (most recent call last):
    ...
    ValueError: Answer "ANSWER" must be an anagram of "clue"
    """
    indicator: str
    fodder: str
    answer: str
    clue: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'clue', indicator_clue(self.indicator, {'fodder': self.fodder}))
        
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is an anagram of the fodder
        if sorted(normalize(self.fodder)) != sorted(self.answer):
            raise ValueError(f'Answer "{self.answer}" must be an anagram of "{self.fodder}"')

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
class Hidden(ClueType):
    """
    A hidden word type clue. The answer is hidden within the clue text.

    Attributes:
        indicator (str): The part of the clue that indicates a hidden word.
        left (str): The text before the hidden word.
        hidden (str): The hidden word (the answer).
        right (str): The text after the hidden word.
        answer (str): The answer to the clue.
        clue (str): The full text of the clue, derived from indicator, left, hidden, and right.

    >>> Hidden('<left><hidden><right> hides', 'Found ', 'ermine, d', 'eer', 'ERMINED')
    Hidden(indicator='<left><hidden><right> hides', left='Found ', hidden='ermine, d', right='eer', answer='ERMINED', clue='Found ermine, deer hides')
    >>> Hidden('Introduction to <hidden><right>', None, 'do-g', 'ooder', 'DOG')
    Hidden(indicator='Introduction to <hidden><right>', left=None, hidden='do-g', right='ooder', answer='DOG', clue='Introduction to do-gooder')
    >>> Hidden('<left><hidden><right> hides', 'Inc', 'orrect', ' hidden clue', 'WRONG')
    Traceback (most recent call last):
    ...
    ValueError: Hidden word "orrect" must produce answer "WRONG"
    """
    indicator: str
    left: str
    hidden: str
    right: str
    answer: str
    clue: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'clue', indicator_clue(self.indicator, {'left': self.left, 'hidden': self.hidden, 'right': self.right}))

        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the hidden word produces the answer
        if normalize(self.hidden) != self.answer:
            raise ValueError(f'Hidden word "{self.hidden}" must produce answer "{self.answer}"')

@dataclass(frozen=True)
class Reversal(ClueType):
    """
    A reversal type clue. The answer is formed by reversing a word or phrase in the clue.

    Attributes:
        indicator (str): The part of the clue that indicates a reversal should be performed.
        fodder (str): The word or phrase to be reversed.
        answer (str): The answer to the clue.
        clue (str): The full text of the clue, derived from indicator and fodder.

    >>> Reversal('Returned <fodder>', 'lager', 'REGAL')
    Reversal(indicator='Returned <fodder>', fodder='lager', answer='REGAL', clue='Returned lager')
    >>> Reversal('Returned <fodder>', 'lager', 'ALGAE')
    Traceback (most recent call last):
    ...
    ValueError: Answer "ALGAE" must be a reversal of "lager"
    """
    indicator: str
    fodder: str
    answer: str
    clue: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'clue', indicator_clue(self.indicator, {'fodder': self.fodder}))
       
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is a reversal of the fodder
        if normalize(self.fodder)[::-1] != self.answer:
            raise ValueError(f'Answer "{self.answer}" must be a reversal of "{self.fodder}"')
        
        # This is a simple check to ensure the answer is a valid word
        # In a real system, you'd want to check against a dictionary
        if len(self.answer) < 2:
            raise ValueError(f'Answer "{self.answer}" must be a valid word')