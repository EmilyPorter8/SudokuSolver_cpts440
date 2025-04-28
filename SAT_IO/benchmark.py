import psutil, time
import matplotlib.pyplot as plt
import seaborn as sns 
from z3 import Solver, Bool, Or, Not
from pysat.solvers import Minisat22

# Encode (row, col, value) into a single SAT variable
def var(i, j, k, n):
    return i * n * n + j * n + k + 1

# Generate CNF with only cell-level constraints
def generate_sudoku_cnf(n):
    clauses = []
    rng = range(n)
    
    # Each cell must have at least one number
    clauses.extend([[var(i, j, k, n) for k in rng] for i in rng for j in rng])
    
    # Each cell must have at most one number (no two numbers in a single cell)
    for i in rng:
        for j in rng:
            for k1 in rng:
                for k2 in rng:
                    if k1 < k2:
                        clauses.append([-var(i, j, k1, n), -var(i, j, k2, n)])
    
    return clauses

# Solve using Z3
def solve_with_z3(cnf):
    s = Solver()
    for clause in cnf:
        s.add(Or(*[Bool(f'x{abs(lit)}') if lit > 0 else Not(Bool(f'x{abs(lit)}')) for lit in clause]))
    s.check()

# Solve using PySAT
def solve_with_pysat(cnf):
    with Minisat22(bootstrap_with=cnf) as m:
        m.solve()

# Benchmark a given solver
def benchmark(solver_func, cnf):
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024 * 1024)
    start_time = time.time()
    solver_func(cnf)
    end_time = time.time()
    mem_after = process.memory_info().rss / (1024 * 1024)
    memory_used = abs(mem_after - mem_before)
    return round(memory_used, 2), round(end_time - start_time, 3)

if __name__ == "__main__":
    # Block sizes (board size = block^2 x block^2)
    block_sizes = [2, 3, 4, 5, 6, 7, 8, 9]  # Includes 81x81 board at block=9

    z3_memory, z3_time = [], []
    pysat_memory, pysat_time = [], []

    for block in block_sizes:
        n = block * block  # Full board size (n x n)
        print(f"\nGenerating {n}x{n} CNF...")
        cnf = generate_sudoku_cnf(n)

        print(f"Solving with Z3...")
        mem_z3, time_z3 = benchmark(solve_with_z3, cnf)

        print(f"Solving with PySAT...")
        mem_ps, time_ps = benchmark(solve_with_pysat, cnf)

        z3_memory.append(mem_z3)
        z3_time.append(time_z3)
        pysat_memory.append(mem_ps)
        pysat_time.append(time_ps)

        print(f"{n}x{n} | Z3: {mem_z3} MB, {time_z3}s | PySAT: {mem_ps} MB, {time_ps}s")

  
    sns.set(style="whitegrid")

    # Save memory plot
    plt.figure(figsize=(10, 6))
    board_labels = [f"{b*b}x{b*b}" for b in block_sizes]
    plt.plot(block_sizes, z3_memory, marker='o', label='Z3 Memory (MB)')
    plt.plot(block_sizes, pysat_memory, marker='o', label='PySAT Memory (MB)')
    plt.xticks(block_sizes, board_labels)
    plt.title('Memory Usage vs Board Size (Cell-Level Constraints)')
    plt.xlabel('Board Size')
    plt.ylabel('Memory Used (MB)')
    plt.legend()
    plt.grid(True)
    plt.savefig("memory_vs_board_size.png")
    plt.close()

    # Save time plot
    plt.figure(figsize=(10, 6))
    plt.plot(block_sizes, z3_time, marker='o', label='Z3 Time (s)')
    plt.plot(block_sizes, pysat_time, marker='o', label='PySAT Time (s)')
    plt.xticks(block_sizes, board_labels)
    plt.title('Solving Time vs Board Size (Cell-Level Constraints)')
    plt.xlabel('Board Size')
    plt.ylabel('Time Taken (s)')
    plt.legend()
    plt.grid(True)
    plt.savefig("time_vs_board_size.png")
    plt.close()

    print("\nBenchmark complete! Graphs saved as:")
    print(" - memory_vs_board_size.png")
    print(" - time_vs_board_size.png")
