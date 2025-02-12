import re
import string
from typing import Optional
from cry_config import cry_config
from cry_types import *

def normalize(s: str) -> str:
    """
    Converts a string to its normalized form: uppercase with spaces and
    punctuation removed. This is how letters are typically treated in a
    crossword.

    Args:
        s (str): The input string to normalize.

    Returns:
        str: The normalized string.

    >>> normalize('Hello world!')
    'HELLOWORLD'
    >>> normalize('Cryptic-Puzzle 123')
    'CRYPTICPUZZLE123'
    >>> normalize('A B C')
    'ABC'
    >>> normalize('')
    ''
    """
    return ''.join(c.upper() for c in s if c.isalnum())

def equals_normalized(a: str, b: str) -> bool:
    """
    Checks if the normalized forms of two strings are equal.

    Args:
        a (str): The first string to compare.
        b (str): The second string to compare.

    Returns:
        bool: True if the normalized forms are equal, False otherwise.

    >>> equals_normalized('Hello world!', 'HELLOWORLD')
    True
    >>> equals_normalized('Cryptic-Puzzle', 'cryptic puzzle')
    True
    >>> equals_normalized('ABC', 'abc')
    True
    >>> equals_normalized('ABC', 'DEF')
    False
    """
    return normalize(a) == normalize(b)

def is_normalized(s: str) -> bool:
    """
    Checks if a string is already in its normalized form.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is in normalized form, False otherwise.

    >>> is_normalized('HELLOWORLD')
    True
    >>> is_normalized('HelloWorld')
    False
    >>> is_normalized('HELLO-WORLD')
    False
    >>> is_normalized('ABC123')
    True
    """
    return s == normalize(s)

def check_normalized(s: str) -> bool:
    """
    Checks if a string is in normalized form and raises an error if it's not.

    Args:
        s (str): The string to check.

    Raises:
        ValueError: If the string is not in normalized form.

    >>> check_normalized('HELLOWORLD')
    >>> check_normalized('HelloWorld')
    Traceback (most recent call last):
    ...
    ValueError: "HelloWorld" must be in normalized form
    """
    if not is_normalized(s):
        raise ValueError(f'"{s}" must be in normalized form')

def is_clue(s: str) -> bool:
    """
    Checks if a string is a valid clue (doesn't contain indicator delimiters).

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a valid clue, False otherwise.

    >>> is_clue("This is a valid clue")
    True
    >>> is_clue("This is <not> a valid clue")
    False
    """
    start, end = cry_config().indicator_delims
    return start not in s and end not in s

def check_clue(s: ClueStr) -> None:
    """
    Checks if a string is a valid clue and raises an error if it's not.

    Args:
        s (ClueStr): The string to check.

    Raises:
        ValueError: If the string is not a valid clue.

    >>> check_clue("This is a valid clue")
    >>> check_clue("This is <not> a valid clue")
    Traceback (most recent call last):
    ...
    ValueError: "This is <not> a valid clue" is not a valid clue: contains indicator delimiters < or >

    >>> from cry_config import cry_config
    >>> original_delims = cry_config().indicator_delims
    >>> cry_config().indicator_delims = ('[', ']')
    >>> check_clue("This is now a <valid> clue")
    >>> check_clue("This is [not] a valid clue")
    Traceback (most recent call last):
    ...
    ValueError: "This is [not] a valid clue" is not a valid clue: contains indicator delimiters [ or ]
    >>> cry_config().indicator_delims = original_delims
    """
    if not is_clue(s):
        start, end = cry_config().indicator_delims
        raise ValueError(f'"{s}" is not a valid clue: contains indicator delimiters {start} or {end}')

def is_answer(s: str) -> bool:
    """
    Checks if a string is in valid answer form: only uppercase letters, spaces, and hyphens.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is in valid answer form, False otherwise.

    >>> is_answer('HELLO WORLD')
    True
    >>> is_answer('HELLO-WORLD')
    True
    >>> is_answer('Hello World')
    False
    >>> is_answer('HELLO_WORLD')
    False
    """
    return re.match(r'^[A-Z \-]+$', s) is not None

def check_answer(s: AnswerStr) -> bool:
    """
    Checks if a string is in valid answer form and raises an error if it's not.

    Args:
        s (str): The string to check.

    Raises:
        ValueError: If the string is not in valid answer form.

    >>> check_answer('HELLO WORLD')
    >>> check_answer('Hello World')
    Traceback (most recent call last):
    ...
    ValueError: "Hello World" must be in "answer" form: only uppercase, spaces and hyphens
    """
    if not is_answer(s):
        raise ValueError(f'"{s}" must be in "answer" form: only uppercase, spaces and hyphens')

def normalize_answer(s: AnswerStr) -> str:
    """
    Normalizes an answer string by removing spaces and hyphens.

    Args:
        s (str): The answer string to normalize.

    Returns:
        str: The normalized answer string.

    Raises:
        ValueError: If the input is not in valid answer form.

    >>> normalize_answer('HELLO WORLD')
    'HELLOWORLD'
    >>> normalize_answer('HELLO-WORLD')
    'HELLOWORLD'
    >>> normalize_answer('Hello World')
    Traceback (most recent call last):
    ...
    ValueError: Answers "Hello World" must be only capitals, spaces and hyphens
    """
    if not is_answer(s):
        raise ValueError(f'Answers "{s}" must be only capitals, spaces and hyphens')
    return ''.join(c.upper() for c in s if c.isalpha())

def is_answer_pattern(s: str) -> bool:
    """
    Checks if a string is a valid answer pattern: uppercase letters, underscores,
    spaces, and hyphens.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a valid answer pattern, False otherwise.

    >>> is_answer_pattern("_____")
    True
    >>> is_answer_pattern("__-__")
    True
    >>> is_answer_pattern("U_-O_")
    True
    >>> is_answer_pattern("UH-OH")
    True
    >>> is_answer_pattern("U|H|-|O|H")
    True
    >>> is_answer_pattern('Hello world')
    False
    >>> is_answer_pattern('ABC!')
    True
    >>> is_answer_pattern('123')
    False
    >>> is_answer_pattern('A\\nB')
    False
    """
    return re.match(f'^[A-Z_ {re.escape(string.punctuation)}]+$', s) is not None

def check_answer_pattern(s: AnswerPatternStr) -> None:
    """
    Checks if a string is a valid answer pattern and raises an error if it's not.

    Args:
        s (str): The string to check.

    Raises:
        ValueError: If the string is not a valid answer pattern.

    >>> check_answer_pattern("_____")
    >>> check_answer_pattern("Hello world")
    Traceback (most recent call last):
    ...
    ValueError: "Hello world" must be in answer pattern form: only uppercase, spaces, hyphens and underscores
    """
    if not is_answer_pattern(s):
        raise ValueError(f'"{s}" must be in answer pattern form: only uppercase, spaces, hyphens and underscores')

def answer_matches_pattern(answer: AnswerStr, answer_pattern: AnswerPatternStr) -> bool:
    """
    Checks if an answer matches a given answer pattern.

    Args:
        answer (str): The answer to check.
        answer_pattern (str): The pattern to match against.

    Returns:
        bool: True if the answer matches the pattern, False otherwise.

    >>> answer_matches_pattern('FOO', '___')
    True
    >>> answer_matches_pattern('F-OO', '___')
    True
    >>> answer_matches_pattern('FOO', '__ _')
    True
    >>> answer_matches_pattern('FO O', '_ __')
    True
    >>> answer_matches_pattern('FO-O', '_-_-_')
    True
    >>> answer_matches_pattern('FOO', '__ _')
    True
    >>> answer_matches_pattern('FOO', '_')
    False
    >>> answer_matches_pattern('FOO', '_____')
    False
    >>> answer_matches_pattern('FOO', 'F__')
    True
    >>> answer_matches_pattern('FOO', 'X__')
    False
    >>> answer_matches_pattern('FOO', '_OO')
    True
    """
    check_answer(answer)
    check_answer_pattern(answer_pattern)
    # Normalize the answer pattern by removing everything except
    # Normalize the answer by removing non-alphabetic characters
    clean_answer_pattern = re.sub('[^A-Z_]+', '', answer_pattern)
    clean_answer = re.sub('[^A-Z]+', '', answer)

    # Create a regex pattern from the answer_pattern
    answer_pattern_regex = clean_answer_pattern.replace('_', '.')
    answer_pattern_regex = f'^{answer_pattern_regex}$'

    # Match the clean answer against the pattern
    return bool(re.match(answer_pattern_regex, clean_answer, re.IGNORECASE))

def indicator_matches(clue: ClueStr, indicator: IndicatorPatternStr, parts: IndicatorParts) -> bool:
    """
    Confirms whether an indicator string when applied to the given parts
    produces the given results.

    Args:
        clue (ClueStr): The original clue string.
        indicator (IndicatorPatternStr): The indicator string with placeholders.
        parts (IndicatorParts): A dictionary of parts to replace in the indicator.
                                A value of None for a part indicates it should be
                                skipped. A list indicates multiple substitutions.

    Returns:
        bool: True if the indicator matches the clue after replacements, False otherwise.

    Raises:
        ValueError: If the indicator is malformed.

    >>> indicator_matches('shredded corset', 'shredded <anagram>', { 'anagram': 'corset' })
    True
    >>> indicator_matches('PAL outside of U', '<left><right> outside of <middle>', {'left': 'P', 'right': 'AL', 'middle': 'U'})
    True
    >>> indicator_matches('DARLING heartlessly', '<keep><delete><keep> heartlessly', {'keep': ['DAR', 'ING'], 'delete': 'L'})
    True
    >>> indicator_matches('Invalid STAR', '<keep><delete>', {'keep': 'TAR', 'delete': ['S', 'X']})
    Traceback (most recent call last):
    ...
    ValueError: Number of occurrences of <delete> (1) does not match the number of substitutions (2)
    """
    return _check_indicator_matches(clue, indicator, parts) is None

def check_indicator_matches(clue: ClueStr, indicator: IndicatorPatternStr, parts: IndicatorParts) -> None:
    """
    Checks if an indicator string when applied to the given parts
    produces the given clue. Raises a ValueError with diagnostic information if not.

    Args:
        clue (ClueStr): The original clue string.
        indicator (IndicatorPatternStr): The indicator string with placeholders.
        parts (IndicatorParts): A dictionary of parts to replace in the indicator.
                                A value of None for a part indicates it should be
                                skipped. A list indicates multiple substitutions.

    Raises:
        ValueError: If the indicator is malformed or doesn't match the clue after replacements,
                    with detailed diagnostic information.

    >>> check_indicator_matches('shredded corset', 'shredded <anagram>', { 'anagram': 'corset' })
    >>> check_indicator_matches('DARLING heartlessly', '<keep><delete><keep> heartlessly', {'keep': ['DAR', 'ING'], 'delete': 'L'})
    >>> check_indicator_matches('Invalid STAR', '<keep><delete>', {'keep': 'TAR', 'delete': ['S', 'X']})
    Traceback (most recent call last):
    ...
    ValueError: Number of occurrences of <delete> (1) does not match the number of substitutions (2)
    """
    error = _check_indicator_matches(clue, indicator, parts)
    if error:
        raise ValueError(error)

def _check_indicator_matches(clue: ClueStr, indicator: IndicatorPatternStr, parts: IndicatorParts) -> Optional[str]:
    """
    Checks if an indicator string when applied to the given parts
    produces the given clue. Returns None if the indicator matches,
    or an error message string if it doesn't.

    Args:
        clue (ClueStr): The original clue string.
        indicator (IndicatorPatternStr): The indicator string with placeholders.
        parts (IndicatorParts): A dictionary of parts to replace in the indicator.

    Returns:
        Optional[str]: None if the indicator matches, or an error message if it doesn't.

    Raises:
        ValueError: If the indicator is malformed (e.g., missing keys, incorrect value types).
    """
    start, end = cry_config().indicator_delims
    replaced_indicator = indicator
    for key, value in parts.items():
        if value is None:
            continue
        bracketed_key = f'{start}{key}{end}'
        if isinstance(value, str):
            if bracketed_key not in replaced_indicator:
                raise ValueError(f"Bracketed key '{bracketed_key}' not found in indicator")
            replaced_indicator = replaced_indicator.replace(bracketed_key, value, 1)
        elif isinstance(value, list):
            count = replaced_indicator.count(bracketed_key)
            if count != len(value):
                raise ValueError(f"Number of occurrences of {bracketed_key} ({count}) does not match the number of substitutions ({len(value)})")
            for sub_value in value:
                replaced_indicator = replaced_indicator.replace(bracketed_key, sub_value, 1)
        else:
            raise ValueError(f"Invalid type for key '{key}': expected str or list, got {type(value)}")

    if not equals_normalized(replaced_indicator, clue):
        return f'Indicator must match: clue: "{clue}", indicator: "{indicator}", parts: "{parts}", indicator replaced with parts: "{replaced_indicator}", got: "{replaced_indicator}"'
    return None

def split_tokens(s: str) -> str:
    """
    Splits a string into tokens, separating each character with the token separator.
    Indicator part markers are treated as single tokens.

    Args:
        s (str): The string to tokenize.

    Returns:
        str: The tokenized string.

    Raises:
        ValueError: If the input string already contains invalid token separators.

    >>> split_tokens('foo')
    'f|o|o'
    >>> split_tokens('f|o|o')
    'f|o|o'

    >>> split_tokens('f||oo')
    Traceback (most recent call last):
    ...
    ValueError: String has illegal token split, probable error: was "f||oo", expected "f|o|o"
    >>> split_tokens('f|oo')
    Traceback (most recent call last):
    ...
    ValueError: String has illegal token split, probable error: was "f|oo", expected "f|o|o"
    >>> split_tokens('f|oo|')
    Traceback (most recent call last):
    ...
    ValueError: String has illegal token split, probable error: was "f|oo|", expected "f|o|o"

    >>> split_tokens('<hello> there')
    '<hello>| |t|h|e|r|e'
    >>> split_tokens('<hello> <there>')
    '<hello>| |<there>'
    >>> split_tokens('a-b c')
    'a|-|b| |c'
    >>> split_tokens('foo <bar> baz <qux>')
    'f|o|o| |<bar>| |b|a|z| |<qux>'
    """
    #print('---s', s)
    separator = cry_config().token_separator
    start, end = cry_config().indicator_delims

    # We should accept strings with the separator provided they are already in
    # the correct form. This makes this operation idempotent. However, since
    # it's easy to make mistakes with this kind of thing we also check that the
    # provided string is correctly split into tokens, just in case.
    if separator in s:
        joined = join_tokens(s)
        expected = split_tokens(joined) # Shouldn't loop, since we've removed separators 
        if s == expected:
            return s
        else:
            raise ValueError(f'String has illegal token split, probable error: was "{s}", expected "{expected}"')

    # Split the string, keeping indicator parts together
    pattern = f'({re.escape(start)}[^{re.escape(end)}]*{re.escape(end)})'
    parts = filter(None, re.split(pattern, s))
    
    def tokenize_part(part):
        if part.startswith(start) and part.endswith(end):
            return part
        else:
            return separator.join(c for c in part)
    
    tokenized_parts = map(tokenize_part, parts)
    return separator.join(tokenized_parts)

def join_tokens(s: str) -> str:
    """
    Joins a tokenized string back into a regular string.

    Args:
        s (str): The tokenized string to join.

    Returns:
        str: The joined string.

    >>> join_tokens('f|o|o')
    'foo'
    >>> join_tokens('<hello>| |t|h|e|r|e')
    '<hello> there'
    >>> join_tokens('<hello>| |<there>')
    '<hello> <there>'
    >>> join_tokens('a|-|b| |c')
    'a-b c'
    """
    separator = cry_config().token_separator
    return s.replace(separator, '')