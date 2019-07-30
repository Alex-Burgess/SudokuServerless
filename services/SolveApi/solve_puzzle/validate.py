from solve_puzzle import common
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.handlers:
    handler = logger.handlers[0]
    handler.setFormatter(logging.Formatter("[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(module)s:%(funcName)s\t%(message)s\n", "%Y-%m-%dT%H:%M:%S"))


def validate_puzzle(puzzle):
    logger.info("Validating puzzle for incorrect format ({})".format(puzzle))

    for r in range(0, 9):
        row = puzzle[r]
        if not validate_row_col_grid(row, "row"):
            return False

    for c in range(0, 9):
        column = common.get_column(puzzle, c)
        if not validate_row_col_grid(column, "column"):
            return False

    for g in range(0, 9):
        grid = common.get_grid(puzzle, g)
        if not validate_row_col_grid(grid, "grid"):
            return False

    return True


def validata_data_types(puzzle):
    logger.info("Validating puzzle for incorrect data types ({})".format(puzzle))
    for r in range(0, 9):
        row = puzzle[r]
        for x in row:
            if not isinstance(x, int):
                logger.error("Puzzle failed data type validation.")
                return False
    return True


def validate_row_col_grid(number_list, type):
    logger.debug("INFO: Validating {} ({})".format(type, number_list))
    max_cell_value_occurences = 1
    for x in range(1, 10):
        if number_list.count(x) > max_cell_value_occurences:
            logger.error("Number (" + str(x) + ") occurred more than once in row (" + str(number_list) + ")")
            return False

    logger.debug("No duplicates found in {} ({})".format(type, number_list))
    return True
