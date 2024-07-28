# Crypilot

Crypilot is a tool for precisely describing and validating cryptic
crossword clues. It's a hobby project aimed at exploring the structure
and logic behind cryptic crosswords.

## Current Features

- Data structures for representing various types of cryptic clues
  (e.g., Anagrams, Containers, Deletions, Homophones)
- Utility functions for string normalization and manipulation specific
  to cryptic crosswords
- Basic validation of clue structures and answers
- Support for combination clues and double solutions
- Type definitions for improved code clarity and consistency

## Project Structure

- [`clues.py`](./clues.py): Defines the main clue types and their structures
- [`clue_sources.py`](./clue_sources.py): Clue source text is defined here as either a plain string or the result of a combination clue
- [`cry_strings.py`](./cry_strings.py): Provides utility functions for string
manipulation and validation
- [`cry_types.py`](./cry_types.py): Contains type definitions used throughout the project
- [`solutions.py`](./solutions.py): Implements solution types, including double
  solutions

## Status

This project is in its early stages and is primarily for
experimentation and learning. It's not yet ready for practical use in
solving or generating full cryptic crosswords.

## Clue Types

Clue types represent different cryptic crossword clue structures. They are defined in [clues.py](./clues.py).

- Equivalences
  - ✅ Straight definition
  - ✅ Cryptic definition
  - ❌ Common abbreviations
  - ❌ Foreign language equivalents
  - ❌ Literary references
- Wordplay
  - ✅ Anagram
  - ❌ Charade
  - ✅ Container
  - Deletions
    - ✅ Standard deletion
    - ❌ Heads and tails (special case of deletion)
    - ❌ Outsides (inverse of hidden word)
  - Hidden
    - ✅ Standard hidden word
    - ❌ Initial or final letters
    - ❌ Odd or even letters
  - ✅ Homophone
  - ❌ Letter bank
  - ❌ Palindrome
  - ✅ Reversal
  - ❌ Spoonerism

## Solution Types

Solution types represent ways to combine clues into full solutions. They are defined in [solutions.py](./solutions.py).

- Split
  - ✅ Standard solution
  - ✅ Double Definition
  - ❌ Triple Solution (and higher multiples)
- All
  - ❌ &lit. (And Literally So)
  - ❌ Semi-&lit.
- ❌ Cryptic definition

## Composition Types

Composition types are used to construct more complex clues and solutions. They are defined in [clue_sources.py](./clue_sources.py).

- ✅ Combination
- ❌ Ignored words

## Configuration

Crypilot behaviour can be configured by changing settings on the [cry_config()](./cry_config.py) object.

- `indicator_delims`: Customize the delimiters used for indicators in clues. Default is `('<', '>')`.

## License

This project is released under the [MIT License](LICENSE).