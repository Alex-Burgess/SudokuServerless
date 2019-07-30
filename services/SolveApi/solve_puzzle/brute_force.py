# import sys
# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler(sys.stdout)
# logger.addHandler(stream_handler)


def solve_wrapper(s):
    s = convert_to_bf(s)
    # logger.info("Executing brute force algorithm.  Puzzle ({})".format(s))
    s = solve(s)
    s = convert_from_bf(s)

    # logger.info("Puzzle solved by brute force.  Solution ({})".format(s))
    return {'puzzle': s, 'status': True}


def solve(s):
    '''
    Solve a Sudoku:

    - Accepts s, a sequence of 81 integers from 0 to 9 in row of
    column order, zeros indicating the cells to fill.

    - Returns the first found solution as a sequence of 81 integers in
    the 1 to 9 interval (same row or column order than input), or None
    if no solution exists.
    '''
    try:
        i = s.index(0)
    except ValueError:
        # No empty cell left: solution found
        return s

    c = [s[j] for j in range(81)
         if not ((i-j) % 9 * (i//9 ^ j//9) * (i//27 ^ j//27 | (i % 9//3 ^ j % 9//3)))]

    for v in range(1, 10):
        if v not in c:
            r = solve(s[:i]+[v]+s[i+1:])
            if r is not None:
                return r


def convert_to_bf(s):
    new_list = []
    for row in s:
        for cell in row:
            new_list.append(cell)

    return new_list


def convert_from_bf(s):
    new_list = []

    counter = 0
    tmp_list = []

    for value in s:
        if counter < 8:
            tmp_list.append(value)
            counter += 1
        else:
            tmp_list.append(value)
            new_list.append(tmp_list)
            tmp_list = []
            counter = 0

    return new_list
