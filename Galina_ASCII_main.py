#
#
#
##
import tcod 
import os
import sys
import glob
##from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon



##
def launch() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50
    max_rooms = 12
    room_min_size = 5
    room_max_size = 17


    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32,8, tcod.tileset.CHARMAP_TCOD
        )
    event_handler = EventHandler()

    player = Entity(int(screen_width/2),int(screen_height/2), "@", (255,255,255))
    evil_snake = Entity(int(screen_width/2 - 5),int(screen_height/2 -5), "S", (147, 244, 200))
    entities = {evil_snake, player}
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
)


    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title =" GALINA's ROGUELIKE SNAKE KILLING EXPERIMENT",
        vsync = True,
        ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:

##            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
            engine.render(console=root_console, context=context)

##            context.present(root_console)
            events = tcod.event.wait()
            
            engine.handle_events(events)
##            root_console.clear()
##
##            for event in tcod.event.wait():
##                action = event_handler.dispatch(event)
##                if action is None:
##                    continue
##                if isinstance(action, MovementAction):
##
##                    player.move(dx=action.dx, dy=action.dy)
##                elif isinstance(action, EscapeAction):
##                    raise SystemExit()
##                





if __name__ == "__main__":
    launch()