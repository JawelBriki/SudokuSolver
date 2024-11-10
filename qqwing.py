with open("qqwing.txt") as qqwing:
    grid = [list(line.strip()) for line in qqwing]
    for i in range(9):
        for j in range(9):
            if grid[i][j] == '.':
                grid[i][j] = '0'
    with open("sudoku.txt", 'w') as sudoku:
        for row in grid:
            sudoku.write(f"{','.join(row)}\n")
