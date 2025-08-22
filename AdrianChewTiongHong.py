import time
import tracemalloc

class EightQueens:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.move_count = 0
        self.solutions = []
        
    def reset_board(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.move_count = 0
        self.solutions = []
    
    def place_queen(self, row: int, col: int) -> bool:
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = 1
            self.move_count += 1
            return True
        return False
    
    def remove_queen(self, row: int, col: int) -> bool:
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = 0
            return True
        return False
    
    def is_safe(self, row: int, col: int) -> bool:
        for i in range(row):
            if self.board[i][col] == 1:
                return False
        
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1
        
        i, j = row - 1, col + 1
        while i >= 0 and j < 8:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j += 1
        
        return True
    
    def dfs_solve(self, row: int = 0) -> bool:
        if row >= 8:
            solution = [row[:] for row in self.board]
            self.solutions.append(solution)
            return True
        
        for col in range(8):
            if self.is_safe(row, col):
                self.place_queen(row, col)
                
                if self.dfs_solve(row + 1):
                    return True
                
                self.remove_queen(row, col)
        
        return False
    
    def find_all_solutions(self) -> List[List[List[int]]]:
        self.reset_board()
        self._find_all_solutions_helper(0)
        return self.solutions
    
    def _find_all_solutions_helper(self, row: int):
        if row >= 8:
            solution = [row[:] for row in self.board]
            self.solutions.append(solution)
            return
        
        for col in range(8):
            if self.is_safe(row, col):
                self.place_queen(row, col)
                self._find_all_solutions_helper(row + 1)
                self.remove_queen(row, col)
    
    def print_board(self, board: Optional[List[List[int]]] = None):
        if board is None:
            board = self.board
        
        print("  " + " ".join([str(i) for i in range(8)]))
        for i, row in enumerate(board):
            print(f"{i} " + " ".join(['Q' if cell == 1 else '.' for cell in row]))
        print()
    
    def get_stats(self) -> dict:
        return {
            'move_count': self.move_count,
            'solutions_found': len(self.solutions)
        }

def run_test_cases():
    print("=" * 50)
    print("Eight Queens Problem - DFS Implementation")
    print("=" * 50)
    
    test_results = []
    
    print("\nTest Case 1: Find One Solution")
    eq1 = EightQueens()
    
    tracemalloc.start()
    start_time = time.time()
    
    success = eq1.dfs_solve()
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_used = end_time - start_time
    memory_used = peak / 1024 / 1024
    
    if success:
        print("Result: WIN - Solution found!")
        eq1.print_board()
        result = "WIN"
    else:
        print("Result: LOSE - No solution found!")
        result = "LOSE"
    
    stats1 = eq1.get_stats()
    print(f"Move Count: {stats1['move_count']}")
    print(f"Time Used: {time_used:.6f} seconds")
    print(f"Memory Used: {memory_used:.2f} MB")
    
    test_results.append({
        'test_case': 1,
        'result': result,
        'moves': stats1['move_count'],
        'time': time_used,
        'memory': memory_used
    })
    
    print("\nTest Case 2: Find All Solutions")
    eq2 = EightQueens()
    
    tracemalloc.start()
    start_time = time.time()
    
    all_solutions = eq2.find_all_solutions()
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_used = end_time - start_time
    memory_used = peak / 1024 / 1024
    
    if all_solutions:
        print(f"Result: WIN - Found {len(all_solutions)} solutions!")
        print("First solution:")
        eq2.print_board(all_solutions[0])
        result = "WIN"
    else:
        print("Result: LOSE - No solutions found!")
        result = "LOSE"
    
    stats2 = eq2.get_stats()
    print(f"Move Count: {stats2['move_count']}")
    print(f"Solutions Found: {len(all_solutions)}")
    print(f"Time Used: {time_used:.6f} seconds")
    print(f"Memory Used: {memory_used:.2f} MB")
    
    test_results.append({
        'test_case': 2,
        'result': result,
        'moves': stats2['move_count'],
        'time': time_used,
        'memory': memory_used,
        'solutions': len(all_solutions)
    })
    
    print("\nTest Case 3: Performance Test (First 3 Solutions)")
    eq3 = EightQueens()
    
    tracemalloc.start()
    start_time = time.time()
    
    solutions_found = 0
    def find_limited_solutions(row: int = 0) -> bool:
        nonlocal solutions_found
        if solutions_found >= 3:
            return True
            
        if row >= 8:
            solution = [row[:] for row in eq3.board]
            eq3.solutions.append(solution)
            solutions_found += 1
            return solutions_found >= 3
        
        for col in range(8):
            if eq3.is_safe(row, col):
                eq3.place_queen(row, col)
                if find_limited_solutions(row + 1):
                    return True
                eq3.remove_queen(row, col)
        
        return False
    
    find_limited_solutions()
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_used = end_time - start_time
    memory_used = peak / 1024 / 1024
    
    if eq3.solutions:
        print(f"Result: WIN - Found {len(eq3.solutions)} solutions!")
        print("Solution 1:")
        eq3.print_board(eq3.solutions[0])
        result = "WIN"
    else:
        print("Result: LOSE - No solutions found!")
        result = "LOSE"
    
    stats3 = eq3.get_stats()
    print(f"Move Count: {stats3['move_count']}")
    print(f"Solutions Found: {len(eq3.solutions)}")
    print(f"Time Used: {time_used:.6f} seconds")
    print(f"Memory Used: {memory_used:.2f} MB")
    
    test_results.append({
        'test_case': 3,
        'result': result,
        'moves': stats3['move_count'],
        'time': time_used,
        'memory': memory_used,
        'solutions': len(eq3.solutions)
    })
    
    print("\n" + "=" * 50)
    print("FINAL STATISTICS")
    print("=" * 50)
    
    win_count = sum(1 for r in test_results if r['result'] == 'WIN')
    lose_count = len(test_results) - win_count
    
    total_moves = sum(r['moves'] for r in test_results)
    total_time = sum(r['time'] for r in test_results)
    total_memory = sum(r['memory'] for r in test_results)
    
    avg_moves = total_moves / len(test_results)
    avg_time = total_time / len(test_results)
    avg_memory = total_memory / len(test_results)
    
    print(f"Total Results: {win_count} WIN / {lose_count} LOSE")
    print(f"Average Moves: {avg_moves:.2f}")
    print(f"Average Time: {avg_time:.6f} seconds")
    print(f"Average Memory: {avg_memory:.2f} MB")
    
    print("\nIndividual Test Case Results:")
    for result in test_results:
        solutions_info = f" ({result.get('solutions', 0)} solutions)" if 'solutions' in result else ""
        print(f"   Test Case {result['test_case']}: {result['result']} - "
              f"{result['moves']} moves, {result['time']:.6f}s, {result['memory']:.2f}MB{solutions_info}")
    
    print("\nAlgorithm Analysis:")
    print("   Completeness: Complete (found solutions in finite search space)")
    print("   Optimality: Not guaranteed (DFS finds first solution, not necessarily optimal)")
    print(f"   Time Complexity: O(N!) - Actual performance varies with pruning")
    print(f"   Space Complexity: O(N) - Linear space for recursion stack")

if __name__ == "__main__":
    run_test_cases()
