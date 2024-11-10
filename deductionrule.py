import functools
from abc import ABC, abstractmethod
from collections import Counter

from grid import SudokuGrid


class DeductionRule(ABC):
    """
    Abstract Base Class for Sudoku deduction rules.
    """

    def __init__(self, grid: SudokuGrid):
        self.grid = grid

    @abstractmethod
    def apply(self) -> bool:
        """
        Applies the deduction rule to the Sudoku grid.
        :return: True if the rule was applied and modified the grid, False otherwise.
        """
        raise NotImplementedError

    @classmethod
    def _get_row_candidates(cls, grid: SudokuGrid, row_index: int) -> list[list[int]]:
        return [grid.get_cell_candidates(row_index, j) for j in range(9) if grid.get_cell_candidates(row_index, j)]

    @classmethod
    def _get_col_candidates(cls, grid: SudokuGrid, col_index: int) -> list[list[int]]:
        return [grid.get_cell_candidates(j, col_index) for j in range(9) if grid.get_cell_candidates(j, col_index)]

    @classmethod
    def _get_block_candidates(cls, grid: SudokuGrid, block_index: int) -> list[list[int]]:
        return [grid.get_cell_candidates((block_index // 3) * 3 + (j // 3), (block_index % 3) * 3 + (j % 3)) for j
                in range(9) if
                grid.get_cell_candidates((block_index // 3) * 3 + (j // 3), (block_index % 3) * 3 + (j % 3))]

    @classmethod
    def _get_indices(cls, candidates_func, i, j):
        if candidates_func == cls._get_row_candidates:
            return i, j
        if candidates_func == cls._get_col_candidates:
            return j, i
        if candidates_func == cls._get_block_candidates:
            return (i // 3) * 3 + (j // 3), (i % 3) * 3 + (j % 3)


class DR1(DeductionRule):
    """
    First Deduction Rule: Naked Singles\n
    https://sudoku.com/sudoku-rules/obvious-singles/\n
    This rule checks if a cell has only one candidate value based on the numbers in its row, column, and 3x3 block.\n
    A grid that can be solved using only this rule is considered Easy.
    """

    def apply(self) -> bool:
        applied = False
        self.grid.update_candidates()

        for i in range(9):
            for j in range(9):
                candidates = self.grid.get_cell_candidates(i, j)
                if len(candidates) == 1:
                    answer = candidates.pop()
                    self.grid.set_cell(i, j, answer)
                    # print(f"Naked Single (Row: {i+1} - Column: {j+1} - Value: {answer})")
                    applied = True
        return applied


class DR2(DeductionRule):
    """
    Second Deduction Rule: Hidden Singles\n
    https://sudoku.com/sudoku-rules/hidden-singles/\n
    This rule checks if, for a given number, a cell is the only one in its row, column, or 3x3 block that has it as a candidate.\n
    A grid that cannot be solved entirely by DR1 but solved by this rule is considered Medium.
    """

    def apply(self) -> bool:
        applied = False
        self.grid.update_candidates()

        for group_index in range(9):
            applied = applied or self._apply_to_group(super()._get_row_candidates, group_index, 'row')
            applied = applied or self._apply_to_group(super()._get_col_candidates, group_index, 'column')
            applied = applied or self._apply_to_group(super()._get_block_candidates, group_index, 'block')

        return applied

    def _apply_to_group(self, candidates_func, group_index, group_type) -> bool:
        applied = False
        candidates = candidates_func(self.grid, group_index)
        if candidates:
            candidates = Counter(functools.reduce(lambda x, y: x + y, candidates))
            for candidate, count in candidates.items():
                if count == 1:
                    for element_index in range(9):
                        row_index, col_index = super()._get_indices(candidates_func, group_index, element_index)
                        if candidate in self.grid.get_cell_candidates(row_index, col_index):
                            self.grid.set_cell(row_index, col_index, candidate)
                            # print(f"Hidden single in {group_type} (Row: {row_index + 1} - Column: {col_index + 1} - Value: {candidate})")
                            self.grid.update_candidates()
                            applied = True
        return applied


class DR3(DeductionRule):
    """
    Third Deduction Rule: Naked Pairs\n
    https://sudoku.com/sudoku-rules/obvious-pairs/\n
    This rule looks for pairs of cells in the same row, column, or block that have the same two candidates.
    If found, these two candidates can be removed from all other cells in that row, column, or block.\n
    A grid that needs to use this rule to be solved is considered Hard.
    """

    def apply(self) -> bool:
        applied = False
        for group_index in range(9):
            applied = applied or self._apply_to_group(super()._get_row_candidates, group_index, "row")
            applied = applied or self._apply_to_group(super()._get_col_candidates, group_index, "column")
            applied = applied or self._apply_to_group(super()._get_block_candidates, group_index, "block")
        return applied

    def _apply_to_group(self, candidates_func, group_index: int, group_type: str) -> bool:
        applied = False
        candidates = candidates_func(self.grid, group_index)

        if candidates:
            pairs = [tuple(sorted(pair)) for pair in candidates if len(pair) == 2]
            if len(pairs) != len(set(pairs)):
                duplicates = [list(x) for n, x in enumerate(pairs) if x in pairs[:n]]
                for pair in duplicates:
                    for element_index in range(9):
                        row_index, col_index = super()._get_indices(candidates_func, group_index, element_index)
                        if self.grid.get_cell_candidates(row_index, col_index) != pair:
                            for candidate in pair:
                                if candidate in self.grid.get_cell_candidates(row_index, col_index):
                                    self.grid.get_cell_candidates(row_index, col_index).remove(candidate)
                                    # print(f"Naked Pair in {group_type} (Row: {row_index + 1} - Column: {col_index + 1} - Value: {candidate})")
                                    applied = True
                                    self.grid.update_candidates()
        return applied
