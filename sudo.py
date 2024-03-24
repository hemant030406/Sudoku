rows,cols = (9,9)

def generate_init_states(filename: str) -> None:
    init_states = []

    with open(filename) as f:
        line = f.readline()
        while line:
            state = []
            for i in range(0,rows*cols,rows):
                state.append(line[i:i+8])
            init_states.append(state)
            line = f.readline()

    # for li in init_states:
    #     print(li)
            
def get_pyco_out(cnf: list[list],solnum: int) -> list:
    import pycosat
    if solnum == 1:
        return pycosat.solve(cnf)
    
    sols = []
    for sol in pycosat.itersolve(cnf):
        sols.append(sol)
    
    return sols[:solnum + 1]

cnf = [[1,-2,3],[-1,2,3],[1,2,-3]]
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
    return cnf

def col_cnf() -> list[list]:
    cnf = []
    return cnf


# print(min_one_val_cnf())

# if __name__ == '__main__':
#     import sys 
#     generate_init_states(sys.argv[1])
        