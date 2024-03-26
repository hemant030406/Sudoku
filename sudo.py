import sys
import validator
import time
import pycosat
from copy import deepcopy
from math import sqrt
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
     
    def solve(self, state_index: int) -> list:
        # start = time.time()
        cnf = self.base_cnf + self.gen_case_specific_cnf(state_index)
        # self.generate_time += (start2 := time.time()) - start
        solved_cnf = pycosat.solve(cnf)
        # self.solve_time += time.time() - start2
        return list(filter(lambda x: x > 0,solved_cnf))


    def print_board_from_cnf(self, state_index: int, cnf_solved: list[int]):
        board = deepcopy(self.init_states[state_index])
        for prop_var in cnf_solved:
            row, col, val = str(prop_var)[0], str(prop_var)[1], str(prop_var)[2]
            board[int(row) - 1][int(col) - 1] = int(val)
        
        print(*board, sep='\n')
        return board

    def gen_case_specific_cnf(self, state_index: int) -> list[list[int]]:
        cnf = []
        for i in range(rows):
            for j in range(cols):
                if (val := self.init_states[state_index][i][j]):
                    cnf.append([int(f'{i+1}{j+1}{val}')])
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
        for col in range(1,cols+1,int(sqrt(cols))):
            for val in range(1,rows + 1):
                for row in range(1,rows + 1,int(sqrt(rows))):
                    li = []
                    for i in range(int(sqrt(rows))):
                        for j in range(int(sqrt(cols))):
                            li.append(int(str(row + i)+str(col + j)+str(val)))
                    cnf.append(li)
        return cnf


def main(infp: str = 'p.txt',outfp: str = 'out.txt'):
    ss = SudokuSolver(infp)
    outfile = open(outfp,'w')
    outfile.write('SOLUTION:\n')
    outfile = open(outfp,'a')
    for i in range(len(ss.init_states)):
        print("Solving: ", i)
        ans = ss.solve(i)
        solved_board = ss.print_board_from_cnf(i, ans)
        if not (validator.isValidSudoku(solved_board)):
            print("FAILED")
            quit()
        else: print("PASSED")

        str_write = ''
        for row in solved_board:
            for col in row:
                str_write += str(col)
        outfile.write(str_write+'\n')
    # print(f"{ss.generate_time = }")
    # print(f"{ss.solve_time = }")

if __name__ == '__main__':
    if len(sys.argv) > 3:
        sys.stderr.write('More than expected number of args')
    elif len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
