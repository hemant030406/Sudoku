import sys
import validator
import time
import pycosat
from copy import deepcopy
rows, cols = 9, 9

class SudokuSolver:
    def __init__(self, fp: str) -> None:
        self.init_states = []
        self.solve_time = 0
        self.generate_time = 0

        with open(fp) as f:
            line = f.readline()
            while line:
                state = []
                for i in range(0,rows*cols,rows):
                    state.append(list(map(lambda c: 0 if c == '.' else int(c), line[i:i+9])))
                self.init_states.append(state)
                line = f.readline()
        
        self.base_cnf = self.min_one_val_cnf() + self.col_cnf() + self.row_cnf() + self.smaller_block_cnf() + self.max_one_val_cnf()
        self.clause_map = tuple({} for _ in range(len(self.init_states)))
        self.clause_list = tuple([] for _ in range(len(self.init_states)))

    def cnf_prop_var_preproc(self, state_index: int, cnf: list[list[int]]) -> list[list[int]]:
        self.clause_map[state_index].clear()
        new_cnf = []
        counter = 1
        for clause in cnf:
            new_clause = []
            for propvar in clause:
                if propvar in self.clause_map[state_index]:
                    new_clause.append(self.clause_map[state_index][propvar])
                elif -propvar in self.clause_map[state_index]:
                    new_clause.append(-self.clause_map[state_index][-propvar])
                else:
                    if propvar < 0:
                        neg = True
                    else: neg = False
                    self.clause_map[state_index][abs(propvar)] = counter
                    self.clause_list[state_index].append(abs(propvar))
                    counter += 1
                    new_clause.append((counter - 1) * (-1 if neg else 1))
            new_cnf.append(new_clause)
        return new_cnf
     
    def solve(self, state_index: int) -> list:
        # start = time.time()
        cnf = self.base_cnf + self.gen_case_specific_cnf(state_index)
        # print("Clauses:", len(cnf))
        # new_cnf = self.cnf_prop_var_preproc(state_index, cnf)
        # self.generate_time += (start2 := time.time()) - start
        solved_cnf = pycosat.solve(cnf)
        # self.solve_time += time.time() - start2
        return list(filter(lambda x: x > 0,solved_cnf))


    def print_board_from_cnf(self, state_index: int, cnf_solved: list[int]):
        board = deepcopy(self.init_states[state_index])
        for prop_var in cnf_solved:
            # row, col, val = str(self.clause_list[state_index][prop_var - 1])
            row, col, val = str(prop_var)[0], str(prop_var)[1], str(prop_var)[2]
            board[int(row) - 1][int(col) - 1] = int(val)
        
        print(*board, sep='\n')
        return board

    def gen_case_specific_cnf(self, state_index: int) -> list[list[int]]:
        cnf = []
        # print(self.init_states[state_index])
        for i in range(rows):
            for j in range(cols):
                if (val := self.init_states[state_index][i][j]):
                    cnf.append([int(f'{i+1}{j+1}{val}')])
        # print(cnf)
        return cnf

    @staticmethod
    def min_one_val_cnf() -> list[list[int]]:
        cnf = []
        for row in range(rows):
            for col in range(cols):
                li = []
                for val in range(rows):
                    li.append(int(f'{row + 1}{col + 1}{val + 1}'))
                cnf.append(li)
        return cnf

    @staticmethod
    def max_one_val_cnf() -> list[list[int]]:
        cnf = []
        for row in range(rows):
            for col in range(cols):
                for val1 in range(rows):
                    for val2 in range(val1 + 1,rows):
                        cnf.append([-int(f'{row + 1}{col + 1}{val1 + 1}'),-int(f'{row + 1}{col + 1}{val2 + 1}')])
        return cnf

    @staticmethod
    def row_cnf() -> list[list[int]]:
        cnf = []
        for row in range(1,rows + 1):
            for val in range(1,rows + 1):
                li = []
                for col in range(1,cols + 1):
                    li.append(int(str(row)+str(col)+str(val)))
                    for nxt_col in range(col + 1,cols + 1):
                        cnf.append([-int(str(row)+str(col)+str(val)),-int(str(row)+str(nxt_col)+str(val))])
                cnf.append(li)
        
        return cnf

    @staticmethod
    def col_cnf() -> list[list[int]]:
        cnf = []
        for col in range(1,cols + 1):
            for val in range(1,rows + 1):
                li = []
                for row in range(1,rows + 1):
                    li.append(int(str(row)+str(col)+str(val)))
                    for nxt_row in range(row + 1,rows + 1):
                        cnf.append([-int(str(row)+str(col)+str(val)),-int(str(nxt_row)+str(col)+str(val))])
                cnf.append(li)
        return cnf

    @staticmethod
    def smaller_block_cnf() -> list[list[int]]:
        cnf = []
        for col in range(1,cols+1,3):
            for val in range(1,rows + 1):
                for row in range(1,rows + 1,3):
                    li = []
                    for i in range(3):
                        for j in range(3):
                            li.append(int(str(row + i)+str(col + j)+str(val)))
                    cnf.append(li)
        return cnf


def main():
    ss = SudokuSolver('p.txt')
    for i in range(len(ss.init_states)):
        print("Solving: ", i)
        ans = ss.solve(i)
        solved_board = ss.print_board_from_cnf(i, ans)
        if not (validator.isValidSudoku(solved_board)):
            print("FAILED")
            quit()
        else: print("PASSED")
    # print(f"{ss.generate_time = }")
    # print(f"{ss.solve_time = }")

def solve_for1():
    ss = SudokuSolver('p.txt')
    ss.solve(0)

    # print(ans)
if __name__ == '__main__':
    main()
    # solve_for1()