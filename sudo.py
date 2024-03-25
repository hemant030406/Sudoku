rows,cols = (9,9)
init_states = []

def generate_init_states(filename: str) -> None:

    with open(filename) as f:
        line = f.readline()
        while line:
            state = []
            for i in range(0,rows*cols,rows):
                state.append(line[i:i+8])
            init_states.append(state)
            line = f.readline()

    for li in init_states:
        print(li)
        break
            
def get_pyco_out(cnf: list[list]) -> list:
    import pycosat
    # if solnum == 1:
    return pycosat.solve(cnf)
    
    # sols = []
    # for sol in pycosat.itersolve(cnf):
    #     sols.append(sol)
    
    return list(pycosat.itersolve(cnf))

# cnf = [[1,-2,3],[-1,2,3],[1,2,-3]]
# get_pyco_out(cnf)

def min_one_val_cnf() -> list[list]:
    cnf = []
    for row in range(1,rows + 1):
        for col in range(1,cols + 1):
            li = []
            for val in range(1,rows + 1):
                li.append(int(str(row)+str(col)+str(val)))
            cnf.append(li)
    return cnf

def max_one_val_cnf() -> list[list]:
    cnf = []
    for row in range(1,rows + 1):
        for col in range(1,cols + 1):
            for val1 in range(1,rows + 1):
                for val2 in range(val1 + 1,rows + 1):
                    li = []
                    li.append(-int(str(row)+str(col)+str(val1)))
                    li.append(-int(str(row)+str(col)+str(val2)))
                    cnf.append(li)
    return cnf

def row_cnf() -> list[list]:
    cnf = []
    for row in range(1,rows + 1):
        for val in range(1,rows + 1):
            li = []
            for col in range(1,cols + 1):
                li.append(int(str(row)+str(col)+str(val)))
            cnf.append(li)
    return cnf

def col_cnf() -> list[list]:
    cnf = []
    for col in range(1,cols + 1):
        for val in range(1,rows + 1):
            li = []
            for row in range(1,rows + 1):
                li.append(int(str(row)+str(col)+str(val)))
            cnf.append(li)
    return cnf

def smaller_block_cnf() -> list[list]:
    cnf = []
    for col in range(1,cols + 1,3):
        for val in range(1,rows + 1):
            for row in range(1,rows + 1,3):
                li = []
                for i in range(3):
                    for j in range(3):
                        li.append(int(str(row + i)+str(col + j)+str(val)))
                cnf.append(li)
    return cnf


# print((min_one_val_cnf()))
# print(len(max_one_val_cnf())) #last
# print(len(row_cnf()))
# print(len(col_cnf()))
# print(len(smaller_block_cnf()))

fin_cnf = min_one_val_cnf() + max_one_val_cnf() + row_cnf() + col_cnf() + smaller_block_cnf()

print(len(fin_cnf))

# sols_min_one = [i for i in get_pyco_out(min_one_val_cnf()) if 100 <= abs(i) < 1000 and '0' not in str(abs(i))]
# sols_max_one = [i for i in get_pyco_out(max_one_val_cnf()) if 100 <= abs(i) < 1000 and '0' not in str(abs(i))]
# sols_row = get_pyco_out(row_cnf())
# sols_col = get_pyco_out(col_cnf())
# sols_smaller_block = get_pyco_out(smaller_block_cnf())

sols_min_one = get_pyco_out(fin_cnf)
print(*filter(lambda x: x > 0, sols_min_one))

# print(sols_max_one)
# sol = []
# for i in sols_min_one:
#     if i in sols_max_one:
#         sol.append(i)

# print(sol)


if __name__ == '__main__':
    import sys 
    generate_init_states(sys.argv[1])


        