Sudoku Solver
===============
Introduction
-------------
This is a Sudoku solver that aims to solve grids without using backtracking algorithms, only deduction rules.
It assigns a difficulty to a grid depending on the variety of rules that needed to be applied in order
to solve the grid.

How to use
-----------
Put the grid that you wish to solve in the `sudoku.txt` file in the following format:
- One line per row of the grid
- Digits are separated by commas exclusively
- A zero represents an empty cell

The [QQWing website](https://qqwing.com/generate.html) is great for generating grids of varying difficulty, and permits cross-checking of the answer
given by the program.

A script to translate a QQWing grid (compact format) to the format accepted by the program is given
in `qqwing.py`; you only need to paste the QQWing grid in the `qqwing.txt` file and run `qqwing.py`.  
An example of grid is already given in both files.

Once you have the grid you wish to solve, just run `solver.py`; the result will be printed to the standard output.  
Some further input on your end may be required if the solver cannot solve the grid on its own.