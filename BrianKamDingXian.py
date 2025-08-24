import time
import tracemalloc
import heapq

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
    
    def display_board(self, isInitial):
        """Display the chessboard with current queen positions"""
        print("\nInitial Board:" if isInitial else "\nFinal Board:")
        self.board = [['.' for _ in range(8)] for _ in range(8)]
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
                print(f"Move queen from row {row+1}, column {original_col+1} to column {col+1} (queens[{row}] = {col})")
            else:
                print(f"Place queen at row {row+1}, column {col+1} (queens[{row+1}] = {col+1})")

    def get_solution_list(self):
        return self.queens

# A* node class
class AStarNode:
    def __init__(self, queens, g_cost, move_sequence=None):
        self.queens = queens[:] # copy queens position list
        self.g_cost = g_cost  # number of moves needed to reach this state
        self.h_cost = self.calculate_heuristic()  # heuristic cost : number of conflicts
        self.f_cost = self.g_cost + self.h_cost  # total cost : f cost = g cost + h cost
        self.move_sequence = move_sequence or [] # sequence of moves from initial state to this state
    
    def calculate_heuristic(self):
        """Count conflicts between all queens"""
        conflicts = 0
        n = len(self.queens) # can remove if all 8 queens are always on board
        
        for i in range(n): # n = 8
             # can be removed
            if self.queens[i] == -1:
                conflicts += 3 # penalty for unplaced queen 
                continue
                
            # check conflicts with other queens
            for j in range(i + 1, n):
                # can be removed
                if self.queens[j] == -1: 
                    continue
                    
                if self.queens[i] == self.queens[j]: # same column
                    conflicts += 2
                
                if abs(self.queens[i] - self.queens[j]) == abs(i - j): # same diagonal : |row1 - row2| == |col1 - col2|
                    conflicts += 2
        
        return conflicts
    
    def is_goal(self):
        """Check if this is a goal state (valid queen placement)"""
        return self.h_cost == 0 # herustic cost = 0 means no conflicts (is goal state)
    
    def get_neighbors(self):
        """Generate all the next possible moves for queens (neighbors)"""
        neighbors = [] # list of neighbor nodes
        
        # iterate each row to find placed and unplaced queens 
        for row in range(8):
            # can be removed
            if self.queens[row] == -1:
                # Place unplaced queen
                for col in range(8):
                    new_queens = self.queens[:]
                    new_queens[row] = col
                    new_move_sequence = self.move_sequence + [(row, self.queens[row], col)]
                    neighbors.append(AStarNode(new_queens, self.g_cost + 1, new_move_sequence))
            else:
                initial_col = self.queens[row] # initial column
                # move queens to other columns in same row
                for col in range(8):
                    if col != initial_col: # avoid moving to same column
                        new_queens = self.queens[:] # copy current queens state
                        new_queens[row] = col # move queen to new column
                        new_move_sequence = self.move_sequence + [(row, initial_col, col)] # record move
                        neighbors.append(AStarNode(new_queens, self.g_cost + 1, new_move_sequence)) # create new node
        
        return neighbors
    
    # priority queue comparison methods : compare costs
    def __lt__(self, other):
        """Less than comparison for priority queue based on f_cost and h_cost"""
        if self.f_cost != other.f_cost:
            return self.f_cost < other.f_cost
        return self.h_cost < other.h_cost
    
    def __eq__(self, other):
        """Equality check based on queens configuration"""
        return self.queens == other.queens
    
    def __hash__(self):
        """Hash function for using in sets and dictionaries"""
        return hash(tuple(self.queens)) # easy way create unique hash for queens position

# A* Search Algorithm for 8 Queens Problem
def astar_search(eq):
    """A* search implementation for 8 Queens problem"""
    initial_state = AStarNode(eq.queens, 0) # initial state with g_cost = 0
    
    if initial_state.is_goal(): # skip if solved
        return
    
    open_set = [initial_state] # priority queue
    closed_set = set() # explored states
    visited_states = {tuple(initial_state.queens): 0} # dictionary to track visited states and their costs
    
    max_iterations = 10000  # prevent infinite loops
    iteration = 0
    
    while open_set and iteration < max_iterations:
        iteration += 1
        current = heapq.heappop(open_set)
        
        # if goal is found, update the board with solution(move sequence)
        if current.is_goal():
            for row, old_col, new_col in current.move_sequence: # old_col is placeholder
                eq.place_queen(row, new_col)
            return
        
        current_tuple = tuple(current.queens) # convert to tuple for explored state set
        if current_tuple in closed_set:
            continue
        
        closed_set.add(current_tuple)
        
        # generate neighbors
        for neighbor in current.get_neighbors():
            neighbor_tuple = tuple(neighbor.queens) # convert to tuple for easy compare
            
            # skip if neighbor already visited with a better or equal cost
            if neighbor_tuple in visited_states and visited_states[neighbor_tuple] <= neighbor.g_cost:
                continue
            
            # skip if already explored in closed(explored) set
            if neighbor_tuple in closed_set:
                continue
            
            visited_states[neighbor_tuple] = neighbor.g_cost
            heapq.heappush(open_set, neighbor)

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
        eq.display_board(isInitial=True)
        print("--- Moving Queens to Valid Configuration ---")

        # start tracking memory and time
        tracemalloc.start()
        start_time = time.perf_counter()

        # implement algorithm here
        astar_search(eq)
        eq.display_board(isInitial=False)

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

if __name__ == "__main__":
    run_test_cases()