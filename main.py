import time
import tracemalloc
class EightQueens:
    def __init__(self, queens=None):
        # if queens not given, initialize with -1 meaning empty
        self.queens = [-1] * 8
        if queens:
            for i in range(min(len(queens), 8)):
                self.queens[i] = queens[i]
        
    def set_queens(self, queens):
        self.queens = queens

    def is_valid_queen_placement(self):
        n = len(self.queens)
        for i in range(n):
            for j in range(i + 1, n):
                # check if in the same column
                if self.queens[i] == self.queens[j]:
                    return False

                # check if in the same diagonal
                if abs(self.queens[i] - self.queens[j]) == abs(i - j):
                    return False

        return True # if passed all constraints return true
    
    def display_board(self):
        """Display the current position of queens in the chessboard"""
        print()
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        for row, col in enumerate(self.queens):
            if 0 <= col < 8:
                self.board[row][col] = 'Q'
        for row in self.board:
            print(' '.join(row))
        print()

    def win_or_lose(self, test_case_no):
        """To determine whether the currect position of all queens is valid or invalid"""
        if self.is_valid_queen_placement():
            print(f"Test Case {test_case_no} Result: WIN  ✅")
            return 0
        else:
            print(f"Test Case {test_case_no} Result: LOSE ❌")
            return 1
    
    def place_queen(self, row, col):
        """
        Place or move a queen to a specified column in a given row
        Use this function in algorithm implementation

        Example: 
            1. Queen currently at row 0, col 0
            2. AFTER place_queen(row=0, col=2)
            3. Queen moved to row 0, col 2
        """
        if 0 <= row < 8 and 0 <= col < 8:
            self.queens[row] = col
            self.board[row][col] = 'Q'
            print(f"Step: Place queen at row {row}, column {col} (queens[{row}] = {col})")

# 10 different test cases (to be changed)
# queens[i] = j --> queen at row i, column j.
test_cases = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [7, 6, 5, 4, 3, 2, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 4, 6, 0, 2, 4, 6],
    [1, 3, 1, 3, 1, 3, 1, 3],
    [0, 2, 2, 5, 5, 7, 7, 1],
    [4, 4, 2, 2, 0, 0, 6, 6],
    [0, 3, 1, 4, 2, 5, 3, 6],
    [1, 1, 1, 1, 2, 2, 2, 2],
    [0, 1, 0, 1, 0, 1, 0, 1], 
]

total_time_used = 0
total_memory_used = 0
win_count = 0
no_of_test_cases = len(test_cases)

# test all cases
for i, case in enumerate(test_cases, 1):
    print('-' * 40)
    print(f"\nTest Case {i}: {case}")

    eq = EightQueens(case)
    eq.display_board()

    # start tracking memory and time
    tracemalloc.start()
    start_time = time.perf_counter()

    # implement algorithm here
    eq.place_queen(row=1, col=2)
    eq.place_queen(row=3, col=7)
    eq.display_board()

    # end memory and time tracking
    time_used = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time_used += time_used
    total_memory_used += peak

    is_win = eq.win_or_lose(i)
    win_count += int(is_win)

    print(f"Time Used: {time_used:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB\n") # show in KB

print('-' * 40)
lose_count = no_of_test_cases - win_count
average_time = total_time_used / len(test_cases)
percentage = win_count / no_of_test_cases * 100
average_memory = total_memory_used / no_of_test_cases

# summary
print(f"\nTotal Wins: {win_count}")
print(f"Total Loss: {lose_count}")
print(f"Total Time Taken: {total_time_used:.4f} seconds")
print(f"Average Time: {average_time:.4f} seconds")
print(f"Percentage of Test Cases Solved: {percentage:.2f}%")
print(f"Total Peak Memory Used: {total_memory_used / 1024:.2f} KB")
print(f"Average Peak Memory Per Case: {average_memory / 1024:.2f} KB\n")