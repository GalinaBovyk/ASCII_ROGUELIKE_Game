####################
# 
# Galina Bovykina
# November 16 2022
#
# This determoines the idex depending on the type of equipment
# Code adopted from TStand90 rogueliketutorials.com
#
####################
from enum import auto, Enum

#####  This part was specifically modified by me  #####
# Added a ring type
class EquipmentType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    RING = auto()
