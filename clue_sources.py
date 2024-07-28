from dataclasses import dataclass
from typing import TYPE_CHECKING
from cry_strings import equals_normalized
from cry_types import ClueSource, ClueStr

if TYPE_CHECKING:
    from clues import ClueType

@dataclass(frozen=True)
class Combination:
    """
    Represents a combination of clues or clue parts.

    Attributes:
        input (ClueStr): The original input clue text.
        prefix (ClueStr): Any text that comes before the combined clue.
        combined (ClueType): The main clue being combined.
        suffix (ClueStr): Any text that comes after the combined clue.
        output (ClueStr): The resulting output after combination.

    >>> import clues
    >>> Combination('Returned beer', 'Returned ', clues.Definition('beer', 'LAGER'), '', 'Returned LAGER')
    Combination(input='Returned beer', prefix='Returned ', combined=Definition(clue='beer', answer='LAGER'), suffix='', output='Returned LAGER')
    """
    input: ClueStr
    prefix: ClueStr
    combined: 'ClueType'
    suffix: ClueStr
    output: ClueStr

    def __post_init__(self):
        if not equals_normalized(self.input, self.prefix + self.combined.clue + self.suffix):
            raise ValueError(f'The Combination input does not match its prefix+combined.clue+suffix') # TODO: Include more info

        if not equals_normalized(self.output, self.prefix + self.combined.answer + self.suffix):
            raise ValueError(f'The Combination input does not match its prefix+combined.clue+suffix') # TODO: Include more info

def clue_input(clue: ClueSource) -> ClueStr:
    """
    >>> import clues
    >>> clue_input('hello')
    'hello'
    >>> clue_input(Combination('Foobar', 'Foo', clues.Definition('bar', 'BAX'), '', 'FooBAX'))
    'Foobar'
    """
    if isinstance(clue, ClueStr.__supertype__):
        return clue
    elif type(clue) == Combination:
        return clue.input
    else:
        raise ValueError(f'Cannot get clue input from unexpected ClueSource type: {type(clue)}')

def clue_output(clue: ClueSource) -> ClueStr:
    """
    >>> import clues
    >>> clue_output('hello')
    'hello'
    >>> clue_output(Combination('Foobar', 'Foo', clues.Definition('bar', 'BAX'), '', 'FooBAX'))
    'FooBAX'
    """
    if isinstance(clue, ClueStr.__supertype__):
        return clue
    elif type(clue) == Combination:
        return clue.output
    else:
        raise ValueError(f'Cannot get clue output from unexpected ClueSource type: {type(clue)}')