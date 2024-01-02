## Crossword Puzzle Generator

## Overview

This project is a Python-based crossword puzzle generator that models the crossword as a constraint satisfaction problem (CSP). It takes a structured grid and a list of words, and fills the grid with the words by choosing which words should go in each vertical or horizontal sequence of squares while satisfying all constraints.

## Features

- **Constraint Satisfaction**: Implements CSP to fill crossword puzzles.
- **Node Consistency**: Ensures all words in a variable's domain match the variable's length.
- **Arc Consistency**: Ensures that for every pair of neighboring variables, each value in the domain of one variable has a corresponding value in the domain of the other variable.
- **Backtracking Search**: Employs backtracking to find a complete, satisfactory assignment of variables to values.

## Structure

The project is divided into two main Python files:

- `crossword.py`: Defines `Variable` and `Crossword` classes to represent the puzzle structure.
- `generate.py`: Contains the `CrosswordCreator` class with methods to generate the puzzle.

## Classes

### `Crossword`

- Reads puzzle structure and word list files.
- Stores puzzle dimensions, structure, word list, variables, and overlaps.
- Provides functionality to determine neighbors for a given variable.

### `Variable`

- Represents a sequence of squares in the crossword puzzle.
- Defined by its starting row (`i`), starting column (`j`), direction (`ACROSS` or `DOWN`), and length.

### `CrosswordCreator`

- Holds a `crossword` object and manages domains for each variable.
- Implements functions to enforce consistency and generate the puzzle.

## Getting Started

To use the crossword puzzle generator:

1. Ensure you have Python 3.6 or higher installed.
2. Clone the repository or download the source code.
3. Install the Pillow library to handle image creation: `pip3 install pillow`
4. Run the `generate.py` script with the structure file, word list file, and optional output file name: `python generator.py data/structure1.txt data/words1.txt output.png`


## Usage

The entry point of the crossword puzzle generator is in the `generate.py` script, which you can run as a command-line tool as shown in the Getting Started section.

---

