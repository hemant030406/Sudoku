import pycosat
from copy import deepcopy
rows, cols = 9, 9





class SudokuSolver:
    def __init__(self, fp: str) -> None:
        self.init_states = []

        with open(fp) as f:
            line = f.readline()
            while line:
                state = []
                for i in range(0,rows*cols,rows):
                    state.append(list(map(lambda c: 0 if c == '.' else int(c), line[i:i+9])))
                self.init_states.append(state)
                line = f.readline()

        # for s in self.init_states:
        #     print(*s, sep='\n')
        #     print('------------------------')  
            
    def solve(self, state_index: int) -> list:
        # if solnum == 1:
        cnf = self.min_one_val_cnf(state_index) + self.max_one_val_cnf(state_index) + self.row_cnf(state_index) + self.col_cnf(state_index) + self.smaller_block_cnf(state_index)
        print("Clauses:", len(cnf))
        solved_cnf = pycosat.solve(cnf)
        # print(solved_cnf)
        return list(filter(lambda x: x > 0,solved_cnf))
    
        # sols = []
        # for sol in pycosat.itersolve(cnf):
        #     sols.append(sol)
    
        return list(pycosat.itersolve(cnf))


    def print_board_from_cnf(self, state_index: int, cnf_solved: list[int]):
        board = deepcopy(self.init_states[state_index])
        for prop_var in cnf_solved:
            row, col, val = str(prop_var)
            board[int(row) - 1][int(col) - 1] = int(val)
        
        print(*board, sep='\n')
        return board

# cnf = [[1,-2,3],[-1,2,3],[1,2,-3]]
# get_pyco_out(cnf)

    def min_one_val_cnf(self, state_index: int) -> list[list]:
        cnf = []
        for row in range(1,rows + 1):
            for col in range(1,cols + 1):
                li = []
                value_already_present = False
                for val in range(1,rows + 1):
                    if self.init_states[state_index][row - 1][col - 1] == val:
                        value_already_present = True
                        break
                    li.append(int(str(row)+str(col)+str(val)))
                if not value_already_present: cnf.append(li)
        return cnf

    def max_one_val_cnf(self, state_index: int) -> list[list]:
        cnf = []
        for row in range(1,rows + 1):
            for col in range(1,cols + 1):
                for val1 in range(1,rows + 1):
                    for val2 in range(val1 + 1,rows + 1):
                        li = []
                        if self.init_states[state_index][row - 1][col - 1] != val1: li.append(-int(str(row)+str(col)+str(val1)))
                        if self.init_states[state_index][row - 1][col - 1] != val2: li.append(-int(str(row)+str(col)+str(val2)))
                        if li: cnf.append(li)
        return cnf

    def row_cnf(self, state_index: int) -> list[list]:
        cnf = []
        for row in range(1,rows + 1):
            for val in range(1,rows + 1):
                li = []
                value_already_present = False
                for col in range(1,cols + 1):
                    if self.init_states[state_index][row - 1][col - 1] == val:
                        value_already_present = True
                        break
                    li.append(int(str(row)+str(col)+str(val)))
                if not value_already_present: cnf.append(li)
        return cnf

    def col_cnf(self, state_index: int) -> list[list]:
        cnf = []
        for col in range(1,cols + 1):
            for val in range(1,rows + 1):
                li = []
                value_already_present = False
                for row in range(1,rows + 1):
                    if self.init_states[state_index][row - 1][col - 1] == val:
                        value_already_present = True
                        break
                    li.append(int(str(row)+str(col)+str(val)))
                if not value_already_present: cnf.append(li)
        return cnf

    def smaller_block_cnf(self, state_index: int) -> list[list]:
        cnf = []
        for col in range(1,cols + 1,3):
            for val in range(1,rows + 1):
                for row in range(1,rows + 1,3):
                    li = []
                    value_already_present = False
                    for i in range(3):
                        for j in range(3):
                            if self.init_states[state_index][row + i - 1][col + j - 1] == val:
                                value_already_present = True
                                break
                            li.append(int(str(row + i)+str(col + j)+str(val)))
                        if value_already_present: break
                    if value_already_present: li = []
                    if li: cnf.append(li)
        return cnf


# print((min_one_val_cnf()))
# print(len(max_one_val_cnf())) #last
# print(len(row_cnf()))
# print(len(col_cnf()))
# print(len(smaller_block_cnf()))

# fin_cnf = min_one_val_cnf() + max_one_val_cnf() + row_cnf() + col_cnf() + smaller_block_cnf()

# print(len(fin_cnf))
# sols_min_one = get_pyco_out(fin_cnf)
# print(*filter(lambda x: x > 0, sols_min_one))

# sols_min_one = [i for i in get_pyco_out(min_one_val_cnf()) if 100 <= abs(i) < 1000 and '0' not in str(abs(i))]
# sols_max_one = [i for i in get_pyco_out(max_one_val_cnf()) if 100 <= abs(i) < 1000 and '0' not in str(abs(i))]
# sols_row = get_pyco_out(row_cnf())
# sols_col = get_pyco_out(col_cnf())
# sols_smaller_block = get_pyco_out(smaller_block_cnf())


# print(sols_max_one)
# sol = []
# for i in sols_min_one:
#     if i in sols_max_one:
#         sol.append(i)

# print(sol)


if __name__ == '__main__':
    import sys
    import validator
    ss = SudokuSolver('p.txt')
    for i in range(len(ss.init_states)):
        print("Solving: ", i)
        ans = ss.solve(i)
        solved_board = ss.print_board_from_cnf(i, ans)
        print(validator.isValidSudoku(solved_board))
    
    # print(ans)