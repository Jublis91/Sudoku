import random

def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def find_empty_location(grid, l):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                l[0], l[1] = row, col
                return True
    return False

def used_in_row(grid, row, num):
    return any(grid[row][i] == num for i in range(9))

def used_in_col(grid, col, num):
    return any(grid[i][col] == num for i in range(9))

def used_in_box(grid, box_start_row, box_start_col, num):
    return any(grid[i][j] == num for i in range(box_start_row, box_start_row + 3) for j in range(box_start_col, box_start_col + 3))

def check_location_is_safe(grid, row, col, num):
    return not used_in_row(grid, row, num) and not used_in_col(grid, col, num) and not used_in_box(grid, row - row % 3, col - col % 3, num)

def solve_sudoku(grid):
    l = [0, 0]
    if not find_empty_location(grid, l):
        return True
    row, col = l[0], l[1]
    for num in range(1, 10):
        if check_location_is_safe(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def fill_diagonal_boxes(grid):
    for i in range(0, 9, 3):
        fill_box(grid, i, i)

def fill_box(grid, row, col):
    num_list = list(range(1, 10))
    random.shuffle(num_list)
    for i in range(3):
        for j in range(3):
            grid[row + i][col + j] = num_list.pop()

def remove_digits(grid, count):
    while count > 0:
        cell_id = random.randint(0, 80)
        row, col = cell_id // 9, cell_id % 9
        if grid[row][col] != 0:
            grid[row][col] = 0
            count -= 1

def generate_sudoku():
    grid = [[0] * 9 for _ in range(9)]
    fill_diagonal_boxes(grid)
    solve_sudoku(grid)
    remove_digits(grid, 40)
    return grid

def main():
    sudoku_grid = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_grid(sudoku_grid)
    if solve_sudoku(sudoku_grid):
        print("\nSolution:")
        print_grid(sudoku_grid)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()