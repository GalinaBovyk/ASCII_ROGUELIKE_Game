# play_widget_v03.py
# VSFX-313
# 20221012
# Gray Marshall

from new_game_setup import Ui_GalinaSnakeStrangelingEperimentSetup
 

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import os
import os.path
import sys
import glob
import random
import input_handlers
import setup_game
import color
from engine import Engine
import entity_factories
from game_map import GameWorld
from procgen import generate_dungeon


class BasicWindow(qtw.QWidget, Ui_GalinaSnakeStrangelingEperimentSetup):
    def __init__(self):
        super().__init__()

        self.setupUi(self)  # Initialize GUI
        self.start_game.clicked.connect(self.game_start)
        self.start_game.clicked.connect(self.on_exit)

        

    
    def index(self) -> int:
        index_now = self.difficulty_level.currentText()
        if index_now == "First Week (easy)":
            index = 1
        elif index_now == "Midterms (normal)":
            index = 2
        else:
            index = 3
        return index
    
    #@property
    def char_name(self) :
        char_name = self.character_name.text()
        
        return char_name
        



    def game_start(self) :
        passing_var =[]
        character_name = self.character_name.text()
        passing_var.append(character_name)
        difficulty = int(self.index())
        passing_var.append(difficulty)
        max_roomsize = int(self.max_roomsize.text())
        passing_var.append(max_roomsize)
        min_roomsize = int(self.min_roomsize.text())
        passing_var.append(min_roomsize)
        rooms_per_floor = int(self.rooms_per_floor.text())
        passing_var.append(rooms_per_floor)
        floors_total = int(self.floors_total.text())
        passing_var.append(floors_total)
        #sys.exit("Start Game")
        #return passing_var
        #return input_handlers.MainGameEventHandler(setup_game.new_game())
        #input_handlers.MainGameEventHandler(new_game())
        return passing_var

        
        #print(f"{passing_var}")
        #sys.exit("Start Game")

    def update(self):
        names = ["Kermit", "Barhtolomew", "Martha", "Greigh"]
        name = random.choice(names)
        self.character_name.setText(name)

    def on_exit(self):
        self.close()
        

    
        


def start_gui():
    app = qtw.QApplication([sys.argv])

    widget = BasicWindow()
    widget.show()
    widget.update()
    widget.char_name()
    #info = widget.game_start()
    #print(widget.game_start())
    app.exec_()
    info = widget.game_start()
    return info

#    sys.exit(app.exec_())
    

##
##if __name__ == "__main__":
##    app = qtw.QApplication([sys.argv])
##
##    widget = BasicWindow()
##    widget.show()
##    widget.update()
##
##    sys.exit(app.exec_())
