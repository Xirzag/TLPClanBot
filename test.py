from TlpMap import TlpMap
from MapPainter import Painter

map = TlpMap([['Yonks', 'Yonks', 'Yonks', 'Yonks'],
              ['Sixtolo', 'Sixtolo', 'Bananero', 'Bananero'],
              ['Sixtolo', 'Sixtolo', 'Crespo', 'Bananero']])

map.print()

painter = Painter(map, {'Yonks': 'red', 'Bananero': 'green', 'Sixtolo': 'blue', 'Crespo': 'orange'});
painter.show_code()
painter.save_svg('try.svg')