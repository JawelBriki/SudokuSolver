
class SudokuGrid:
    """
    Representation of a Sudoku grid as a 9x9 matrix.\n
    Only one instance of this class exists at any given time (Singleton).\n
    """
    instance = None

    def __new__(cls, *args):
        if not cls.instance:
            cls.instance = super(SudokuGrid, cls).__new__(cls)
        return cls.instance

    def __init__(self, grid):
        if not hasattr(self, 'grid'):
            self.grid = grid
            self.candidates = {(i, j): list() for i in range(9) for j in range(9)}

    def __repr__(self):
        r = ""
        for i in range(9):
            for j in range(9):
                r += str(self.grid[i][j]) if self.grid[i][j] else '.'
                if j != 8:
                    r += ' '
                if (j + 1) % 3 == 0 and j != 8:
                    r += ('|' + ' ')
            r += '\n'
            if (i + 1) % 3 == 0 and i != 8:
                r += '––––––|–––––––|––––––\n'
        return r

    def get_cell(self, row_index, col_index) -> int:
        return self.grid[row_index][col_index]

    def get_row(self, row_index) -> list[int]:
        return self.grid[row_index]

    def get_column(self, col_index) -> list[int]:
        return [row[col_index] for row in self.grid]

    def get_block(self, row_index, col_index) -> list[int]:
        block_row = row_index // 3 * 3
        block_col = col_index // 3 * 3
        return [
            self.grid[r][c]
            for r in range(block_row, block_row + 3)
            for c in range(block_col, block_col + 3)
        ]

    def set_cell(self, row_index, col_index, value):
        self.grid[row_index][col_index] = value

    def update_candidates(self):
        numbers = set(range(1, 10))
        for i in range(9):
            for j in range(9):
                if self.get_cell(i, j) == 0:
                    row = self.get_row(i)
                    col = self.get_column(j)
                    block = self.get_block(i, j)
                    previous_candidates = self.get_cell_candidates(i, j)

                    cell_candidates = numbers - set(row) - set(col) - set(block)
                    if previous_candidates:
                        cell_candidates = cell_candidates.intersection(set(previous_candidates))
                    self.candidates[(i, j)] = sorted(list(cell_candidates))
                else:
                    self.candidates[(i, j)] = list()

    def get_cell_candidates(self, row_index, col_index) -> list[int]:
        return self.candidates[(row_index, col_index)]

    @staticmethod
    def _is_valid_group(group):
        seen = set()
        for num in group:
            if num != 0:
                if num in seen or num < 1 or num > 9:
                    return False
                seen.add(num)
        return True

    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.get_cell(i, j) == 0:
                    return False
        return True

    def is_valid(self):
        for i in range(9):
            row = self.get_row(i)
            col = self.get_column(i)
            block = self.get_block((i // 3) * 3, (i % 3) * 3)
            if not self._is_valid_group(row) or not self._is_valid_group(col) or not self._is_valid_group(block):
                return False
        return True
