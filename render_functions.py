#
#
#
#

from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
import textwrap

import tcod
import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x,y) or not game_map.visible[x,y]:
        return""
    names = ",".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )
    
    return names.capitalize()

def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = float(current_value/maximum_value)
##    x = 0
##    for i in range (0,maximum_value):
##        console.draw_rect(x=x, y=50, width=1, height=1, ch=1, bg=color.black)
##        x += 2
##
    x = 0

    console.print(x=65, y=58, string="for help - (h)", fg=color.white)

    console.print(
        x=1, y = 50, string=f"HP:{current_value}/{maximum_value}", fg=color.bar_text
    )
    
    if bar_width >= 0.75:
        console.print(x = 1,y= 51,string=" _--_ _--_ ",fg=color.bar_filled)
        console.print(x = 1,y= 52,string="/....V....\ ",fg=color.bar_filled)
        console.print(x = 1,y= 53,string="(.........)",fg=color.bar_filled)
        console.print(x = 1,y= 54,string=" \......./ ",fg=color.bar_filled)
        console.print(x = 1,y= 55,string="  \...../  ",fg=color.bar_filled)
        console.print(x = 1,y= 56,string="   \.../   ",fg=color.bar_filled)
        console.print(x = 1,y= 57,string="    \./    ",fg=color.bar_filled)
        console.print(x = 1,y= 58,string="     v     ",fg=color.bar_filled)
	
    elif 0.75 > bar_width >= 0.5:
        console.print(x = 1,y= 51,string=" _--_ _--_ ",fg=color.bar_half_plus)
        console.print(x = 1,y= 52,string="/....V....\ ",fg=color.bar_half_plus)
        console.print(x = 1,y= 53,string="(..../....)",fg=color.bar_half_plus)
        console.print(x = 1,y= 54,string=" \...\.../ ",fg=color.bar_half_plus)
        console.print(x = 1,y= 55,string="  \../../  ",fg=color.bar_half_plus)
        console.print(x = 1,y= 56,string="   \.\./   ",fg=color.bar_half_plus)
        console.print(x = 1,y= 57,string="    \|/    ",fg=color.bar_half_plus)
        console.print(x = 1,y= 58,string="     v     ",fg=color.bar_half_plus)
    elif 0.5 > bar_width >= 0.25:
        console.print(x = 1,y= 51,string=" _--_ _--_ ",fg=color.bar_half)
        console.print(x = 1,y= 52,string="/.../ \.X.\ ",fg=color.bar_half)
        console.print(x = 1,y= 53,string="(...\ /...)",fg=color.bar_half)
        console.print(x = 1,y= 54,string=" \X./ \../ ",fg=color.bar_half)
        console.print(x = 1,y= 55,string="  \.\ /./  ",fg=color.bar_half)
        console.print(x = 1,y= 56,string="   \.\./   ",fg=color.bar_half)
        console.print(x = 1,y= 57,string="    \|/    ",fg=color.bar_half)
        console.print(x = 1,y= 58,string=" _   v ;_  ",fg=color.bar_half)
    elif 0.25 > bar_width > 0:
        console.print(x = 1,y= 51,string=" _--   --_ ",fg=color.bar_half_minus)
        console.print(x = 1,y= 52,string="/X./'  \X.\ ",fg=color.bar_half_minus)
        console.print(x = 1,y= 53,string="(..\  '/x.)",fg=color.bar_half_minus)
        console.print(x = 1,y= 54,string=" \X/   \./ ",fg=color.bar_half_minus)
        console.print(x = 1,y= 55,string="  \.\ /./  ",fg=color.bar_half_minus)
        console.print(x = 1,y= 56,string=" ; \; ;/   ",fg=color.bar_half_minus)
        console.print(x = 1,y= 57,string="    \~/;   ",fg=color.bar_half_minus)
        console.print(x = 1,y= 58,string=" _;_ v _;_ ",fg=color.bar_half_minus)
    else:
        console.print(x = 1,y= 51,string=" YOU PERISH",fg=color.bar_empty)
        console.print(x = 1,y= 52,string="   _---_   ",fg=color.bar_empty)
        console.print(x = 1,y= 53,string="  /.....\  ",fg=color.bar_empty)
        console.print(x = 1,y= 54,string=" (.X...X.) ",fg=color.bar_empty)
        console.print(x = 1,y= 55,string="  |..Y..|  ",fg=color.bar_empty)
        console.print(x = 1,y= 56,string="  |||||||  ",fg=color.bar_empty)
        console.print(x = 1,y= 57,string="           ",fg=color.bar_empty)
        console.print(x = 1,y= 58,string="__-;-__;-;_",fg=color.bar_empty)
        
    

def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    x,y = location

    console.print(x=x, y=y, string = f"Dungeon floor: {dungeon_level}")
    

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )
    y_offset = +1
    for line in textwrap.wrap(f"This is a {names_at_mouse_location}", 15):
        console.print(x=x, y=y + y_offset , string=line)
        y_offset +=1
        

def boss_print( console: Console ):
    console.print(x=1, y=1, string='''       ,)"""""")       )^^^^^)  /^^^^^/  \^"""""\   /^^^^^/              )""""""''', fg=color.white)
    console.print(x=1, y=2, string='''     /""""""";'       /^^^^^/  (^^^^^(    \^"""""`;^^^^^;              ,;"""""""''', fg=color.white)
    console.print(x=1, y=3, string='''  ,;"""""",~'        :^^^^^:   |^^^^^|     `\^"""(^^^^^(             ,/"""""""";''', fg=color.white)
    console.print(x=1, y=4, string='''  (""""""(         ,!^^^^^^!   (^^^^^(       \^"""|^^^^^|`--__    ,;'"""""""",/ ''', fg=color.white)
    console.print(x=1, y=5, string='''  !"""""",_--_,,__-!^^^^^^^)    `^^^^^`       `~.;^^^^^;'"""""`--'""""""""",/   ''', fg=color.white)
    console.print(x=1, y=6, string='''   `;"",/^^^^^^^^^^^^^^^^^/      \^^^^^\        (^^^^^("""""""""""""""""",/     ''', fg=color.white)
    console.print(x=1, y=7, string='''    \,/^^^^^^^^^^^^^^^^^,)        \^^^^^\       |^^^^^|\^"""""__-----__.;       ''', fg=color.white)
    console.print(x=1, y=8, string='''    ~^^^^^^^^^^^,._--_.~           \^^^^^\      (^^^^^( `~-.;'^^^^^^^^^^`       ''', fg=color.white)
    console.print(x=1, y=9, string='''   /^^^^^^^,_;/")                   \^^^^^\      ;^^^^^: __/^^^^^^^^^^^^^\      ''', fg=color.white)
    console.print(x=1, y=10, string='''  (^^^^^^^(""""";                    )^^^^^)      \_^^^^^^^^^^^, __^^^^^^^\     ''', fg=color.white)
    console.print(x=1, y=11, string='''  ;^^^^^^^;""""""\                  /^^^^^/         `__,^^^^^,~    `,^^^^^^\    ''', fg=color.white)
    console.print(x=1, y=12, string='''  )^^^^^^,)""""""")                (^^^^^(              ;___~        )^^^^^^)   ''', fg=color.white)
    console.print(x=1, y=13, string='''/^^^^^^^/!"""""""!                 |^^^^^|                          ;^^^^^^;    ''', fg=color.white)
    console.print(x=1, y=14, string='''^^^^^^^) )""""""")                /^^^^^^^\                         (^^^^^(     ''', fg=color.white)
    console.print(x=1, y=15, string='''^^^,/   /"""""""/                 \^^^^^^^/                         :^^^^^^: ,~.''', fg=color.white)
    console.print(x=1, y=16, string='''__)     !""""""!                   \X^^^0/                           !^^^^^!/"""''', fg=color.white)
    console.print(x=1, y=17, string='''       (""""""(                     \^^^/              /\            (^^^^^^("""''', fg=color.white)
    console.print(x=1, y=18, string='''        )"""""")                     `w'               ("\            \_^^^^^\_"''', fg=color.white)
    console.print(x=1, y=19, string='''       ;""""""';                      |                !""`~,__     __/"\^^^^^^|''', fg=color.white)
    console.print(x=1, y=20, string='''  ,_--'"""""""(                      / \                `,"""""`~--'"""""~_^^^^^''', fg=color.white)
    console.print(x=1, y=21, string=''',:""""""""""",)                                          `~,__"""""""""""",\^^^^''', fg=color.white)
    console.print(x=1, y=22, string='''""""""""""""";                                                `~--,""""";/'.`~--''', fg=color.white)
    console.print(x=1, y=23, string='''""""""""""",/                                                      `~~'"        ''', fg=color.white)
    console.print(x=1, y=24, string='''"",;-,__--'                        _______                                      ''', fg=color.white)
    console.print(x=41, y=25, string='''  \                                     ''', fg=color.white)
    console.print(x=41, y=26, string='''   \                                    ''', fg=color.white)
    console.print(x=41, y=27, string='''    |\                                  ''', fg=color.white)
    console.print(x=41, y=28, string='''    | \                                 ''', fg=color.white)
    console.print(x=41, y=29, string='''    |                                   ''', fg=color.white)
    console.print(x=1, y=25, string='''./                                /''', fg=color.white)
    console.print(x=1, y=26, string=''';                                / ''', fg=color.white)
    console.print(x=1, y=27, string='''                               /|  ''', fg=color.white)
    console.print(x=1, y=28, string='''                              / |  ''', fg=color.white)
    console.print(x=1, y=29, string='''                                |  ''', fg=color.white)
#    console.print(x=1, y=30, string='''......................................#.........................................''', fg=color.white)
#    console.print(x=1, y=31, string='''......................................#.........................................''', fg=color.white)
#    console.print(x=1, y=32, string='''......................................#.........................................''', fg=color.white)
#    console.print(x=1, y=33, string='''......................................#.........................................''', fg=color.white)








    #console.print(x=x, y =y, string=f"{names_at_mouse_location}")
                                
