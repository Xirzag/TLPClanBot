import random
from TlpMap import TlpMap
from MapPainter import Painter, Writer
from TlpMapLoader import create_tlp_map


def print_map(tlp_map, battle, attacker_clan=None, victim_clan=None):
    print("Batalla {} -----".format(battle))
    # tlp_map.print()

    painter = Painter(tlp_map)
    painter.paint(attacker_clan, victim_clan)
    painter.save_png('battle{}'.format(battle + 1))

    writer = Writer(tlp_map)
    if attacker_clan is None and victim_clan is None:
        writer.win_message(tlp_map.get_clans()[0], battle)
    else:
        writer.generate_message(attacker_clan, victim_clan, battle)

    writer.close()


def do_battle(tlp_map, battle):

    attacker_clan = tlp_map.clan_in_position(tlp_map.random_table())
    victim_clan = random.choice(tlp_map.get_near_clans(attacker_clan))

    print_map(tlp_map, battle, attacker_clan, victim_clan)

    victim_table_pos = tlp_map.find_clan_positions(victim_clan)
    updated_grid = tlp_map.get_grid()

    for position in victim_table_pos:
        updated_grid[position['row']][position['col']] = attacker_clan

    tlp_map = TlpMap(updated_grid)

    battle += 1

    return tlp_map, battle


def __main__():
    '''tlp_map = TlpMap([['Yonks', 'Yonks', 'Yonks', 'Yonks'],
                  ['Sixtolo', 'Sixtolo', 'Bananero', 'Bananero'],
                  ['Sixtolo', 'Sixtolo', 'Crespo', 'Bananero']])'''

    tlp_map = create_tlp_map('clanesasientos.csv')

    battle = 0
    while tlp_map.clans_amount() is not 1:
        tlp_map, battle = do_battle(tlp_map, battle)

    print_map(tlp_map, battle)


__main__()