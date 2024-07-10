import random
import tkinter as tk
from tkinter import messagebox

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

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.grid = generate_sudoku()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()
        
    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center')
                if self.grid[i][j] != 0:
                    entry.insert(0, str(self.grid[i][j]))
                    entry.config(state='disabled')
                entry.grid(row=i, column=j, padx=5, pady=5)
                self.entries[i][j] = entry
        check_button = tk.Button(self.root, text="Check Solution", command=self.check_solution)
        check_button.pack()

    def check_solution(self):
        user_grid = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    user_grid[i][j] = int(value)
                else:
                    messagebox.showerror("Error", "Please enter valid numbers (1-9).")
                    return
        if self.validate_solution(user_grid):
            messagebox.showinfo("Success", "Congratulations! The solution is correct.")
        else:
            messagebox.showerror("Error", "The solution is incorrect. Please try again.")

    def validate_solution(self, grid):
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                if num == 0 or not check_location_is_safe(grid, row, col, num):
                    return False
        return True

def main():
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()