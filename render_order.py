####################
# 
# Galina Bovykina
# November 16 2022
#
# This is a render orderer
# Code adopted from TStand90 rogueliketutorials.com
#
####################
from enum import auto, Enum

class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
