from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from cry_strings import *
from clue_sources import *

if TYPE_CHECKING:
    from clue_sources import Combination

class ClueType:
    """
    Base class of all clue types. All clues have the form
    SomeClueType(clue: ClueSource, ..., answer: AnswerStr)

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        answer (AnswerStr): The answer to the clue.

    >>> @dataclass
    ... class SimpleClue(ClueType):
    ...     clue: ClueSource
    ...     answer: AnswerStr
    >>> SimpleClue("Valid clue", "ANSWER")
    SimpleClue(clue='Valid clue', answer='ANSWER')
    >>> SimpleClue("Invalid <clue>", "ANSWER")
    Traceback (most recent call last):
    ...
    ValueError: "Invalid <clue>" is not a valid clue: contains indicator delimiters < or >
    >>> SimpleClue("Valid clue", "invalid answer")
    Traceback (most recent call last):
    ...
    ValueError: "invalid answer" must be in "answer" form: only uppercase, spaces and hyphens
    """
    clue: ClueSource
    answer: AnswerStr

    def __post_init__(self):
        check_clue(clue_input(self.clue))
        check_answer(self.answer)

    def check_indicator_matches(self, parts: dict[str, Optional[IndicatorPart]]):
        check_indicator_matches(clue_output(self.clue), self.indicator, parts)

    def check_normalized_equal(self, a: str, b: str, error_message: str):
        if not equals_normalized(a, b):
            raise ValueError(error_message)

@dataclass(frozen=True)
class Anagram(ClueType):
    """
    An anagram type clue. The clue contains a word or phrase that can be
    rearranged to form the answer.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        indicator (IndicatorPatternStr): The part of the clue that indicates an anagram should be performed.
        fodder (IndicatorPartStr): The word or phrase to be anagrammed.
        answer (AnswerStr): The answer to the clue.

    >>> Anagram('shredded corset', 'shredded <fodder>', 'corset', 'ESCORT')
    Anagram(clue='shredded corset', indicator='shredded <fodder>', fodder='corset', answer='ESCORT')
    >>> Anagram('Mixed up clue', 'Mixed up <fodder>', 'clue', 'ANSWER')
    Traceback (most recent call last):
    ...
    ValueError: Answer "ANSWER" must be an anagram of "clue"
    """
    clue: ClueSource
    indicator: IndicatorPatternStr
    fodder: IndicatorPartStr
    answer: AnswerStr

    def __post_init__(self):
        super().__post_init__()

        # Validate that the indicator matches the clue and produces the fodder
        self.check_indicator_matches({'fodder': self.fodder})

        # Validate that the answer is an anagram of the fodder
        self.check_normalized_equal(
            ''.join(sorted(normalize(self.fodder))),
            ''.join(sorted(self.answer)),
            f'Answer "{self.answer}" must be an anagram of "{self.fodder}"'
        )

@dataclass(frozen=True)
class Container(ClueType):
    """
    A container type clue. One set of letters is placed inside another.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        indicator (IndicatorPatternStr): The part of the clue that indicates a container should be formed.
        outer_left (IndicatorPartStr): The left part of the word or phrase that forms the outer part of the container.
        outer_right (IndicatorPartStr): The right part of the word or phrase that forms the outer part of the container.
        inner (IndicatorPartStr): The word or phrase to be placed inside the outer parts.
        answer (AnswerStr): The answer to the clue.

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
    clue: ClueSource
    indicator: IndicatorPatternStr
    outer_left: IndicatorPartStr
    outer_right: IndicatorPartStr
    inner: IndicatorPartStr
    answer: AnswerStr

    def __post_init__(self):
        super().__post_init__()

        # Validate that the indicator matches the clue and produces the container
        self.check_indicator_matches({
            'outer_left': self.outer_left,
            'outer_right': self.outer_right,
            'inner': self.inner
        })

        # Validate that the answer is formed by putting inner between outer_left and outer_right
        expected_answer = normalize(self.outer_left + self.inner + self.outer_right)
        self.check_normalized_equal(
            self.answer,
            expected_answer,
            f'Answer "{self.answer}" must be formed by putting "{self.inner}" between "{self.outer_left}" and "{self.outer_right}"'
        )

@dataclass(frozen=True)
class Deletion(ClueType):
    """
    A deletion type clue. Letters are removed from a word or phrase to form the answer.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        indicator (IndicatorPatternStr): The part of the clue that indicates how the deletion should be performed.
        keep (IndicatorPart): The part(s) of the fodder that are kept.
        delete (IndicatorPart): The part(s) of the fodder that are deleted.
        deletion (Optional[IndicatorPartStr]): The specific letter(s) being deleted, if mentioned in the clue.
        answer (AnswerStr): The answer to the clue.

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
    clue: ClueSource
    indicator: IndicatorPatternStr
    keep: IndicatorPart
    delete: IndicatorPart
    deletion: Optional[IndicatorPartStr]
    answer: AnswerStr

    def __post_init__(self):
        super().__post_init__()

        # Validate the indicator
        self.check_indicator_matches({'keep': self.keep, 'delete': self.delete, 'deletion': self.deletion})

        # Validate the deletion operation
        expected_answer = ''.join(self.keep) if isinstance(self.keep, list) else self.keep
        self.check_normalized_equal(
            expected_answer,
            self.answer,
            f'The answer "{self.answer}" does not match the kept parts: "{self.keep}"'
        )

        # Validate the specified deletion (if provided)
        if self.deletion:
            actual_delete = ''.join(self.delete) if isinstance(self.delete, list) else self.delete
            self.check_normalized_equal(
                actual_delete,
                self.deletion,
                f'The specified deletion "{self.deletion}" does not match the actual deleted part "{self.delete}"'
            )

@dataclass(frozen=True)
class Definition(ClueType):
    """
    A definition type clue. This is the simplest form of clue where the clue
    directly defines the answer.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        answer (AnswerStr): The answer to the clue.

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
    clue: ClueSource
    answer: AnswerStr

    def __post_init__(self):
        # Validate that the answer is in the correct format
        check_answer(self.answer)

@dataclass(frozen=True)
class Hidden(ClueType):
    """
    A hidden word type clue. The answer is hidden within the clue text.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        indicator (IndicatorPatternStr): The part of the clue that indicates a hidden word.
        left (IndicatorPartStr): The text before the hidden word.
        hidden (IndicatorPartStr): The hidden word (the answer).
        right (IndicatorPartStr): The text after the hidden word.
        answer (AnswerStr): The answer to the clue.

    >>> Hidden('Found ermine, deer hides', '<left><hidden><right> hides', 'Found ', 'ermine, d', 'eer', 'ERMINED')
    Hidden(clue='Found ermine, deer hides', indicator='<left><hidden><right> hides', left='Found ', hidden='ermine, d', right='eer', answer='ERMINED')
    >>> Hidden('Introduction to do-gooder', 'Introduction to <hidden><right>', None, 'do-g', 'ooder', 'DOG')
    Hidden(clue='Introduction to do-gooder', indicator='Introduction to <hidden><right>', left=None, hidden='do-g', right='ooder', answer='DOG')
    >>> Hidden('Incorrect hidden clue', '<left><hidden><right> hides', 'Inc', 'orrect', ' hidden clue', 'WRONG')
    Traceback (most recent call last):
    ...
    ValueError: Indicator must match: clue: "Incorrect hidden clue", indicator: "<left><hidden><right> hides", parts: "{'left': 'Inc', 'hidden': 'orrect', 'right': ' hidden clue'}", indicator replaced with parts: "Incorrect hidden clue hides", got: "Incorrect hidden clue hides"
    """
    clue: ClueSource
    indicator: IndicatorPatternStr
    left: IndicatorPartStr
    hidden: IndicatorPartStr
    right: IndicatorPartStr
    answer: AnswerStr

    def __post_init__(self):
        super().__post_init__()

        # Validate that the indicator matches the clue and produces the hidden word
        self.check_indicator_matches({'left': self.left, 'hidden': self.hidden, 'right': self.right})

        # Validate that the hidden word produces the answer
        self.check_normalized_equal(
            self.hidden,
            self.answer,
            f'Hidden word "{self.hidden}" must produce answer "{self.answer}"'
        )

@dataclass(frozen=True)
class Homophone(ClueType):
    """
    A homophone type clue. The answer sounds like another word or phrase in the clue.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        indicator (IndicatorPatternStr): The part of the clue that indicates a homophone should be used.
        sound_alike (IndicatorPartStr): The word or phrase that sounds like the answer.
        answer (AnswerStr): The answer to the clue.

    >>> from clues import *

    >>> Homophone(
    ...     Combination('We hear twins', 'We hear ', Definition('twins', 'PAIR'), '', 'We hear PAIR'),
    ...     'We hear <sound_alike>',
    ...     'PAIR',
    ...     'PARE'
    ... )
    Homophone(clue=Combination(input='We hear twins', prefix='We hear ', combined=Definition(clue='twins', answer='PAIR'), suffix='', output='We hear PAIR'), indicator='We hear <sound_alike>', sound_alike='PAIR', answer='PARE')

    >>> Homophone(
    ...     Combination('Reportedly, couple', 'Reportedly, ', Definition('couple', 'PAIR'), '', 'Reportedly, PAIR'),
    ...     'Reportedly, <sound_alike>',
    ...     'PAIR',
    ...     'PARE'
    ... )
    Homophone(clue=Combination(input='Reportedly, couple', prefix='Reportedly, ', combined=Definition(clue='couple', answer='PAIR'), suffix='', output='Reportedly, PAIR'), indicator='Reportedly, <sound_alike>', sound_alike='PAIR', answer='PARE')

    >>> Homophone(
    ...     'Incorrect sound',
    ...     'Incorrect <sound_alike>',
    ...     'bear',
    ...     'BEER'
    ... )
    Traceback (most recent call last):
    ...
    ValueError: Indicator must match: clue: "Incorrect sound", indicator: "Incorrect <sound_alike>", parts: "{'sound_alike': 'bear'}", indicator replaced with parts: "Incorrect bear", got: "Incorrect bear"
    """
    clue: ClueSource
    indicator: IndicatorPatternStr
    sound_alike: IndicatorPartStr
    answer: AnswerStr

    def __post_init__(self):
        super().__post_init__()

        # Validate that the indicator matches the clue and produces the sound-alike word
        self.check_indicator_matches({'sound_alike': self.sound_alike})

        # Note: We can't programmatically verify that the sound_alike actually sounds like the answer.
        # This would require a pronunciation database or API, which is beyond the scope of this implementation.
        # Instead, we rely on the clue setter to ensure the homophone is valid.

@dataclass(frozen=True)
class Reversal(ClueType):
    """
    A reversal type clue. The answer is formed by reversing a word or phrase in the clue.

    Attributes:
        clue (ClueSource): The clue text, either a string or a Combination.
        indicator (IndicatorPatternStr): The part of the clue that indicates a reversal should be performed.
        fodder (IndicatorPartStr): The word or phrase to be reversed.
        answer (AnswerStr): The answer to the clue.

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
    clue: ClueSource
    indicator: IndicatorPatternStr
    fodder: IndicatorPartStr
    answer: AnswerStr

    def __post_init__(self):
        super().__post_init__()

        # Validate that the indicator matches the clue and produces the fodder
        self.check_indicator_matches({'fodder': self.fodder})

        # Validate that the answer is a reversal of the fodder
        self.check_normalized_equal(
            normalize(self.fodder)[::-1],
            self.answer,
            f'Answer "{self.answer}" must be a reversal of "{self.fodder}"'
        )