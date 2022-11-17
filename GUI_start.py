####################
# 
# Galina Bovykina
# November 16 2022
#
# This manages the New Game GUI and collects the information
# for the game setup
#
####################

from new_game_setup import Ui_GalinaSnakeStrangelingEperimentSetup
 
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import os
import os.path
import sys
import random
import input_handlers

class BasicWindow(qtw.QWidget, Ui_GalinaSnakeStrangelingEperimentSetup):
    def __init__(self):
        super().__init__()

        self.setupUi(self)  # Initialize GUI
        self.start_game.clicked.connect(self.game_start)
        self.start_game.clicked.connect(self.on_exit)

    #  This determines what level of difficulty the user wants
    def index(self) -> int:
        index_now = self.difficulty_level.currentText()
        if index_now == "First Week (easy)":
            index = 1
        elif index_now == "Midterms (normal)":
            index = 2
        else:
            index = 3
        return index
    
    #  This collects the user input information
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
        return passing_var
    
    #  This creates a randomized base name for the player
    def update(self):
        names = ["Kermit", "Barhtolomew", "Martha", "Greigh"]
        name = random.choice(names)
        self.character_name.setText(name)

    #  This auto closes the widget when the user is done
    def on_exit(self):
        self.close()


def start_gui():
    app = qtw.QApplication([sys.argv])
    #  This does the basic order of operations 
    widget = BasicWindow()
    widget.show()
    widget.update()
    app.exec_()
    info = widget.game_start()
    return info
