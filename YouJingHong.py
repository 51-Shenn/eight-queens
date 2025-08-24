import time
import tracemalloc

class EightQueens:
    def __init__(self, queens=None):
        # if queens not given, initialize with -1 meaning empty
        self.queens = [-1] * 8
        self.move_count = 0
        if queens:
            for i in range(min(len(queens), 8)):
                self.queens[i] = queens[i]
        
    def set_queens(self, queens):
        """Set the queen positions manually with a given list"""
        self.queens = queens

    def is_valid_queen_placement(self):
        """Check whether the current placement of queens is valid"""
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
        """Display the chessboard with current queen positions"""
        print()
        self.board = [['-' for _ in range(8)] for _ in range(8)]
        for row, col in enumerate(self.queens):
            if 0 <= col < 8:
                self.board[row][col] = 'Q'
        for row in self.board:
            print(' '.join(row))
        print()

    def win_or_lose(self, test_case_no):
        """Evaluate and print if the current test case is a WIN (valid) or LOSE (invalid)"""
        if self.is_valid_queen_placement():
            print(f"Test Case {test_case_no} Result: WIN ✅")
            return True
        else:
            print(f"Test Case {test_case_no} Result: LOSE ❌")
            return False
    
    def place_queen(self, row, col):
        """Place or move a queen to a specified column in a given row"""
        if 0 <= row < 8 and 0 <= col < 8:
            original_col = self.queens[row]
            self.queens[row] = col
            self.move_count += 1
            if original_col != -1 and original_col != col:
                print(f"Move queen from row {row}, column {original_col} to column {col} (queens[{row}] = {col})")
            else:
                print(f"Place queen at row {row}, column {col} (queens[{row}] = {col})")

    def get_solution_list(self):
        return self.queens

def run_test_cases():
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

    solutions = []
    solution_states = []

    total_move_count = 0
    total_time_used = 0
    total_memory_used = 0
    win_count = 0
    no_of_test_cases = len(test_cases)

    # test all cases
    for i, case in enumerate(test_cases, 1):
        print('-' * 60)
        print(f"\nTest Case {i}: {case}")

        eq = EightQueens(case)
        eq.display_board()

        # start tracking memory and time
        tracemalloc.start()
        start_time = time.perf_counter()

        # implement algorithm here
        eq.set_queens(steepest_ascent_hill_climbing(eq))
        eq.display_board()

        # end memory and time tracking
        time_used = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        total_time_used += time_used
        total_memory_used += peak

        print(f"Solution: {eq.get_solution_list()}")
        solutions.append(eq.get_solution_list())
        print(f"Move Count: {eq.move_count}")
        total_move_count += eq.move_count

        is_win = eq.win_or_lose(i)
        solution_states.append("WIN ✅" if is_win else "LOSE ❌")
        win_count += int(is_win)

        print(f"Time Used: {time_used:.4f} seconds")
        print(f"Peak Memory Usage: {peak / 1024:.2f} KB\n") # show in KB

    print('-' * 60)
    lose_count = no_of_test_cases - win_count
    average_move_count = total_move_count / no_of_test_cases
    average_time = total_time_used / no_of_test_cases
    percentage = win_count / no_of_test_cases * 100
    average_memory = total_memory_used / no_of_test_cases

    # summary
    print(f"\nSUMMARY RESULTS:")
    print(f"Total Wins: {win_count}")
    print(f"Total Loss: {lose_count}")
    print(f"Total Move Count: {total_move_count}")
    print(f"Average Move Count: {average_move_count}")
    print(f"Total Time Taken: {total_time_used:.4f} seconds")
    print(f"Average Time: {average_time:.4f} seconds")
    print(f"Percentage of Test Cases Solved: {percentage:.2f}%")
    print(f"Total Peak Memory Used: {total_memory_used / 1024:.2f} KB")
    print(f"Average Peak Memory Per Case: {average_memory / 1024:.2f} KB\n")

    print("FINAL SOLUTIONS:")
    for i, s in enumerate(solutions, 1):
        print(f"Test Case {i:02d}: {s} -> {solution_states[i-1]}")
    print()

def heuristic (queens):
    conflicts = 0
    for row in range(8):   
        for col in range(row+1,8):
            if queens[row] == queens[col]:
                conflicts += 1
            elif abs(queens[row] - queens[col]) == abs(row - col):
                conflicts += 1

    return conflicts

def steepest_ascent_hill_climbing(eq):
    current_state = eq.queens[:]

    while True:
        # Find the heuristic of current state
        neighbors=[]
        neighbor_count = 0
        current_h = heuristic(current_state)
        best_h = current_h
        best_state = current_state[:]

        # Identify all neighbor states
        for row in range(8):
            for col in range(8):
                if col != current_state[row]:
                    neighbor_count += 1
                    neighbor_state = current_state[:]
                    neighbor_state[row] =  col
                    neighbors.append(neighbor_state)

        # Evaluate each neighbor state's heuristic, find the best neighbor state, move to that state, repeat the whole thing
        for neighbor in neighbors:
            neighbor_h = heuristic(neighbor)
            if neighbor_h < best_h:
                if neighbor_h == 0:
                    current_state = neighbor
                    return current_state
                else:
                    best_h = neighbor_h
                    best_state = neighbor
            
        if best_h == current_h:
            return current_state

        if best_h < current_h:
            current_state = best_state
            eq.move_count += 1
            current_h = best_h
  
if __name__ == "__main__":
    run_test_cases()