from deductionrule import DR1, DR2, DR3
from grid import SudokuGrid


class SudokuSolver:
    """
    A class to solve a Sudoku puzzle using deduction rules.
    The puzzle is read from a file and the solution is printed to the console.
    Deduction rules are applied in order of increasing difficulty.
    """

    def __init__(self, grid_file: str):
        with open(grid_file, 'r') as file:
            self.grid = SudokuGrid([list(map(int, line.split(','))) for line in file])
            self.dr1 = DR1(self.grid)
            self.dr2 = DR2(self.grid)
            self.dr3 = DR3(self.grid)

    def show_grid(self):
        print(self.grid)

    def is_solved(self) -> bool:
        return self.grid.is_valid() and self.grid.is_complete()

    def ask_user_for_input(self) -> None:
        print("No more deductions possibles. Please fill a cell correctly to proceed with solving.")
        row, col, val = input("Enter the row, column, and value separated by commas (starting at index 0): ").split(',')
        self.grid.set_cell(int(row), int(col), int(val))

    def solve_easy(self) -> bool:
        while self.dr1.apply():
            pass
        if self.is_solved():
            self.show_grid()
            print("Solved.\nDifficulty: Easy")
            return True
        return False

    def solve_medium(self) -> bool:
        while self.dr2.apply():
            pass
        if self.is_solved():
            self.show_grid()
            print("Solved.\nDifficulty: Medium")
            return True
        return False

    def solve_hard(self) -> None:
        input_required = False
        rules = [self.dr3, self.dr2, self.dr1]
        while not self.is_solved():
            applied = False
            for rule in rules:
                applied = applied or rule.apply()
            if not applied:
                self.show_grid()
                self.ask_user_for_input()
                # Since user input was required, classify as Very Hard (or the grid might be invalid)
                input_required = True
                if not self.grid.is_valid():
                    print("Error found. Please restart the solving process from the beginning.")
                    return
        self.show_grid()
        print(f"Solved.\nDifficulty: {'Very Hard' if input_required else 'Hard'}")

    def solve(self) -> None:
        self.show_grid()

        # Try solving with DR1 only
        if self.solve_easy():
            return

        # Try solving with DR2 only
        if self.solve_medium():
            return

        # Try solving with all rules
        self.solve_hard()


if __name__ == '__main__':
    solver = SudokuSolver("sudoku.txt")
    solver.solve()
