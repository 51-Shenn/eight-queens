class EightQueen:
    def __init__(self, queens=None):
        # if queens list is not defined, initialize as empty list
        self.queens = queens if queens is not None else [] 
        
    def set_queens(self, queens):
        self.queens = queens

    def is_valid_queen_placement(self):
        n = len(self.queens);
        for i in range(n):
            for j in range(i + 1, n):
                # check if in the same column
                if self.queens[i] == self.queens[j]:
                    return False;

                # check if in the same diagonal
                if abs(self.queens[i] - self.queens[j]) == abs(i - j):
                    return False;

        return True # if passed all constraints return true
    
    def display_board(self):
        board = [['.' for _ in range(8)] for _ in range(8)]
        for row, col in enumerate(self.queens):
            if 0 <= col < 8:
                board[row][col] = 'Q'
        for row in board:
            print(' '.join(row))

    def win_or_lose(self, test_case_no):
        if self.is_valid_queen_placement():
            print(f"\nTest Case {test_case_no} Result: WIN  ✅\n")
        else:
            print(f"\nTest Case {test_case_no} Result: LOSE ❌\n")

    def print_queen_placement_steps(self, queens):
        for row, col in enumerate(queens):
            print(f"Step: queens[{row}][{col}] = queens[{row}][{col}]")

# 10 different test cases
# queens[i] = j --> queen at row i, column j.
test_cases = [
    [0, 4, 7, 5, 2, 6, 1, 3],
    [0, 1, 2, 3, 4, 5, 6, 7],
    [1, 3, 5, 7, 2, 0, 6, 4],
    [2, 4, 6, 0, 3, 1, 7, 5],
    [0, 2, 4, 1, 7, 5, 3, 6],
    [3, 1, 6, 2, 5, 7, 0, 4],
    [4, 6, 0, 2, 7, 5, 3, 1],
    [5, 3, 0, 4, 7, 1, 6, 2],
    [0, 2, 4, 6, 1, 3, 5, 7],
    [1, 5, 0, 6, 3, 7, 2, 4], 
]

# test all cases
# Step: queens[a][b] = queens[c][d] --> queen from row a, col b move to row c, col d
for i, case in enumerate(test_cases, 1):
    print('-' * 40)
    eq = EightQueen(case)
    print(f"\nTest Case {i}: {case}\n")
    eq.print_queen_placement_steps(case)
    eq.win_or_lose(i)

print('-' * 40)