from typing import ForwardRef, NewType, Union, List, Dict, Optional

# Basic string types
ClueStr = NewType('ClueStr', str)
"""A string representing a cryptic crossword clue."""

AnswerStr = NewType('AnswerStr', str)
"""A string representing an answer to a cryptic crossword clue. Must be in uppercase, and may contain spaces and hyphens."""

AnswerPatternStr = NewType('AnswerPatternStr', str)
"""A string representing the pattern of an answer, using underscores for unknown letters."""

IndicatorPatternStr = NewType('IndicatorPatternStr', str)
"""A string representing the pattern of an indicator, with placeholders for variable parts."""

# ClueSources are often plain strings, but sometimes a combination clue
ClueSource = Union[ClueStr, ForwardRef('Combination')]
"""
A type representing the source of a clue, which can be either a simple string (ClueStr)
or a Combination object that combines multiple clues.
"""

# Indicator parts
IndicatorPartStr = NewType('IndicatorPartStr', str)
"""A string representing a part of an indicator."""

IndicatorPart = Union[IndicatorPartStr, Optional[IndicatorPartStr], List[IndicatorPartStr]]
"""
A type representing a part of an indicator, which can be a single string,
an optional string, or a list of strings.
"""

IndicatorParts = Dict[str, Optional[IndicatorPart]]
"""
A dictionary mapping indicator part names to their values, which can be
single strings, optional strings, or lists of strings.
"""