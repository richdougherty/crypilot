from typing import Tuple

class CrypilotConfig:
    """
    Configuration class for Crypilot.

    Attributes:
        indicator_delims (Tuple[str, str]): A tuple of two single-character strings
            representing the opening and closing delimiters for indicators in clues.
            Default is ('<', '>').
        token_separator (str): A single-character string used as a separator for tokenization.
            Default is '|'.
    """
    def __init__(self):
        self._indicator_delims: Tuple[str, str] = ('<', '>')
        self._token_separator: str = '|'

    @property
    def indicator_delims(self) -> Tuple[str, str]:
        return self._indicator_delims

    @indicator_delims.setter
    def indicator_delims(self, value: Tuple[str, str]):
        if not isinstance(value, tuple) or len(value) != 2 or not all(isinstance(v, str) and len(v) == 1 for v in value):
            raise ValueError("indicator_delims must be a tuple of two single-character strings")
        self._indicator_delims = value

    @property
    def token_separator(self) -> str:
        return self._token_separator

    @token_separator.setter
    def token_separator(self, value: str):
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("token_separator must be a single-character string")
        self._token_separator = value

_config = CrypilotConfig()

def cry_config() -> CrypilotConfig:
    return _config