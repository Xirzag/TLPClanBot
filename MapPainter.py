from TlpMap import TlpMap
import os
import random
import xml.etree.ElementTree as ET
import os
import cairosvg


class Painter:
    clan_colors = None

    def __init__(self, map):
        self.table_dim = 15
        self.xml = self.create_xml()
        self.map = map
        if Painter.clan_colors is None:
            Painter.clan_colors = self.generate_colors()

    def create_xml(self):
        svg_file = open('tlp_start.svg', 'r', encoding='utf-8')
        svg = svg_file.read()
        svg_file.close()
        return ET.fromstring(svg)

    @staticmethod
    def random_hsl():
        return 'rgb({}, {}, {})'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def find_id(self, id):
        return self.xml.find(".//*[@id='{}']".format(id))

    def generate_colors(self):
        clan_colors = {}
        for clan in self.map.get_clans():
            clan_colors[clan] = self.random_hsl()

        return clan_colors

    def paint(self, attacker_clan=None, victim_clan=None):
        if attacker_clan is not None and victim_clan is not None:
            pattern_layer = self.find_id('Words')
            pattern_layer.insert(1, self.create_pattern(attacker_clan, victim_clan))
            clan_text_layer = self.find_id('Clan Text')
            clan_text_layer.insert(0, self.paint_clan_text(victim_clan))
            clan_text_layer.insert(0, self.paint_clan_text(attacker_clan))

        dim = self.map.dimensions()
        for row in range(dim['rows']):
            for col in range(dim['cols']):
                painted_clan = self.map.clan_in(row, col)
                if self.map.is_a_clan(painted_clan):
                    if painted_clan == attacker_clan:
                        table_layer_name = 'Attacker Tables'
                    elif painted_clan == victim_clan:
                        table_layer_name = 'Victim Tables'
                    else:
                        table_layer_name = 'Tables'
                    table_layer = self.find_id(table_layer_name)

                    table_layer.insert(1, self.print_table(row, col, painted_clan,
                                                        attacker_clan if painted_clan == attacker_clan else None,
                                                        victim_clan if painted_clan == victim_clan else None))

    def paint_clan_text(self, clan):
        positions = self.map.find_clan_positions(clan)
        meanX = 0
        meanY = 0
        for pos in positions:
            x, y = self.table_pos(pos['row'], pos['col'])
            meanY += y
            meanX += x

        meanX = meanX / len(positions)
        meanY = meanY / len(positions)

        clan_text = '''
        <text
             style="font-style:normal;font-weight:normal;font-size:18px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:black;fill-opacity:1;stroke:none;stroke-width:0.26458332"
             x="0"
             y="0"
             id="text4564"><tspan
               id="tspan4562"
               x="{}"
               y="{}"
               style="font-style:italic;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold Italic';fill:black;fill-opacity:1;stroke-width:0.26458332">{}</tspan></text>
        ''' .format(meanX - len(clan) / 4 * 18, meanY + 18 / 2, clan)
        return ET.fromstring(clan_text)

    def get_clan_color(self, clan):
        return Painter.clan_colors[clan]

    def table_pos(self, row, col):
        y = 120 + row * self.table_dim
        x = 30 + col * self.table_dim

        if col > 16:
            x += self.table_dim * 2
        if col > 26:
            x += self.table_dim * 6
        if col > 36:
            x += self.table_dim * 2

        if row > 12:
            y += self.table_dim * 2
        if row > 25:
            y += self.table_dim * 2

        return x, y

    def print_table(self, row, col, clan, victim, attacker):

        if attacker is not None:
            stroke_color = 'green'
        elif victim is not None:
            stroke_color = 'red'
        else:
            stroke_color = 'white'

        x, y = self.table_pos(row, col)

        table = '''<rect id="{}" width="{}" height="{}" x="{}" y="{}"
                style="fill:{};stroke-width:{};stroke:{}" />''' \
            .format('{}-{}'.format(col, row), self.table_dim, self.table_dim,
                    x, y,
                    self.get_clan_color(clan) if attacker is None else 'url(#attack_pattern)',
                    '4' if attacker is None or victim is None else 1,
                    stroke_color)
        return ET.fromstring(table)

    def svg_to_png(self, file, output, width=1024, use_inkscape=False):
        if use_inkscape:
            if os.name == 'nt':
                cmd = '"C:\Program Files\Inkscape\inkscape" -z -e {1} -w {2} {0}'.format(file, output, width)
            else:
                cmd = "inkscape -z -e {1} -w {2} {0}".format(file, output, width)
            print(cmd)
            os.system(cmd)
        else:
            cairosvg.svg2png(url=file, write_to=output)

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
            <line x1="0" y1="0" x2="0" y2="3" style="stroke:{}; stroke-width:3.5; stroke-opcaity:0.75" />
        </pattern>'''.format(self.get_clan_color(attacker_clan), self.get_clan_color(victim_clan))

        return ET.fromstring(pattern)


class Writer:

    def __init__(self, map):
        self.map = map
        self.file = open("tweets.txt", "a", encoding='utf-8')

    def write(self, msg):
        self.file.write(msg + ';\n')
        self.file.flush()

    def generate_message(self, attacker, victim, battle):
        self.write(
            '''Batalla {}
{} ha derrotado al clan {}'''.format(battle + 1, attacker, victim))

    def close(self):
        self.file.close()

    def win_message(self, winner_clan, battle):
        self.write('''El clan {} ha ganado el TLP War Bot'''.format(winner_clan))

    @staticmethod
    def clean():
        file = open("tweets.txt", "w", encoding='utf-8')
        file.close()




ET.register_namespace("", "http://www.w3.org/2000/svg")