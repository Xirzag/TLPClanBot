import csv
from TlpMap import TlpMap


def create_tlp_map(name):
    grid = matrix = [[None for i in range(16 + 10 + 10 + 16)] for i in range(40)]
    with open(name, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            fill_grid(grid, row[0], row[1], row[2], row[3])

    return TlpMap(grid)


def fill_grid(grid, clan, zone, row, col):
    row = int(row)
    col = int(col)

    # print(clan, zone, row, col)
    if zone is 'A':
        grid[row - 1][col - 1] = clan
    elif zone is 'B':
        grid[row][10 - col + 16] = clan
    elif zone is 'C':
        grid[row][10 + 16 + col - 1] = clan
    elif zone is 'D':
        grid[row - 1][10 + 16 + 10 + 16 - col] = clan


# print(create_tlp_map('clanesasientos.csv'))