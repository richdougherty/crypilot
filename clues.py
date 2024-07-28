from dataclasses import dataclass
from typing import Optional
from cry_strings import *
from clue_text import *

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
    clue: ClueText
    indicator: str
    fodder: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the fodder
        check_indicator_matches(clue_output(self.clue), self.indicator, {'fodder': self.fodder}) 
       
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is an anagram of the fodder
        if sorted(normalize(self.fodder)) != sorted(self.answer):
            raise ValueError(f'Answer "{self.answer}" must be an anagram of "{self.fodder}"')

@dataclass(frozen=True)
class Container(ClueType):
    """
    A container type clue. One set of letters is placed inside another.

    Attributes:
        clue (str): The full text of the clue.
        indicator (str): The part of the clue that indicates a container should be formed.
        outer_left (str): The left part of the word or phrase that forms the outer part of the container.
        outer_right (str): The right part of the word or phrase that forms the outer part of the container.
        inner (str): The word or phrase to be placed inside the outer parts.
        answer (str): The answer to the clue.

    >>> Container('PAL outside of U', '<outer_left><outer_right> outside of <inner>', 'PA', 'L', 'U', 'PAUL')
    Container(clue='PAL outside of U', indicator='<outer_left><outer_right> outside of <inner>', outer_left='PA', outer_right='L', inner='U', answer='PAUL')
    
    >>> Container('O in VICE', '<inner> in <outer_left><outer_right>', 'V', 'ICE', 'O', 'VOICE')
    Container(clue='O in VICE', indicator='<inner> in <outer_left><outer_right>', outer_left='V', outer_right='ICE', inner='O', answer='VOICE')
   
    >>> Container('CAMUS banks P', '<outer_left><outer_right> banks <inner>', 'CAM', 'US', 'P', 'CAMPUS')
    Container(clue='CAMUS banks P', indicator='<outer_left><outer_right> banks <inner>', outer_left='CAM', outer_right='US', inner='P', answer='CAMPUS')
    
    >>> Container('Incorrect container', '<outer_left><outer_right> contains <inner>', 'OU', 'T', 'IN', 'WRONG')
    Traceback (most recent call last):
    ...
    ValueError: Indicator must match: clue: "Incorrect container", indicator: "<outer_left><outer_right> contains <inner>", parts: "{'outer_left': 'OU', 'outer_right': 'T', 'inner': 'IN'}", indicator replaced with parts: "OUT contains IN", got: "OUT contains IN"

    >>> Container('R in GEMS', '<inner> in <outer_left><outer_right>', 'GE', 'MS', 'R', 'GERMS')
    Container(clue='R in GEMS', indicator='<inner> in <outer_left><outer_right>', outer_left='GE', outer_right='MS', inner='R', answer='GERMS')
    """
    clue: str
    indicator: str
    outer_left: str
    outer_right: str
    inner: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the container
        check_indicator_matches(self.clue, self.indicator, {
            'outer_left': self.outer_left,
            'outer_right': self.outer_right,
            'inner': self.inner
        })
       
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is formed by putting inner between outer_left and outer_right
        expected_answer = normalize(self.outer_left + self.inner + self.outer_right)
        if normalize(self.answer) != expected_answer:
            raise ValueError(f'Answer "{self.answer}" must be formed by putting "{self.inner}" between "{self.outer_left}" and "{self.outer_right}"')

from dataclasses import dataclass
from typing import Union, Tuple, Optional
from cry_strings import *
from clue_text import *

@dataclass(frozen=True)
class Deletion(ClueType):
    """
    A deletion type clue. Letters are removed from a word or phrase to form the answer.

    Attributes:
        clue (str): The full text of the clue.
        indicator (str): The part of the clue that indicates how the deletion should be performed.
        keep (StringOrList): The part(s) of the fodder that are kept.
        delete (StringOrList): The part(s) of the fodder that are deleted.
        deletion (Optional[str]): The specific letter(s) being deleted, if mentioned in the clue.
        answer (str): The answer to the clue.

    >>> Deletion("Beheaded STAR", "Beheaded <delete><keep>", "TAR", "S", None, "TAR")
    Deletion(clue='Beheaded STAR', indicator='Beheaded <delete><keep>', keep='TAR', delete='S', deletion=None, answer='TAR')

    >>> Deletion("CRAVEN C to fly away", "<delete><keep> <deletion> to fly away", "RAVEN", "C", "C", "RAVEN")
    Deletion(clue='CRAVEN C to fly away', indicator='<delete><keep> <deletion> to fly away', keep='RAVEN', delete='C', deletion='C', answer='RAVEN')

    >>> Deletion('BOOK endlessly', "<keep><delete> endlessly", "BOO", "K", None, "BOO")
    Deletion(clue='BOOK endlessly', indicator='<keep><delete> endlessly', keep='BOO', delete='K', deletion=None, answer='BOO')

    >>> Deletion("DARLING heartlessly", "<keep><delete><keep> heartlessly", ["DAR", "ING"], "L", None, "DARING")
    Deletion(clue='DARLING heartlessly', indicator='<keep><delete><keep> heartlessly', keep=['DAR', 'ING'], delete='L', deletion=None, answer='DARING')

    >>> Deletion("Invalid STAR", "<keep><delete>", "TAR", ["S", "X"], None, "TA")
    Traceback (most recent call last):
    ...
    ValueError: Number of occurrences of <delete> (1) does not match the number of substitutions (2)

    >>> Deletion("Mismatched CRAVEN", "<keep><delete> <deletion> away", "RAVEN", "C", "X", "RAVEN")
    Traceback (most recent call last):
    ...
    ValueError: Indicator must match: clue: "Mismatched CRAVEN", indicator: "<keep><delete> <deletion> away", parts: "{'keep': 'RAVEN', 'delete': 'C', 'deletion': 'X'}", indicator replaced with parts: "RAVENC X away", got: "RAVENC X away"
    """
    clue: str
    indicator: str
    keep: StringOrList
    delete: StringOrList
    deletion: Optional[str]
    answer: str

    def __post_init__(self):
        # Validate the indicator
        parts = {'keep': self.keep, 'delete': self.delete}
        if self.deletion:
            parts['deletion'] = self.deletion
        check_indicator_matches(self.clue, self.indicator, parts)

        # Validate the answer
        check_answer(self.answer)

        # Validate the deletion operation
        expected_answer = ''.join(self.keep) if isinstance(self.keep, list) else self.keep
        if not equals_normalized(expected_answer, self.answer):
            raise ValueError(f'The answer "{self.answer}" does not match the kept parts: "{self.keep}"')

        # Validate the specified deletion (if provided)
        if self.deletion:
            actual_delete = ''.join(self.delete) if isinstance(self.delete, list) else self.delete
            if not equals_normalized(actual_delete, self.deletion):
                raise ValueError(f'The specified deletion "{self.deletion}" does not match the actual deleted part "{self.delete}"')

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
    ValueError: Indicator must match: clue: "Incorrect hidden clue", indicator: "<left><hidden><right> hides", parts: "{'left': 'Inc', 'hidden': 'orrect', 'right': ' hidden clue'}", indicator replaced with parts: "Incorrect hidden clue hides", got: "Incorrect hidden clue hides"
    """
    clue: str
    indicator: str
    left: str
    hidden: str
    right: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the hidden word
        check_indicator_matches(clue_output(self.clue), self.indicator, {'left': self.left, 'hidden': self.hidden, 'right': self.right})

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
        clue (str): The full text of the clue.
        indicator (str): The part of the clue that indicates a reversal should be performed.
        fodder (str): The word or phrase to be reversed.
        answer (str): The answer to the clue.

    >>> Reversal('Returned lager', 'Returned <fodder>', 'lager', 'REGAL')
    Reversal(clue='Returned lager', indicator='Returned <fodder>', fodder='lager', answer='REGAL')
    >>> Reversal(
    ...     Combination('Returned beer', 'Returned ', Definition('beer', 'LAGER'), '', 'Returned LAGER'),
    ...     'Returned <fodder>', 'LAGER', 'REGAL')
    Reversal(clue=Combination(input='Returned beer', prefix='Returned ', combined=Definition(clue='beer', answer='LAGER'), suffix='', output='Returned LAGER'), indicator='Returned <fodder>', fodder='LAGER', answer='REGAL')
    >>> Reversal('Returned lager', 'Returned <fodder>', 'lager', 'ALGAE')
    Traceback (most recent call last):
    ...
    ValueError: Answer "ALGAE" must be a reversal of "lager"
    """
    clue: str
    indicator: str
    fodder: str
    answer: str

    def __post_init__(self):
        # Validate that the indicator matches the clue and produces the fodder
        check_indicator_matches(clue_output(self.clue), self.indicator, {'fodder': self.fodder})
       
        # Validate that the answer is in the correct format
        check_answer(self.answer)
        
        # Validate that the answer is a reversal of the fodder
        if normalize(self.fodder)[::-1] != self.answer:
            raise ValueError(f'Answer "{self.answer}" must be a reversal of "{self.fodder}"')
        
        # This is a simple check to ensure the answer is a valid word
        # In a real system, you'd want to check against a dictionary
        if len(self.answer) < 2:
            raise ValueError(f'Answer "{self.answer}" must be a valid word')