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
        
        self.clause_map = tuple({} for _ in range(len(self.init_states)))
        self.clause_list = tuple([] for _ in range(len(self.init_states))) 

        # for s in self.init_states:
        #     print(*s, sep='\n')
        #     print('------------------------')  

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
        # if solnum == 1:
        start = time.time()
        cnf = self.min_one_val_cnf(state_index) + self.col_cnf(state_index) + self.row_cnf(state_index) + self.smaller_block_cnf(state_index) + self.max_one_val_cnf(state_index)
        print("Clauses:", len(cnf))
        new_cnf = self.cnf_prop_var_preproc(state_index, cnf)
        self.generate_time += (start2 := time.time()) - start
        # print(new_cnf)
        solved_cnf = pycosat.solve(new_cnf)
        # print(solved_cnf)
        self.solve_time += time.time() - start2
        return list(filter(lambda x: x > 0,solved_cnf))
    
        # sols = []
        # for sol in pycosat.itersolve(cnf):
        #     sols.append(sol)
    
        return list(pycosat.itersolve(cnf))


    def print_board_from_cnf(self, state_index: int, cnf_solved: list[int]):
        board = deepcopy(self.init_states[state_index])
        for prop_var in cnf_solved:
            row, col, val = str(self.clause_list[state_index][prop_var - 1])
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
                # if (val := self.init_states[state_index][row - 1][col - 1]):
                #     for v in range(1, rows + 1):
                #         if v == val: continue
                #         cnf.append([-int(str(row)+str(col)+str(v))])
                    # cnf.append(l)
                for val1 in range(1,rows + 1):
                    for val2 in range(val1 + 1,rows + 1):
                        li = []
                        # li.append(-int(str(row)+str(col)+str(val1)))
                        # li.append(-int(str(row)+str(col)+str(val2)))
                        # cnf.append(li)
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


def main():
    ss = SudokuSolver('p.txt')
    for i in range(len(ss.init_states)):
        print("Solving: ", i)
        ans = ss.solve(i)
        solved_board = ss.print_board_from_cnf(i, ans)
        # if not (validator.isValidSudoku(solved_board)):
        #     print(":AWDAWDAWDAHWKJLDHAKLWJDHLAKWJHDLAKWJDHALWKJH")
        #     quit()
        # else: print("PASSED")
    print(f"{ss.generate_time = }")
    print(f"{ss.solve_time = }")

def solve_for1():
    ss = SudokuSolver('p.txt')
    ss.solve(0)

    # print(ans)
if __name__ == '__main__':
    main()
    # solve_for1()