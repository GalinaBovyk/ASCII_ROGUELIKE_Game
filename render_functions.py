#
#
#
#

from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
import textwrap

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
    bar_width = int(float(current_value)/maximum_value*total_width)
##    x = 0
##    for i in range (0,maximum_value):
##        console.draw_rect(x=x, y=50, width=1, height=1, ch=1, bg=color.black)
##        x += 2
##
    x = 0

    for j in range (0,current_value):
        console.draw_rect(x=x, y=50, width=1, height=1, ch=1, bg=color.bar_filled)
        x += 2

    console.print(
        x=1, y = 50, string=f"HP:{current_value}/{maximum_value}", fg=color.bar_text
    )
##    if bar_width >= 0.7:
##        for i, text in enumerate(
##                [" _--_ _--_ ",
##                 "(    V    )",
##                 " \       / ",
##                 "  \     /  ",
##                 "    \v/    "
##                 ]
##            ):
##                console.print(
##                    x = 1,
##                    y= 51 + i ,
##                    fg=color.bar_filled,
##                    alignment=tcod.CENTER,
##                )

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
    for line in textwrap.wrap(f"This is a {names_at_mouse_location}", 19):
        console.print(x=x, y=y + y_offset , string=line)
        y_offset +=1
        
        
    #console.print(x=x, y =y, string=f"{names_at_mouse_location}")
                                
