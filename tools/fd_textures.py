"""Генератор текстур блюд Stardew Delight в стиле Farmer's Delight.

Каждое блюдо = тара (глубокая миска / широкая миска-тарелка / стеклянная кружка / ничего)
+ пиксельный шаблон еды 16x16 + цвета блюда. Палитра тары взята из Farmer's Delight,
цвета еды раскладываются в рампу (контур -> тень -> база -> свет -> блик) со сдвигом
оттенка: тени уходят в холодное/красное, блики в тёплое — как у текстур FD.

Запуск:
    py tools/fd_textures.py                 # перезаписать текстуры мода
    py tools/fd_textures.py <папка>         # записать в другую папку
    py tools/fd_textures.py <папка> --sheet sheet.png   # плюс сводный лист для проверки
"""
import colorsys, os, sys
# Pillow импортируется внутри функций рисования: tools/gen.py берёт отсюда только таблицу DISHES и работает без него.

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, 'src/main/resources/assets/stardewdelight/textures/item')

# ======================================================================================
#  Шаблоны.  Символы:
#   O          контур основного цвета (тон зависит от положения: сверху-слева светлее)
#   Z          глубокая тень основного цвета (ровная, без учёта положения)
#   D B L H    тень / база / свет / блик основного цвета
#   q w e      гарнир 1 (тень, база, свет)      r t y  гарнир 2
#   u i o      гарнир 3                          z x c  гарнир 4
#   f g h      зелень (тёмная, средняя, светлая) — общая палитра
#   a s d      белое: рис, сливки, белок (тень, база, свет)
#   v b        желток (свет, тень)
#   K M N P Q R Y W   дерево миски (палитра FD), W — дно широкой миски
#   j k l m    стекло (палитра FD)
#   .          прозрачно
# ======================================================================================

CONTAINERS = {
    # глубокая миска: супы, рагу, салаты, пудинги (как vegetable_soup / mixed_salad в FD)
    'deep': [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "..K..........N..",
        "..KN........RQ..",
        "..KMN.NRR.MRNQ..",
        "...PMMMMMYNNQ...",
        "....QQNMMNQQ....",
        "......QQQQ......",
        "................",
        "................",
        "................",
    ],
    # широкая миска: плотные вторые блюда (как steak_and_potatoes / grilled_salmon в FD)
    'wide': [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "KN............NK",
        "KMN..........NNQ",
        ".KM.........NNQ.",
        "..KKNMWWWMMNQQ..",
        "....KKQQQQQQ....",
        "................",
        "................",
    ],
    # стеклянная кружка с ручкой (как напитки FD)
    'glass': [
        "................",
        "................",
        "................",
        "................",
        "....lmmmmmm.....",
        "...mk.....kl....",
        "....mllmmlk.....",
        "....m.....kjjk..",
        "....m.....j...k.",
        "...m.......j..k.",
        "...m.......j.k..",
        "...l.......jj...",
        "...k.......j....",
        "....k.....j.....",
        ".....kjjjj......",
        "................",
    ],
}

FOOD = {}

# ---------------- глубокая миска (строки 0..9, строка 9 почти закрыта краем миски) ----------------
FOOD['soup'] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....OOOOOO.....",
    "...OODBBLLBDO...",
    "...BLHLBBwBBBD..",
    "...DBLBBqwBeBD..",
    "...DDBBBBBBDD...",
]
FOOD['soup_chunky'] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....OOOOOO.....",
    "...OODwBLBtDO...",
    "...BLHqweBrtBD..",
    "...DBeBwBtyBwD..",
    "...DDBBtBBBDD...",
]
FOOD['soup_cream'] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....OOOOOO.....",
    "...OODBLLLBDO...",
    "...BLHweeLBBBD..",
    "...DBLBwwBBBBD..",
    "...DDBBBBBBDD...",
]
FOOD['heap'] = [
    "................",
    "................",
    "................",
    "......OOOO......",
    "....OODBBDOO....",
    "...OBLwBBtBBO...",
    "...BLHqweBryBD..",
    "...BwBBBtBwBBD..",
    "...DqBtrBBqBDD..",
    "...DDBBBBBBDD...",
]
FOOD['salad'] = [
    "................",
    "................",
    "................",
    "......OO..O.....",
    "..OO.OLHO.OLO...",
    ".OLBOBLBBOBLBO..",
    "..OBwBtBLBeBwBO.",
    "...BwqBtyBBwBD..",
    "...DBwBBBtBBDD..",
    "...DDBBBBBBDD...",
]
FOOD['mound'] = [
    "................",
    "................",
    "................",
    "................",
    "......OOOO......",
    "....OOLHHLOO....",
    "...OBLHLLBBBO...",
    "...BLBBBBBBBBD..",
    "...DBBBBBBBBDD..",
    "...DDBBBBBBDD...",
]
FOOD['pudding'] = [
    "................",
    "................",
    "......OOOO......",
    "....OODLLBOO....",
    "...ODLHHLBBDO...",
    "...DBLLBBBBDO...",
    "...DBBBBBBBDO...",
    "...ODBBBBBDDO...",
    "....OODDDDOO....",
    "................",
]
FOOD['icecream'] = [
    "................",
    "................",
    "......OOOO......",
    ".....OLHLBO.....",
    "..rrrOBLBBOqq...",
    ".rtyyrOOOOqwwq..",
    ".rtytyrBBqweewq.",
    "..rtttrBBqwwwq..",
    "...rrrDBBDqqq...",
    "...DDBBBBBBDD...",
]
FOOD['cocktail'] = [
    "................",
    "................",
    "..qq........qq..",
    ".qwwq......qwwq.",
    ".qweq.OOOO.qewq.",
    "..qwqOBLHBOqwq..",
    "...qOBLBBBBOq...",
    "...DBBBBBBBBD...",
    "...DBBBBBBBBD...",
    "...DDBBBBBBDD...",
]

# ---------------- широкая миска (строки 0..11, нижние закрыты бортом) ----------------
FOOD['pl_main_side'] = [
    "................",
    "................",
    "................",
    "......OO..rrr...",
    "...OOOLHOrtyyr..",
    "..OBLHBBOrtyttr.",
    ".OBLBBBBOrtttyr.",
    ".OBBBBwBOrttttr.",
    ".ODBBwqBOrtttrr.",
    "..ODBBBOqqrrrr..",
    "...ODDOgfhqq....",
    "....OO.fghf.....",
]
FOOD['pl_fish'] = [
    "................",
    "................",
    "................",
    "..........OOO...",
    "........OOLHBO..",
    "......OOLHLBBO..",
    "....OOLHLBBBDO..",
    "..OOLHLBBBBDO...",
    ".OLHLBBBBBDDOww.",
    "..OBBBBBDDOOwewq",
    "...OODDOOghfqwq.",
    "........fhgf....",
]
FOOD['pl_fried'] = [
    "................",
    "................",
    "................",
    "................",
    "...OOOO.........",
    "..OLHLBO.OOOO...",
    "..OBLBBOOLHLBO..",
    "...OBBDOOBLBBDO.",
    "....OOOOOBBBDO..",
    "..OOOO.qOODOO...",
    ".OLHBDOqwq......",
    "..OODOO.q.......",
]
FOOD['pl_noodles'] = [
    "................",
    "................",
    "................",
    "......OOOO......",
    "....OOLBLBOO....",
    "...OLBLwwBLBO...",
    "..OBLBwewwBLBO..",
    ".OLBLBwwqwBLBLO.",
    ".OBLBLBwqBLBLBO.",
    "..OBLBLBLBLBLO..",
    "...OOBDBDBDOO...",
    "................",
]
FOOD['pl_ravioli'] = [
    "................",
    "................",
    "................",
    "................",
    "....OOOO........",
    "...OLHLBO.OOOO..",
    "...OBLBDOOLHLBO.",
    "..wOODDOwOBLBDO.",
    ".wewOOOOOwODDOw.",
    "..wOLHLBOwOOOOw.",
    "...OBLBDOww.....",
    "....OOOOO.......",
]
FOOD['pl_breakfast'] = [
    "................",
    "................",
    "................",
    "....aaaa........",
    "..aassdsa.OOOO..",
    ".asdsvvsaOLHLBO.",
    ".asdvvbsaOBLBBO.",
    ".aassbsaODDDDDO.",
    "..aaaaaqOLHLBBO.",
    "..qqwwqwqBLBBDO.",
    "...qwewqwODDDO..",
    "....qqqq........",
]
FOOD['pl_mix3'] = [
    "................",
    "................",
    "................",
    ".....OOO........",
    "....OLHBO.rrr...",
    "...OLHLBBOrtyr..",
    "..OBLBBBBOtyttr.",
    ".qqqOBBBDOrtttr.",
    "qwewqODDOrttrr..",
    ".qwwqqOOrrrr....",
    "..qqwq..........",
    "................",
]
FOOD['pl_blobs'] = [
    "................",
    "................",
    "................",
    "................",
    ".....OOO..OOO...",
    "....OLHBOOLHBO..",
    "...OOBBDOOBBDO..",
    "..OLHOOOwOOOOOO.",
    "..OBBDOOLHBOLHBO",
    "..OOOOwOBBDOBBDO",
    "...www.OOOOOOOO.",
    "................",
]
FOOD['pl_dip'] = [
    "................",
    "................",
    "................",
    "....qq..........",
    "...qeeq.........",
    "...qwwq.OOOO....",
    "....qqOOLHLBOO..",
    "...rrOLHLBBBBO..",
    "..rtyrOBBBBBDO..",
    "..rttrODBBBDDO..",
    "...rr..OOOOOO...",
    "................",
]
FOOD['pl_heap'] = [
    "................",
    "................",
    "................",
    "................",
    "......OOOO......",
    "....OOLHLBOO....",
    "...OLHBwBBtBO...",
    "..OLBBqBBBrBBO..",
    ".OBBtBBBwBBBqDO.",
    ".OBwBBrBBBtBBDO.",
    "..ODBBBqBBBDDO..",
    "...OODDDDDDOO...",
]

FOOD['pl_eel'] = [  # две глазированные полоски угря с решёткой гриля
    "................",
    "................",
    "................",
    "................",
    "...OOOOOOOOOO...",
    "..OLHLLBLLBBDO..",
    "..OBqBBqBBqBDO..",
    "..ODDDDDDDDDDO..",
    "..OOOOOOOOOOOO..",
    "..OLHLLBLLBBDO..",
    "..OBqBBqBBqBDO..",
    "...ODDDDDDDDO...",
]
FOOD['pl_sardines'] = [  # две рыбки
    "................",
    "................",
    "................",
    "...OOOOOO..O....",
    "..OLHLBBBOOLO...",
    "..OZBBBDDDODO...",
    "...OOOOOO..O....",
    "....OOOOOO..O...",
    "...OLHLBBBOOLO..",
    "...OZBBBDDDODO..",
    "....OOOOOO..O...",
    "......fghf......",
]
FOOD['pl_fillet'] = [  # филе в панировке + долька лимона
    "................",
    "................",
    "................",
    ".uu.............",
    "uiou.OOOOOOO....",
    "uiiuOLHLLBLBOO..",
    ".uuOLHBqBBqBBBO.",
    "...OBBqBBqBBqBDO",
    "...OBqBBqBBqBBDO",
    "...ODBBBqBBBDDO.",
    "....OODDDDDDOO..",
    "......OOOOOO....",
]
FOOD['pl_wedges'] = [  # запечённые корнеплоды дольками
    "................",
    "................",
    "................",
    "......OOO.......",
    ".....OLHBO.OOO..",
    "..OOOLHBDOOLHBO.",
    ".OLHOOBDDOLHBDO.",
    ".OBBDOOOOOBBDDO.",
    "..ODDOqqqOODDO..",
    "...OOqwewqOOO...",
    "....qwwwwq......",
    ".....qqqq.......",
]

# ---------------- в руках (снеки и сладости) ----------------
FOOD['hash'] = [  # драник: прямоугольник с полосками тёртого картофеля
    "................",
    "................",
    "................",
    "................",
    "................",
    "...OOOOOOOOOO...",
    "..OLHLqLHLqLBO..",
    ".OLHBqBLBqBBBDO.",
    ".OBBqBBBqBBqBDO.",
    ".OBqBBqBBBqBDDO.",
    ".ODBBBqBBqBDDDO.",
    "..ODDDDDDDDDDO..",
    "...OOOOOOOOOO...",
    "................",
    "................",
    "................",
]
FOOD['cookie'] = [
    "................",
    "................",
    ".....OOOOOO.....",
    "...OOBLLBLBOO...",
    "..OBLHLBqBBLBO..",
    ".OBLBBBBBBLBqBO.",
    ".OLHBqBBLBBBBDO.",
    ".OLBBBBLBqBBDDO.",
    ".OBBqBBBBBBDBDO.",
    ".OBBBBBqBBBDDDO.",
    ".ODBBBBBBBDDqDO.",
    "..ODDBBqBDDDDO..",
    "...OODDDDDDOO...",
    ".....OOOOOO.....",
    "................",
    "................",
]
FOOD['slice'] = [
    "................",
    "................",
    "................",
    ".......OOO......",
    ".......OLHOO....",
    "......OewwLBO...",
    ".....OewqwwBO...",
    "....OewwwqwBO...",
    "...OewqwwwBDO...",
    "...OwwwwwBDO....",
    "...OBLLBBDO.....",
    "...OBBBDOO......",
    "...ODDOO........",
    "...OOO..........",
    "................",
    "................",
]
FOOD['cake'] = [
    "................",
    "................",
    "........rt......",
    ".......OyOOO....",
    "......OcxxcxO...",
    ".....OcxxxxxO...",
    "....OcxxxxxDO...",
    "...OxxxxxxDLO...",
    "...OLHLBBDLBO...",
    "...OcxxxxDDO....",
    "...OLHLBBDO.....",
    "...OBBBBDO......",
    "...ODDDOO.......",
    "...OOOO.........",
    "................",
    "................",
]
FOOD['tart'] = [
    "................",
    "................",
    "................",
    "................",
    "....OOOOOOOO....",
    "...OLHLLBLBBO...",
    "..OLwewtwewBDO..",
    "..OBwtwwetwwDO..",
    "..OBewtwwwtBDO..",
    "..OLBwwtwewBDO..",
    "...ODLBBBBDDO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................",
    "................",
]
FOOD['cobbler'] = [
    "................",
    "................",
    "................",
    "................",
    "....OOOOOOOO....",
    "...OLHwLBwLBO...",
    "..OLwewBLweBDO..",
    "..OBBwLBwBBwDO..",
    "..OwBLwewLBBDO..",
    "..OLBBwBBwBDDO..",
    "...ODLBBBBDDO...",
    "....OOOOOOOO....",
    "................",
    "................",
    "................",
    "................",
]
FOOD['muffin'] = [
    "................",
    "................",
    "................",
    ".....OOOOO......",
    "....OLHLBBO.....",
    "...OLHBqBBBO....",
    "...OBqBBBqBO....",
    "...ODBBBqBDO....",
    "....OOOOOOO.....",
    "....OrtrtrO.....",
    "....OtyrtrO.....",
    ".....OtrtO......",
    ".....OOOOO......",
    "................",
    "................",
    "................",
]
FOOD['bar'] = [
    "................",
    "................",
    "................",
    "................",
    "..........OOO...",
    "........OOwweO..",
    "......OOweewwO..",
    "....OOwewwwwqO..",
    "..OOweewwwwqO...",
    ".OwewwwwwqqO....",
    ".OBLBBBBBDO.....",
    "..OOBBDDOO......",
    "....OOOO........",
    "................",
    "................",
    "................",
]
FOOD['candy'] = [
    "................",
    "................",
    "................",
    "..OO......OO....",
    ".OwOO....OOwO...",
    ".OwewOOOOwewO...",
    "..OwOLHLBOwO....",
    "...OLHBBBDO.....",
    "...OBBBBBDO.....",
    "..OwODBBDOwO....",
    ".OwewOOOOwewO...",
    ".OwOO....OOwO...",
    "..OO......OO....",
    "................",
    "................",
    "................",
]
FOOD['burger'] = [
    "................",
    "................",
    "......OOOO......",
    "....OOLHLBOO....",
    "...OLHLBBBBDO...",
    "..OBLBBBBBBBDO..",
    "..ODBBBBBBBDDO..",
    "..qqwqwwqwqwqq..",
    ".ffghhgfghhgff..",
    "..rrtttrttttr...",
    "..OLHBBBBBBDO...",
    "..ODDBBBBDDDO...",
    "...OOOOOOOOO....",
    "................",
    "................",
    "................",
]
FOOD['taco'] = [
    "................",
    "................",
    "................",
    "................",
    "...ggf..rt......",
    "..fhgwwrtyrwg...",
    ".OOwewgtrwewfO..",
    ".OLOwqwwqwwqOBO.",
    ".OLHOOwwwwOOLBO.",
    "..OLHLOOOOLBDO..",
    "...OLLBBBBBDO...",
    "....OOBBBDOO....",
    "......OOOO......",
    "................",
    "................",
    "................",
]
FOOD['wrap'] = [
    "................",
    "................",
    "................",
    "...........OO...",
    ".........OOgfO..",
    "........OLwhgO..",
    "......OOLHrwtO..",
    ".....OLHLBBBDO..",
    "....OLHBBBBDO...",
    "...OLHBBBBDO....",
    "..OLBBBBBDO.....",
    "..OBBBBBDO......",
    "..ODBBDDO.......",
    "...OOOOO........",
    "................",
    "................",
]
FOOD['flat'] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "....OOOOOOOO....",
    "..OOLHLLBLBBOO..",
    ".OLHLBqBBLBBBDO.",
    ".OBLBBBBqBBBBDO.",
    ".OBBqBBBBBBqDDO.",
    "..OODBBBBDDDOO..",
    "....OOOOOOOO....",
    "................",
    "................",
    "................",
    "................",
]
FOOD['pizza'] = [
    "................",
    "................",
    "................",
    ".OOOOOOOOOOO....",
    ".OLHLLBLBBDO....",
    ".OOwwrwwwwwO....",
    "..OwrtrwwwO.....",
    "..OwwrwqwwO.....",
    "...OwwwrtO......",
    "...OwqwtrO......",
    "....OwwwO.......",
    "....OwwO........",
    ".....OO.........",
    "................",
    "................",
    "................",
]
FOOD['toast'] = [
    "................",
    "................",
    "................",
    "...........OO...",
    ".........OOrtO..",
    ".......OOrtyrgO.",
    ".....OOtrfghrtO.",
    "...OOrtgfrtytrO.",
    "..OwrtyrtgfhrO..",
    ".OLwwrtrgftrOO..",
    ".OLHLwwwwwwOO...",
    ".OBBLLBBBOO.....",
    "..ODDBBOO.......",
    "...OOOO.........",
    "................",
    "................",
]
FOOD['sushi'] = [
    "................",
    "................",
    "................",
    "................",
    "....OOOO........",
    "...OaddaO.OOOO..",
    "...OdwwsOOaddaO.",
    "...OsweaOOdwwsO.",
    "...OOsaOOOsweaO.",
    ".OOOOOOOOOOsaOO.",
    ".OaddaOOOOOOOO..",
    ".OdwwsO.........",
    ".OsweaO.........",
    "..OOOO..........",
    "................",
    "................",
]
FOOD['slices'] = [
    "................",
    "................",
    "................",
    "................",
    "........OOOO....",
    "......OOLHLBO...",
    "....OOLHLBBDO...",
    "...OLHLBBBDO....",
    "...OOOOOOOO.....",
    "..OOLHLBBBDO....",
    ".OLHLBBBDDO.....",
    ".OOOOOOOOO......",
    "...ggfhg........",
    "................",
    "................",
    "................",
]
FOOD['nuts'] = [
    "................",
    "................",
    "................",
    "................",
    "......OOO.......",
    ".....OLHBO.OO...",
    "...OOOBBDOOLBO..",
    "..OLHBOOOOBBDO..",
    "..OBBDOOLHOOOOO.",
    "...OOOLHBBOLHBO.",
    "..OOO.OBBDOBBDO.",
    ".OLHBO.OOO.OOO..",
    ".OBBDO..........",
    "..OOO...........",
    "................",
    "................",
]
FOOD['poppers'] = [
    "................",
    "................",
    "................",
    "................",
    "..........fg....",
    "...fg....OOh....",
    "...hOO..OLHBO...",
    "..OOLBO.OwewBO..",
    ".OLHwwBOOBwwDO..",
    ".OBwewBO.OBBDO..",
    ".OBBwBDO..OOO...",
    "..OBBDO.........",
    "...OOO..........",
    "................",
    "................",
    "................",
]
FOOD['bun'] = [
    "................",
    "................",
    "................",
    "................",
    ".....OOOOOO.....",
    "...OOLHLLBBOO...",
    "..OLHLBBqBBBDO..",
    ".OLHBBqBBBBqBDO.",
    ".OBBBBBBqBBBDDO.",
    ".OBqBBBBBBBDDDO.",
    "..ODBBBBBDDDDO..",
    "...OODDDDDDOO...",
    ".....OOOOOO.....",
    "................",
    "................",
    "................",
]
FOOD['rings'] = [
    "................",
    "................",
    "................",
    "................",
    "....OOOO........",
    "...OLHLBO.OOOO..",
    "..OLO..OBOLHLBO.",
    "..OBO..OBOO..OBO",
    "...OBBDOOO....DO",
    "....OOOOLHLBOBDO",
    ".......OO..OBOO.",
    ".......OB..ODO..",
    "........OBDDO...",
    ".........OOO....",
    "................",
    "................",
]
FOOD['patties'] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    ".....OOOOO......",
    "...OOLHLBBOO....",
    "..OLHBBqBBBDO...",
    "..OBBqBBBqBDOOO.",
    "..ODBBBBDDOLHBOO",
    "...OODDDDOLBqBDO",
    ".....OOOOOBBBDDO",
    "..........OOOOO.",
    "................",
    "................",
    "................",
]
FOOD['pancakes'] = [
    "................",
    "................",
    "................",
    "......qwwq......",
    "....OOqeewOO....",
    "...OLHLwwBBBO...",
    "..OBLLBBBBBBDO..",
    "..ODDDDDDDDDDO..",
    "..OLHLBBBBBBDO..",
    "..ODDDDDDDDDDO..",
    "..OLHLBBBBBBDO..",
    "..ODDDDDDDDDDO..",
    "...OOOOOOOOOO...",
    "................",
    "................",
    "................",
]
FOOD['omelet'] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "......OOOOO.....",
    "....OOLHHLBOO...",
    "...OLHLBBBBBDO..",
    "..OLHBBBBBBBBDO.",
    "..OBBBBqBBBBBDO.",
    "..ODBBBBBBBBDDO.",
    "...OODDDDDDDOO..",
    ".....OOOOOOOO...",
    "................",
    "................",
    "................",
]

# ---------------- напиток в кружке (рисуется ПОВЕРХ стекла) ----------------
FOOD['drink'] = [
    "................",
    "................",
    "................",
    "................",
    "........LL......",
    ".....DDLLL......",
    "................",
    ".....BDDDB......",
    ".....LmLBD......",
    "....LmLLBBD.....",
    "....LlLBDZZ.....",
    "....BLBDZZZ.....",
    "....DBBDZZD.....",
    ".....DDDDD......",
    "................",
    "................",
]

# ---------------- накладки (рисуются последними) ----------------
OVERLAY = {
    'sprig': [
        "................",
        "................",
        "................",
        "..........gh....",
        ".........fgg....",
        "..........f.....",
    ],
    'berries': [
        "................",
        "................",
        "................",
        ".......rt.......",
        "......rtyt......",
        ".......rr.......",
    ],
    'holly': [
        "................",
        "......fg.gh.....",
        ".......frt......",
        "........yt......",
    ],
    'drizzle': [
        "................",
        "................",
        "................",
        "................",
        "......w..w......",
        ".....w.ww..w....",
        "......w...w.....",
    ],
    'mango': [
        "................",
        "................",
        "................",
        "................",
        "......qwwe......",
        ".....qwwwwe.....",
        "......qqqw......",
    ],
    'dollop': [
        "................",
        "................",
        "........as......",
        ".......asdd.....",
        "........aa......",
    ],
    'lemon': [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "............uu..",
        "...........uiou.",
        "...........uiiu.",
        "............uu..",
    ],
    # пар над горячим напитком (цвет — светлое стекло, как у hot_cocoa в FD)
    'steam': [
        ".......m........",
        "........m.......",
        ".......mm.......",
        "......m.........",
    ],
    # долька лимона на краю кружки
    'lemon_rim': [
        "................",
        "................",
        "..........ui....",
        ".........uoiu...",
        ".........uiu....",
        "..........u.....",
    ],
    'foam': [
        "................",
        "................",
        "................",
        "................",
        "....sdds........",
        ".....asas.......",
    ],
    # колечки перца поверх блюда
    'chili': [
        "................",
        "................",
        "................",
        "................",
        "................",
        ".....rt....rt...",
        "................",
        "................",
        "................",
        "........rt......",
    ],
    # долька лимона слева сверху (для блюд в руках)
    'lemon_tl': [
        "................",
        "................",
        ".uu.............",
        "uiou............",
        "uiiu............",
        ".uu.............",
    ],
    # кусочек хлеба на краю миски
    'bread': [
        "................",
        "................",
        "................",
        "...........uuu..",
        "..........uoiiu.",
        "..........uiiu..",
        "...........uu...",
    ],
    # завитки папоротника
    'fiddle': [
        "................",
        "................",
        "................",
        "......gh..hg....",
        ".....g.f..f.g...",
        "......gf..fg....",
    ],
}

# ======================================================================================
#  Блюда: (тара, шаблон, основной цвет, гарнир1, гарнир2, гарнир3, гарнир4, накладки)
#  тара: 'deep' | 'wide' | 'glass' | None
# ======================================================================================
def S(cont, tpl, main, g1=None, g2=None, g3=None, g4=None, over=()):
    return dict(cont=cont, tpl=tpl, main=main, g=[g1, g2, g3, g4], over=list(over))

DISHES = {
    # ---- супы и похлёбки (глубокая миска) ----
    'parsnip_soup':       S('deep', 'soup_cream',  '#e3cc8c', '#f5ecc8', over=['sprig']),
    'pumpkin_soup':       S('deep', 'soup_cream',  '#e0862a', '#f3d6a0', over=['sprig']),
    'lobster_bisque':     S('deep', 'soup_cream',  '#d95a36', '#f2b07c', over=['sprig']),
    'algae_soup':         S('deep', 'soup',        '#4f8a3a', '#2f6a2a', '#7ab24a'),
    'pale_broth':         S('deep', 'soup',        '#d6d0b0', '#bdb38f'),
    'bean_hotpot':        S('deep', 'soup_chunky', '#a0522d', '#d9a066', '#5aa03c'),
    'tom_kha_soup':       S('deep', 'soup_chunky', '#ecd59a', '#e0703a', '#6aa040', over=['sprig']),
    'trout_soup':         S('deep', 'soup_chunky', '#d6843e', '#f2b4a0', '#3f8a52'),
    'chowder':            S('deep', 'soup_chunky', '#e8dcb8', '#e2b46e', '#d07040', g3='#d9a25a', over=['bread']),
    'fish_stew':          S('deep', 'soup_chunky', '#c44a2a', '#f0caa0', '#e8a040', over=['sprig']),
    'tropical_curry':     S('deep', 'soup_chunky', '#dc9a28', '#f2e4b0', '#c8442a'),
    'vegetable_medley':   S('deep', 'heap',        '#c84a32', '#5aa03c', '#e8902c'),
    'autumns_bounty':     S('deep', 'heap',        '#de7a2a', '#c99a4a', '#9a4a32'),
    'stir_fry':           S('deep', 'heap',        '#c8843a', '#6aa040', '#e05a30'),
    'fiddlehead_risotto': S('deep', 'mound',       '#eadfb8', over=['fiddle']),
    'coleslaw':           S('deep', 'heap',        '#d8dca0', '#94468a', '#e8902c'),
    'poi':                S('deep', 'mound',       '#a688b8'),
    # ---- салаты ----
    'salad':              S('deep', 'salad',       '#5fa83a', '#d23c2c', '#f0d040'),
    'radish_salad':       S('deep', 'salad',       '#6aa040', '#dc3c5c', '#ece2d6'),
    'shrimp_cocktail':    S('deep', 'cocktail',    '#c23a2a', '#f08a62', over=['lemon'], g3='#f0d040'),
    # ---- сладкое в миске ----
    'cranberry_sauce':    S('deep', 'mound',       '#a8203a', g2='#d8344c', over=['berries']),
    'rice_pudding':       S('deep', 'mound',       '#efe6cc', '#b0703a', over=['drizzle']),
    'mango_sticky_rice':  S('deep', 'mound',       '#eee8dc', '#f0a830', over=['mango']),
    'banana_pudding':     S('deep', 'heap',        '#f0d878', '#e8c470', '#c8904a'),
    'plum_pudding':       S('deep', 'pudding',     '#7a3a2a', g2='#d0283a', over=['holly']),
    'seafoam_pudding':    S('deep', 'pudding',     '#4fae9e', over=['dollop']),
    'ice_cream':          S('deep', 'icecream',    '#f2e4c4', '#f09ab4', '#8a5a3a'),
    'fruit_salad':        S('deep', 'heap',        '#f0a040', '#e04050', '#5a6ad0'),
    # ---- вторые блюда (широкая миска) ----
    'cheese_cauliflower': S('wide', 'pl_blobs',    '#ece2c4', '#f0c040'),
    'eggplant_parmesan':  S('wide', 'pl_blobs',    '#7a4a8a', '#c8302a'),
    'glazed_yams':        S('wide', 'pl_blobs',    '#e07a30', '#f5c060'),
    'baked_fish':         S('wide', 'pl_fish',     '#d9a35a', '#f2d64b'),
    'carp_surprise':      S('wide', 'pl_fish',     '#8c8a68', '#c8b080'),
    'crispy_bass':        S('wide', 'pl_fillet',   '#c8843a', '#a86a2a', g3='#f0d040'),
    'spicy_eel':          S('wide', 'pl_eel',      '#c8442a', '#6a1a10', '#4f9a30', over=['chili']),
    'dish_o_the_sea':     S('wide', 'pl_sardines', '#8aa0b0'),
    'fried_mushroom':     S('wide', 'pl_fried',    '#9a6a42', '#6aa040'),
    'fried_eel':          S('wide', 'pl_eel',      '#c08a40', '#6a3a14', over=['sprig']),
    'escargot':           S('wide', 'pl_fried',    '#8e6448', '#6aa040'),
    'salmon_dinner':      S('wide', 'pl_main_side', '#f08a6a', '#f2d64b', '#5a9a3a'),
    'farmers_lunch':      S('wide', 'pl_main_side', '#f2c94c', '#d89a30', '#e8d7a0'),
    'complete_breakfast': S('wide', 'pl_breakfast', '#d9a25a', '#c87a3a'),
    'spaghetti':          S('wide', 'pl_noodles',  '#f0d690', '#c8302a'),
    'squid_ink_ravioli':  S('wide', 'pl_ravioli',  '#3a3846', '#e8dcc0'),
    'red_plate':          S('wide', 'pl_mix3',     '#c8343a', '#8a2a5a', '#e05a4a'),
    'super_meal':         S('wide', 'pl_mix3',     '#5aa03c', '#e0b040', '#c8402a'),
    'roots_platter':      S('wide', 'pl_wedges',   '#e07a30', '#e8d7a0'),
    'stuffing':           S('wide', 'pl_heap',     '#b07a40', '#c8243a', '#8a5a2a'),
    'artichoke_dip':      S('wide', 'pl_dip',      '#c4c486', '#e0b060', '#6a9a3a'),
    # ---- в руках: снеки ----
    'omelet':             S(None, 'omelet',   '#f2c94c', '#d89a30', over=['sprig']),
    'tortilla':           S(None, 'flat',     '#e8c88a', '#c8a060'),
    'hashbrowns':         S(None, 'hash',     '#d8a04a', '#a8702a'),
    'crab_cakes':         S(None, 'patties',  '#d8a050', '#c8502a', g3='#f0d040', over=['lemon_tl']),
    'pancakes':           S(None, 'pancakes', '#e0b060', '#f2dc70'),
    'fried_calamari':     S(None, 'rings',    '#e0b060'),
    'strange_bun':        S(None, 'bun',      '#7a5a8a', '#4a3a5a'),
    'lucky_lunch':        S(None, 'wrap',     '#e8c88a', '#5a7ad0', '#8a4a7a'),
    'pizza':              S(None, 'pizza',    '#d9a25a', '#f0c850', '#c0342a'),
    'pepper_poppers':     S(None, 'poppers',  '#c8402a', '#f0e0b0'),
    'sashimi':            S(None, 'slices',   '#f07a6a'),
    'maki_roll':          S(None, 'sushi',    '#2f4a30', '#f08a6a'),
    'roasted_hazelnuts':  S(None, 'nuts',     '#a8703a'),
    'bruschetta':         S(None, 'toast',    '#d9a25a', '#f0d8a0', '#d03a2a'),
    'fish_taco':          S(None, 'taco',     '#e8c060', '#f0e0c0', '#d03a2a'),
    'survival_burger':    S(None, 'burger',   '#c8883a', '#f0c040', '#7a4a2a'),
    # ---- в руках: сладости ----
    'cookie':             S(None, 'cookie',   '#d9a25a', '#5a3a22'),
    'chocolate_cake':     S(None, 'cake',     '#7a4a2a', g2='#c8243a', g4='#4a2818'),
    'pink_cake':          S(None, 'cake',     '#f0d8b0', g2='#d0304a', g4='#f090b0'),
    'rhubarb_pie':        S(None, 'slice',    '#d9a25a', '#c8304a'),
    'pumpkin_pie':        S(None, 'slice',    '#d9a25a', '#e07a2a', over=['dollop']),
    'blueberry_tart':     S(None, 'tart',     '#d9a25a', '#4a5ac0', '#2a3a8a'),
    'blackberry_cobbler': S(None, 'cobbler',  '#c8904a', '#4a2a5a'),
    'cranberry_candy':    S(None, 'candy',    '#c8243a', '#e8e0d0'),
    'poppyseed_muffin':   S(None, 'muffin',   '#e0b060', '#3a3040', '#b85a3a'),
    'miners_treat':       S(None, 'muffin',   '#f0e0b0', '#e8902a', '#8a6a9a'),
    'maple_bar':          S(None, 'bar',      '#d9a25a', '#a8602a'),
    # ---- напитки (стеклянная кружка) ----
    'triple_shot_espresso': S('glass', 'drink', '#4a2a18', over=['steam']),
    'ginger_ale':           S('glass', 'drink', '#e8b84a', over=['lemon_rim'], g3='#f0d040'),
}

# ======================================================================================
#  Цвет
# ======================================================================================
FIXED = {
    # зелень
    'f': '#2a5a26', 'g': '#4d8c3b', 'h': '#7ab244',
    # белое (рис, сливки, белок) — как у FD: без чистого белого
    'a': '#b7ab9b', 's': '#e9e2d9', 'd': '#f8f1e9',
    # желток
    'v': '#f5c040', 'b': '#d98a1c',
    # дерево миски (палитра Farmer's Delight)
    'K': '#3f2b0b', 'M': '#714f0f', 'N': '#533909', 'P': '#302109', 'Q': '#1f1502',
    'R': '#3a2706', 'Y': '#8a6420', 'W': '#986d4e',
    # стекло (палитра Farmer's Delight)
    'j': '#5d8fc2', 'k': '#84add8', 'l': '#b3cfec', 'm': '#d4e5f7',
}

def _rgb(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))

def _hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, round(x))) for x in rgb)

def _clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def _toward(h, target, amt):
    d = (target - h + 0.5) % 1.0 - 0.5
    return (h + max(-amt, min(amt, d))) % 1.0

def tone(base, vm, sm, hs, light):
    """Сдвиг тона: light=True — к тёплому жёлтому, иначе тени: жёлто-оранжевые уходят в красное,
    остальные — в сине-фиолетовое."""
    r, g, b = [x / 255 for x in _rgb(base)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.16:  # почти белый/серый — тёплый нейтральный, как сливки/рис у FD
        h = 0.085
        s = _clamp(s * sm + (0.0 if light else (1 - vm) * 0.22))
    else:
        target = 0.14 if light else (0.0 if 0.03 <= h <= 0.22 else 0.74)
        h = _toward(h, target, hs)
        s = _clamp(s * sm)
    v = _clamp(v * vm, 0.07, 0.97)
    if light and v >= 0.97:      # уже светлый — блик за счёт снижения насыщенности
        s = _clamp(s * 0.75)
    return _hex([x * 255 for x in colorsys.hsv_to_rgb(h, s, v)])

def main_ramp(base):
    return {
        'H': tone(base, 1.24, 0.62, 0.035, True),
        'L': tone(base, 1.11, 0.84, 0.018, True),
        'B': tone(base, 1.0, 1.0, 0.0, True) if _rgb(base) != (255, 255, 255) else '#f8f1e9',
        'D': tone(base, 0.80, 1.08, 0.022, False),
        'O1': tone(base, 0.62, 1.12, 0.035, False),
        'O2': tone(base, 0.47, 1.15, 0.05, False),
        'O3': tone(base, 0.34, 1.18, 0.065, False),
    }

def small_ramp(base):
    return (tone(base, 0.76, 1.08, 0.025, False), tone(base, 1.0, 1.0, 0.0, True), tone(base, 1.16, 0.8, 0.025, True))

def palette(spec):
    pal = dict(FIXED)
    mr = main_ramp(spec['main'])
    pal.update({k: mr[k] for k in 'HLBD'})
    pal['Z'] = mr['O2']
    for chars, col in zip(('qwe', 'rty', 'uio', 'zxc'), spec['g']):
        if col is None:
            continue
        for ch, c in zip(chars, small_ramp(col)):
            pal[ch] = c
    return pal, mr

# ======================================================================================
#  Отрисовка
# ======================================================================================
def _pad(rows):
    rows = [r.ljust(16, '.')[:16] for r in rows]
    return rows + ['.' * 16] * (16 - len(rows))

def render(name, spec):
    from PIL import Image
    pal, mr = palette(spec)
    food = _pad(FOOD[spec['tpl']])
    cont = spec['cont']
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    px = img.load()

    # центр еды — для тонировки контура (сверху-слева светлее, снизу-справа темнее)
    cells = [(x, y) for y in range(16) for x in range(16) if food[y][x] != '.']
    cx = sum(x for x, _ in cells) / len(cells)
    cy = sum(y for _, y in cells) / len(cells)

    def put(x, y, ch):
        if ch == '.':
            return
        if ch == 'O':
            t = (x - cx) * 0.55 + (y - cy)
            col = mr['O1'] if t < -1.5 else (mr['O3'] if t > 2.0 else mr['O2'])
        else:
            col = pal.get(ch)
            if col is None:
                raise KeyError(f'{name}: цвет для "{ch}" не задан')
        px[x, y] = _rgb(col) + (255,)

    def layer(rows):
        for y, row in enumerate(_pad(rows)):
            for x, ch in enumerate(row):
                put(x, y, ch)

    if cont == 'glass':
        layer(CONTAINERS['glass'])
        layer(food)
    else:
        layer(food)
        if cont:
            layer(CONTAINERS[cont])
    for ov in spec['over']:
        layer(OVERLAY[ov])
    return img

def render_all(out_dir, names=None):
    os.makedirs(out_dir, exist_ok=True)
    done = []
    for name, spec in DISHES.items():
        if names and name not in names:
            continue
        render(name, spec).save(os.path.join(out_dir, name + '.png'))
        done.append(name)
    return done

def contact_sheet(src_dir, names, out_png, scale=6, cols=10):
    from PIL import Image, ImageDraw
    cell = 16 * scale + 8
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * cell, rows * (cell + 12)), (139, 139, 139, 255))
    d = ImageDraw.Draw(sheet)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(src_dir, n + '.png')).convert('RGBA').resize((16 * scale, 16 * scale), Image.NEAREST)
        x, y = (i % cols) * cell, (i // cols) * (cell + 12)
        sheet.alpha_composite(im, (x + 4, y + 4))
        d.text((x + 3, y + cell - 2), n[:18], fill=(20, 20, 20, 255))
    sheet.save(out_png)

if __name__ == '__main__':
    argv = sys.argv[1:]
    sheet = None
    if '--sheet' in argv:
        i = argv.index('--sheet')
        sheet = argv[i + 1]
        del argv[i:i + 2]
    out = argv[0] if argv else DEFAULT_OUT
    names = render_all(out)
    print(f'OK: {len(names)} текстур -> {out}')
    if sheet:
        contact_sheet(out, names, sheet)
