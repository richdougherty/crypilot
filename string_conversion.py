from typing import Callable, List, Optional, Union
from cry_types import (
    ClueStr, AnswerStr, AnswerPatternStr, ClueSource,
    IndicatorPatternStr, IndicatorPartStr, IndicatorPart
)
from clue_sources import Combination

class StringConversion:
    """
    A class for converting various string types used in the Crypilot project.

    >>> identity_conv = StringConversion(lambda x: x)
    >>> upper_conv = StringConversion(str.upper)
    >>> lower_conv = StringConversion(str.lower)

    >>> identity_conv.convert_clue_str(ClueStr("Some Clue"))
    'Some Clue'
    >>> upper_conv.convert_clue_str(ClueStr("Some Clue"))
    'SOME CLUE'
    >>> lower_conv.convert_clue_str(ClueStr("Some Clue"))
    'some clue'

    >>> identity_conv.convert_answer_str(AnswerStr("ANSWER"))
    'ANSWER'
    >>> lower_conv.convert_answer_str(AnswerStr("ANSWER"))
    'answer'

    >>> identity_conv.convert_answer_pattern_str(AnswerPatternStr("A__W__"))
    'A__W__'
    >>> upper_conv.convert_answer_pattern_str(AnswerPatternStr("a__w__"))
    'A__W__'

    >>> identity_conv.convert_clue_source(ClueStr("Some Clue"))
    'Some Clue'
    >>> upper_conv.convert_clue_source(ClueStr("Some Clue"))
    'SOME CLUE'
    >>> from clues import Definition
    >>> combo = Combination("Test Combo", "Test ", Definition("Combo", "COMBO"), "", "Test COMBO")
    >>> identity_conv.convert_clue_source(combo) == combo
    True

    >>> identity_conv.convert_indicator_pattern_str(IndicatorPatternStr("<left><right>"))
    '<left><right>'
    >>> upper_conv.convert_indicator_pattern_str(IndicatorPatternStr("<left><right>"))
    '<LEFT><RIGHT>'

    >>> identity_conv.convert_indicator_part_str(IndicatorPartStr("part"))
    'part'
    >>> upper_conv.convert_indicator_part_str(IndicatorPartStr("part"))
    'PART'

    >>> identity_conv.convert_indicator_part(IndicatorPartStr("part"))
    'part'
    >>> upper_conv.convert_indicator_part(IndicatorPartStr("part"))
    'PART'
    >>> lower_conv.convert_indicator_part(["PART1", "PART2"])
    ['part1', 'part2']
    >>> identity_conv.convert_indicator_part(None) is None
    True

    >>> parts = {"left": "LEFT", "right": ["RIGHT1", "RIGHT2"], "middle": None}
    >>> identity_conv.convert_indicator_parts(parts) == parts
    True
    >>> upper_conv.convert_indicator_parts(parts)
    {'left': 'LEFT', 'right': ['RIGHT1', 'RIGHT2'], 'middle': None}
    >>> lower_conv.convert_indicator_parts(parts)
    {'left': 'left', 'right': ['right1', 'right2'], 'middle': None}
    """
    def __init__(self, convert_str: Callable[[str], str]):
        self.convert_str = convert_str

    def convert_clue_str(self, value: ClueStr) -> ClueStr:
        return ClueStr(self.convert_str(value))

    def convert_answer_str(self, value: AnswerStr) -> AnswerStr:
        return AnswerStr(self.convert_str(value))

    def convert_answer_pattern_str(self, value: AnswerPatternStr) -> AnswerPatternStr:
        return AnswerPatternStr(self.convert_str(value))

    def convert_clue_source(self, value: ClueSource) -> ClueSource:
        if isinstance(value, Combination):
            return value
        return self.convert_clue_str(value)

    def convert_indicator_pattern_str(self, value: IndicatorPatternStr) -> IndicatorPatternStr:
        return IndicatorPatternStr(self.convert_str(value))

    def convert_indicator_part_str(self, value: IndicatorPartStr) -> IndicatorPartStr:
        return IndicatorPartStr(self.convert_str(value))

    def convert_indicator_part(self, value: IndicatorPart) -> IndicatorPart:
        if value is None:
            return None
        elif isinstance(value, str):
            return self.convert_indicator_part_str(value)
        elif isinstance(value, list):
            return [self.convert_indicator_part_str(item) for item in value]
        else:
            raise TypeError(f"Unsupported IndicatorPart type: {type(value)}")

    def convert_indicator_parts(self, parts: dict[str, Optional[IndicatorPart]]) -> dict[str, Optional[IndicatorPart]]:
        return {key: self.convert_indicator_part(value) for key, value in parts.items()}