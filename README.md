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

## License

This project is released under the [MIT License](LICENSE).