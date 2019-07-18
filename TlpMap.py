import random

class TlpMap:

    def __init__(self, grid):
        self.grid = grid

    def get_clans(self):
        clans = []
        for row in self.grid:
            for cell in row:
                if cell not in clans:
                    clans.append(cell)

        return clans

    def get_grid(self):
        return self.grid

    def clan_in(self, row, col):
        return self.grid[row][col]

    def random_table(self):
        table = None
        pos = None
        while table is None:
            dim = self.dimensions()
            pos = {'row': random.randint(0, dim['rows'] - 1), 'col': random.randint(0, dim['cols'] - 1)}
            table = self.clan_in_position(pos)

        return pos

    def clan_in_position(self, position):
        return self.clan_in(position['row'], position['col'])

    def clans_amount(self):
        return len(self.get_clans())

    def find_clan_positions(self, clan):
        positions = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell is clan:
                    positions.append({'row': i, 'col': j})

        return positions

    @staticmethod
    def position_offset(pos, offset):
        return {'row': pos['row'] + offset['row'], 'col': pos['col'] + offset['col']}

    @staticmethod
    def is_a_clan(clan):
        return clan is not None

    def is_a_table(self, pos):
        return self.is_a_clan(self.clan_in(pos['row'], pos['col']))

    def dimensions(self):
        return {'rows': len(self.grid), 'cols': len(self.grid[0])}

    def get_near_clans(self, clan):
        clan_positions = self.find_clan_positions(clan)
        near_clans = []
        dims = self.dimensions()
        for position in clan_positions:
            if position['row'] is not 0:
                near_clan = self.clan_in_position(TlpMap.position_offset(position, {'row': -1, 'col': 0}))
                if clan is not near_clan and TlpMap.is_a_clan(near_clan) and near_clan not in near_clans:
                    near_clans.append(near_clan)

            if position['col'] is not 0:
                near_clan = self.clan_in_position(TlpMap.position_offset(position, {'row': 0, 'col': -1}))
                if clan is not near_clan and TlpMap.is_a_clan(near_clan) and near_clan not in near_clans:
                    near_clans.append(near_clan)

            if position['row'] is not dims['rows'] - 1:
                near_clan = self.clan_in_position(TlpMap.position_offset(position, {'row': 1, 'col': 0}))
                if clan is not near_clan and TlpMap.is_a_clan(near_clan) and near_clan not in near_clans:
                    near_clans.append(near_clan)

            if position['col'] is not dims['cols'] - 1:
                near_clan = self.clan_in_position(TlpMap.position_offset(position, {'row': 0, 'col': 1}))
                if clan is not near_clan and TlpMap.is_a_clan(near_clan) and near_clan not in near_clans:
                    near_clans.append(near_clan)

        return near_clans

    def print(self):
        for row in self.grid:
            print([cell for cell in row])