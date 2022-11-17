####################
# 
# Galina Bovykina
# November 16 2022
#
# This is the main file that launches the whole game
# Code adopted from TStand90 rogueliketutorials.com
#
####################

import random
import traceback
import tcod 
import os
import sys
import glob
import exceptions
import input_handlers
from input_handlers import EventHandler
import setup_game
import color


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved successfully.")


#This is the main function that launches the game
def launch() -> None:
    screen_width = 80
    screen_height = 60
    #  This sets up the standart for the display
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32,8, tcod.tileset.CHARMAP_TCOD
        )

    #  This runs the Main Menu
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    #  This sets up the Game Screen
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title =" GALINA's ROGUELIKE SNAKE KILLING EXPERIMENT",
        vsync = True,
        ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        #  This makes sure that the game is running smoothly 
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:
                    traceback.print_exc()
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:
            save_game(handler, "savegame.sav")
            raise 
        except BaseException:
            save_game(handler, "savegame.sav")
            raise 




if __name__ == "__main__":
    #   This is here for play testing to make it easier to playtest
    #random.seed(42)
    launch()
