from pysat.solvers import Solver

# class NQueensSatSolver: n, board, solver
class NQueensSatSolver:
    def __init__(self, n):
        self.n = n
        self.board = self._create_board()
        self.solver = Solver()

    # Create a board of size n x n
    def _create_board(self):
        board = [[0 for j in range(self.n)] for i in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                board[i][j] = i*self.n + j + 1
        return board

    # Get the variables of the queens in the same row
    def _queens_in_row(self, i):
        return self.board[i]

    # Get the variables of the queens in the same column
    def _queens_in_column(self, j):
       return [self.board[i][j] for i in range(self.n)]

    # Get the variables of the queens in the same diagonal
    def _queens_in_diag(self, x, y):
        diag_vars = [self.board[x][y]]
        for i in range(self.n):
            if x+i in range(self.n) and y+i in range(self.n):
                diag_vars.append(self.board[x+i][y+i])
            if x-i in range(self.n) and y-i in range(self.n):
                diag_vars.append(self.board[x-i][y-i])
        return diag_vars

    # Get the variables of the queens in the same anti-diagonal
    def _queens_in_anti_diag(self, x, y):
        anti_diag_vars = [self.board[x][y]]
        for i in range(self.n):
            if x+i in range(self.n) and y-i in range(self.n):
                anti_diag_vars.append(self.board[x+i][y-i])
            if x-i in range(self.n) and y+i in range(self.n):
                anti_diag_vars.append(self.board[x-i][y+i])
        return anti_diag_vars

    # Get the variables of the queens that can be attacked by the queen at (x, y)
    def _attacked_vars(self, x, y):
        s = set()
        s.update(self._queens_in_row(x))
        s.update(self._queens_in_column(y))
        s.update(self._queens_in_diag(x, y))
        s.update(self._queens_in_anti_diag(x, y))
        s.remove(self.board[x][y])
        return s

    def create_clauses(self):
        # First set of clauses: There must be a queen in each row.
        for i in range(self.n):
            self.solver.add_clause(self._queens_in_row(i))

        # Second set of clauses: There must be a queen in each column.
        for i in range(self.n):
            self.solver.add_clause(self._queens_in_column(i))

        # Third set of clauses: No two queens can attack each other.
        for i in range(self.n):
            for j in range(self.n):
                for attacked in self._attacked_vars(i, j):
                    clause = [-self.board[i][j], -attacked]
                    self.solver.add_clause(clause)
                    # print(f"Attack clause: {clause}")

    # Answer the SAT problem
    def solve(self):
        self.create_clauses()
        if self.solver.solve():
            print("[SAT] ")
            self.print_model()
        else:
            print("[UNSAT]", end=" ")

    # Print the solution
    def print_model(self):
        print("Solution:")
        for i in range(self.n):
            s = ""
            for j in range(self.n):
                if self.solver.get_model()[self.board[i][j]-1] > 0:
                    s += "👑"
                else:
                    s += "⬜" if (i + j) % 2 == 0 else "⬛"
            print(s)

# Main
if __name__ == "__main__":
    import sys
    n = int(sys.argv[1])
    solver = NQueensSatSolver(n)
    solver.solve()
