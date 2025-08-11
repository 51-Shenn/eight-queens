import time
import tracemalloc
import random
import numpy as np
from typing import List, Tuple

# Genetic Algorithm Parameters
POP_SIZE = 100
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8

def fitness(chromosome):
    """Calculate fitness for 8-Queens problem. Higher fitness = fewer conflicts."""
    conflicts = 0
    n = len(chromosome)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Check if queens are on same column
            if chromosome[i] == chromosome[j]:
                conflicts += 1
            # Check diagonal conflicts
            elif abs(chromosome[i] - chromosome[j]) == abs(i - j):
                conflicts += 1
    
    # Return fitness (28 is max possible - total pairs minus conflicts)
    max_pairs = n * (n - 1) // 2  # 28 for n=8
    return max_pairs - conflicts

def select(population):
    """Tournament selection - select two parents."""
    def tournament_select():
        tournament_size = 3
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: fitness(x))
    
    parent1 = tournament_select()
    parent2 = tournament_select()
    return parent1, parent2

def crossover(parent1, parent2):
    """Order crossover (OX) - preserves relative order."""
    if random.random() > CROSSOVER_RATE:
        return parent1.copy()
    
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    # Create offspring
    offspring = [-1] * size
    
    # Copy selected segment from parent1
    offspring[start:end] = parent1[start:end]
    
    # Get elements from parent2 that are not already in offspring
    used_elements = set(offspring[start:end])
    remaining = []
    for x in parent2:
        if x not in used_elements:
            remaining.append(x)
            used_elements.add(x)
    
    # If we don't have enough unique elements, fill with missing values 0-7
    all_values = set(range(8))
    missing_values = list(all_values - used_elements)
    remaining.extend(missing_values)
    
    # Fill remaining positions
    j = 0
    for i in range(size):
        if offspring[i] == -1:
            if j < len(remaining):
                offspring[i] = remaining[j]
                j += 1
            else:
                # Fallback: use any remaining value from 0-7
                for val in range(8):
                    if offspring.count(val) == 0:
                        offspring[i] = val
                        break
    
    return offspring

def mutate(chromosome):
    """Swap mutation - swap two random positions."""
    if random.random() < MUTATION_RATE:
        chromosome = chromosome.copy()
        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

def create_random_chromosome():
    """Create a random chromosome (permutation of 0-7)."""
    chromosome = list(range(8))
    random.shuffle(chromosome)
    return chromosome

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
        self.move_count += 1  # Count this as a move

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

        # Genetic Algorithm Implementation
        print(f"Initial fitness: {fitness(case)}")
        
        # Initialize population with current test case and random chromosomes
        population = [case.copy()]  # Include the test case
        for _ in range(POP_SIZE - 1):
            population.append(create_random_chromosome())

        best_solution = case.copy()
        best_fitness = fitness(case)
        generation_found = 0

        for generation in range(MAX_GENERATIONS):
            # Sort population by fitness (best first)
            population = sorted(population, key=lambda x: fitness(x), reverse=True)
            
            current_best_fitness = fitness(population[0])
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = population[0].copy()
                generation_found = generation
            
            # Check if solution found (fitness = 28 means no conflicts)
            if best_fitness == 28:
                print(f"Perfect solution found in generation {generation}: {best_solution}")
                break

            # Elitism - keep top 10% of population
            elite_size = max(1, POP_SIZE // 10)
            new_population = population[:elite_size]

            # Generate rest of population through crossover and mutation
            while len(new_population) < POP_SIZE:
                parent1, parent2 = select(population)
                child = crossover(parent1, parent2)
                child = mutate(child)
                new_population.append(child)

            population = new_population
        else:
            print(f"Best solution found (fitness {best_fitness}) in generation {generation_found}: {best_solution}")

        # Set the best solution found
        eq.set_queens(best_solution)
        eq.display_board()

        # end memory and time tracking
        time_used = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        total_time_used += time_used
        total_memory_used += peak

        print(f"Solution: {eq.get_solution_list()}")
        print(f"Solution fitness: {fitness(eq.get_solution_list())}")
        solutions.append(eq.get_solution_list())
        print(f"Move Count: {eq.move_count}")
        total_move_count += eq.move_count

        is_win = eq.win_or_lose(i)
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
        fitness_score = fitness(s)
        status = "✅ PERFECT" if fitness_score == 28 else f"❌ Fitness: {fitness_score}"
        print(f"Test Case {i}: {s} - {status}")
    print()

if __name__ == "__main__":
    run_test_cases()