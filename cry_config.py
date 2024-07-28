# cry_config.py

from typing import Tuple

class CrypilotConfig:
    """
    Configuration class for Crypilot.

    Attributes:
        indicator_delims (Tuple[str, str]): A tuple of two single-character strings
            representing the opening and closing delimiters for indicators in clues.
            Default is ('<', '>').
    """
    def __init__(self):
        self._indicator_delims: Tuple[str, str] = ('<', '>')

    @property
    def indicator_delims(self) -> Tuple[str, str]:
        return self._indicator_delims

    @indicator_delims.setter
    def indicator_delims(self, value: Tuple[str, str]):
        if not isinstance(value, tuple) or len(value) != 2 or not all(isinstance(v, str) and len(v) == 1 for v in value):
            raise ValueError("indicator_delims must be a tuple of two single-character strings")
        self._indicator_delims = value

_config = CrypilotConfig()

def cry_config() -> CrypilotConfig:
    return _config