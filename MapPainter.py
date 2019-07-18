from TlpMap import TlpMap
import os
import random
import xml.etree.ElementTree as ET
import os


class Painter:

    def __init__(self, map):
        self.table_dim = 20
        self.xml = self.create_xml()
        self.map = map
        self.clan_colors = self.generate_colors()

    def create_xml(self):
        svg = '''<?xml version="1.0"?>
        <svg width="1500" height="1500"
             viewBox="0 0 1500 1500"
             xmlns="http://www.w3.org/2000/svg">
         </svg>
        '''
        return ET.fromstring(svg)

    @staticmethod
    def random_hsl():
        return 'rgb({}, {}, {})'.format(random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))

    def generate_colors(self):
        clan_colors = {}
        for clan in self.map.get_clans():
            clan_colors[clan] = self.random_hsl()

        return clan_colors

    def paint(self, attacker_clan = None, victim_clan = None):
        if attacker_clan is not None and victim_clan is not None:
            self.xml.insert(0, self.create_pattern(attacker_clan, victim_clan))

        dim = self.map.dimensions()
        for row in range(dim['rows']):
            for col in range(dim['cols']):
                painted_clan = self.map.clan_in(row, col)
                if self.map.is_a_clan(painted_clan):
                    self.xml.insert(0, self.print_table(row, col, painted_clan,
                                                attacker_clan if painted_clan is victim_clan else None))

    def get_clan_color(self, clan):
        return self.clan_colors[clan]

    def print_table(self, row, col, clan, attacker):
        table = '''<rect id="{}" width="{}" height="{}" x="{}" y="{}"
                style="fill:{};stroke-width:1;stroke:{}"></rect>'''\
            .format('{}-{}'.format(col, row), self.table_dim, self.table_dim,
                    col * self.table_dim, row * self.table_dim,
                    self.get_clan_color(clan) if attacker is None else 'url(#attack_pattern)',
                    'white' if attacker is None else self.get_clan_color(attacker))
        return ET.fromstring(table)

    def svg_to_png(self, file, output, width=1024):
        if os.name == 'nt':
            cmd = '"C:\Program Files\Inkscape\inkscape" -z -e {1} -w {2} {0}'.format(file, output, width)
        else:
            cmd = "inkscape -z -e {1} -w {2} {0}".format(file, output, width)
        print(cmd)
        os.system(cmd)

    @staticmethod
    def load_svg(file):
        tree = ET.parse(file)
        return tree.getroot()

    def save_svg(self, name):
        tree = ET.ElementTree(self.xml)
        tree.write(name)
        return name

    @staticmethod
    def remove_file(file):
        if os.name == 'nt':
            cmd = "del {0}".format(file)
        else:
            cmd = "rm {0}".format(file)
        os.system(cmd)

    def save_png(self, name):
        self.save_svg(name + '.svg')
        self.svg_to_png(name + '.svg', name + '.png')
        # self.remove_file(name + '.svg')

    def show_code(self):
        print(ET.tostring(self.xml))

    def create_pattern(self, attacker_clan, victim_clan):
        pattern = '''<pattern id="attack_pattern" width="3" height="3" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <rect  width="3" height="3" style="fill:{};" />
            <line x1="0" y1="0" x2="0" y2="3" style="stroke:{}; stroke-width:1.5; stroke-opcaity:0.75" />
        </pattern>'''.format(self.get_clan_color(attacker_clan), self.get_clan_color(victim_clan))

        return ET.fromstring(pattern)


class Writer:

    def __init__(self, map):
        self.map = map
        self.file = open("tweets.txt", "a")

    def write(self, msg):
        self.file.write(msg + ';\n')
        self.file.flush()

    def generate_message(self, attacker, victim, battle):
        self.write(
'''Batalla {}
{} ha derrotado a {}'''.format(battle +1, attacker, victim))

    def close(self):
        self.file.close()

    def win_message(self, winner_clan, battle):
        self.write('''El clan {} ha ganado el TLP War Bot'''.format(winner_clan))


ET.register_namespace("", "http://www.w3.org/2000/svg")