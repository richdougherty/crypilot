import re

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

def check_answer(s: str) -> bool:
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

def normalize_answer(s: str) -> str:
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
    >>> is_answer_pattern('Hello world')
    False
    >>> is_answer_pattern('ABC!')
    False
    """
    return re.match(r'^[A-Z_ \-]+$', s) is not None

def check_answer_pattern(s: str) -> bool:
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

def answer_matches_pattern(answer: str, answer_pattern: str):
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
    # Normalize the answer by removing non-alphabetic characters
    clean_answer = ''.join(c for c in answer if c.isalpha())
    
    # Create a regex pattern from the answer_pattern
    pattern = answer_pattern.replace('_', '.').replace(' ', r'\s*').replace('-', r'-?')
    pattern = f'^{pattern}$'
    
    # Match the clean answer against the pattern
    return bool(re.match(pattern, clean_answer, re.IGNORECASE))

def indicator_clue(indicator: str, parts: dict[str, str]) -> bool:
    """
    Gets the clue for an indicator by substituting the parts.

    Args:
        indicator (str): The indicator string with placeholders.
        parts (dict[str, str]): A dictionary of parts to replace in the indicator.
                                A value of None for a part indicates it should be
                                skipped.

    Returns:
        str: The clue

    Raises:
        ValueError: If a bracketed key in the indicator is not found in the parts dictionary.

    >>> indicator_clue('shredded <fodder>', { 'fodder': 'corset' })
    'shredded corset'
    >>> indicator_clue(
    ...     '<left><right> outside of <middle>',
    ...     {
    ...         'left': 'P',
    ...         'right': 'AL',
    ...         'middle': 'U'
    ...     }
    ... )
    'PAL outside of U'
    >>> indicator_clue('mixed up <fodder>', { 'fodder': 'clues' })
    'mixed up clues'
    >>> indicator_clue('<fodder> shaken up', { 'fodder': 'word' })
    'word shaken up'
    """
    replaced_indicator = indicator
    for key, value in parts.items():
        if value is None:
            # A value of None indicates that the <key> is not present
            # This can be used to have variations on common patterns, but
            # exclude some parts for them. E.g. a hidden clue with no
            # <left>, only a <hidden> and <right>.
            continue
        bracketed_key = f'<{key}>'
        if bracketed_key not in replaced_indicator:
            raise ValueError(f"Bracketed key '{bracketed_key}' not found in indicator")
        replaced_indicator = replaced_indicator.replace(bracketed_key, value, 1)
    return replaced_indicator

def check_indicator_matches(clue: str, indicator: str, parts: dict[str, str]) -> None:
    """
    Checks if an indicator string when applied to the given parts
    produces the given clue. Raises a ValueError with diagnostic information if not.

    Args:
        clue (str): The original clue string.
        indicator (str): The indicator string with placeholders.
        parts (dict[str, str]): A dictionary of parts to replace in the indicator.
                                A value of None for a part indicates it should be
                                skipped.

    Raises:
        ValueError: If the indicator doesn't match the clue after replacements,
                    with detailed diagnostic information.

    >>> check_indicator_matches('shredded corset', 'shredded <anagram>', { 'anagram': 'corset' })
    >>> check_indicator_matches('shredded pickle', 'shredded <anagram>', { 'anagram': 'corset' })
    Traceback (most recent call last):
    ...
    ValueError: Indicator must match: clue: "shredded pickle", indicator: "shredded <anagram>", parts: "{'anagram': 'corset'}", indicator replaced with parts: "shredded corset"
    >>> check_indicator_matches('PAL outside of U', '<left><right> outside of <middle>', {'left': 'P', 'right': 'AL', 'middle': 'U'})
    >>> check_indicator_matches('word shaken up', '<fodder> shaken up', { 'fodder': 'word' })
    """
    replaced_indicator = indicator
    for key, value in parts.items():
        if value is None:
            # A value of None indicates that the <key> is not present
            # This can be used to have variations on common patterns, but
            # exclude some parts for them. E.g. a hidden clue with no
            # <left>, only a <hidden> and <right>.
            continue
        bracketed_key = f'<{key}>'
        if bracketed_key not in replaced_indicator:
            raise ValueError(f"Bracketed key '{bracketed_key}' not found in indicator")
        replaced_indicator = replaced_indicator.replace(bracketed_key, value, 1)
    
    if not equals_normalized(replaced_indicator, clue):
        error_message = f'Indicator must match: clue: "{clue}", indicator: "{indicator}", parts: "{parts}", indicator replaced with parts: "{replaced_indicator}"'
        raise ValueError(error_message)