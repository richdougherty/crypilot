from typing import NewType, Union, List, Dict, Optional

# Basic string types
ClueStr = NewType('ClueStr', str)
AnswerStr = NewType('AnswerStr', str)
AnswerPatternStr = NewType('AnswerPatternStr', str)
IndicatorStr = NewType('IndicatorStr', str)

# Complex types
PartValue = Union[str, List[str]]
IndicatorParts = Dict[str, Optional[PartValue]]

# Type aliases
StringOrList = Union[str, List[str]]