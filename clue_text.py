from dataclasses import dataclass
from typing import Union
from cryptic_strings import *
import clues

ClueText = Union[str, 'Combination']

@dataclass(frozen=True)
class Combination:
    """
    >>> Combination('Returned beer', 'Returned ', clues.Definition('beer', 'LAGER'), '', 'Returned LAGER')
    Combination(input='Returned beer', prefix='Returned ', combined=Definition(clue='beer', answer='LAGER'), suffix='', output='Returned LAGER')
    """
    input: 'ClueText'
    prefix: str
    combined: 'clues.ClueType'
    suffix: str
    output: str

    def __post_init__(self):
        if not equals_normalized(self.input, self.prefix + self.combined.clue + self.suffix):
            raise ValueError(f'The Combination input does not match its prefix+combined.clue+suffix') # TODO: Include more info

        if not equals_normalized(self.output, self.prefix + self.combined.answer + self.suffix):
            raise ValueError(f'The Combination input does not match its prefix+combined.clue+suffix') # TODO: Include more info

def clue_input(clue: ClueText) -> str:
    """
    >>> clue_input('hello')
    'hello'
    >>> clue_input(Combination('Foobar', 'Foo', clues.Definition('bar', 'BAX'), '', 'FooBAX'))
    'Foobar'
    """
    if type(clue) == str:
        return clue
    elif type(clue) == Combination:
        return clue.input

def clue_output(clue: ClueText) -> str:
    """
    >>> clue_output('hello')
    'hello'
    >>> clue_output(Combination('Foobar', 'Foo', clues.Definition('bar', 'BAX'), '', 'FooBAX'))
    'FooBAX'
    """
    if type(clue) == str:
        return clue
    elif type(clue) == Combination:
        return clue.output