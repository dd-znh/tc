from pysat.solvers import Solver
import sys

class NQueensSatSolver:
    def __init__(self, n):
        self.n = n
        self.board = self._create_board()
        self.solver = Solver()

    def _create_board(self):
        board = [[0 for j in range(self.n)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                board[i][j] = i * self.n + j + 1
        print("Board:")
        for i in range(self.n):
            print(board[i])
        print()
        return board

    def _queens_in_row(self, i):
        return self.board[i]

    def _queens_in_column(self, j):
        return [self.board[i][j] for i in range(self.n)]

    def _queens_in_diag(self, x, y):
        diag_vars = [self.board[x][y]]
        for i in range(self.n):
            if x + i in range(self.n) and y + i in range(self.n):
                diag_vars.append(self.board[x + i][y + i])
            if x - i in range(self.n) and y - i in range(self.n):
                diag_vars.append(self.board[x - i][y - i])
        return diag_vars

    def _queens_in_anti_diag(self, x, y):
        anti_diag_vars = [self.board[x][y]]
        for i in range(self.n):
            if x + i in range(self.n) and y - i in range(self.n):
                anti_diag_vars.append(self.board[x + i][y - i])
            if x - i in range(self.n) and y + i in range(self.n):
                anti_diag_vars.append(self.board[x - i][y + i])
        return anti_diag_vars

    def _attacked_vars(self, x, y):
        s = set()
        s.update(self._queens_in_row(x))
        s.update(self._queens_in_column(y))
        s.update(self._queens_in_diag(x, y))
        s.update(self._queens_in_anti_diag(x, y))
        s.remove(self.board[x][y])
        return s

    def create_clauses(self):
        print("Clauses:")
        print()
        print("First set of clauses: There must be a queen in each row.")
        print()
        for i in range(self.n):
            self.solver.add_clause(self._queens_in_row(i))
            print(f"Row clause: {self.format_clauses_to_logic([self._queens_in_row(i)])}")
        print()

        print("Second set of clauses: There must be a queen in each column.")
        print()
        for i in range(self.n):
            self.solver.add_clause(self._queens_in_column(i))
            print(f"Column clause: {self.format_clauses_to_logic([self._queens_in_column(i)])}")
        print()

        print("Third set of clauses: No two queens can attack each other.")
        print()
        for i in range(self.n):
            for j in range(self.n):
                print(f"Posição: x = {i}, y = {j}")
                for attacked in self._attacked_vars(i, j):
                    clause = [-self.board[i][j], -attacked]
                    self.solver.add_clause(clause)
                    print(f"Attacked clause: {self.format_clauses_to_logic([clause])}")
                print()

    def format_clauses_to_logic(self, clauses):
        logical_formulas = []
        for clause in clauses:
            formatted_clause = " ∨ ".join(
                [f"{abs(var)}" if var > 0 else f"¬{abs(var)}" for var in clause]
            )
            logical_formulas.append(f"({formatted_clause})")
        return logical_formulas

    def solve(self):
        self.create_clauses()
        if self.solver.solve():
            print("[SAT] ")
            self.print_model()
        else:
            print("[UNSAT]", end=" ")

    def print_model(self):
        print("Solution:")
        for i in range(self.n):
            s = ""
            for j in range(self.n):
                if self.solver.get_model()[self.board[i][j] - 1] > 0:
                    s += "👑"
                else:
                    s += "⬜" if (i + j) % 2 == 0 else "⬛"
            print(s)

if __name__ == "__main__":
    n = int(sys.argv[1])
    output_file = f"{n}.txt"
    with open(output_file, "w") as f:
        sys.stdout = f
        solver = NQueensSatSolver(n)
        solver.solve()
    sys.stdout = sys.__stdout__
