####################
# 
# Galina Bovykina
# November 16 2022
#
# This is a library of the different equipments one can find
# This was also customized ot include rings and very flexible equipment
# Code adopted from TStand90 rogueliketutorials.com
#
####################

from __future__ import annotations
from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import item

class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        strength_bonus: int = 0,
        armorclass_bonus: int = 0,
        magic_bonus: int = 0,
    ):
        self.equipment_type = equipment_type
        self.strength_bonus = strength_bonus
        self.armorclass_bonus = armorclass_bonus
        self.magic_bonus = magic_bonus



################################################################ WEAPON
class ComputerMouse(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, strength_bonus=1)

 
class Keyboard(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, strength_bonus=2)


class EmergencyTowel(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            armorclass_bonus=1,
        )


class PepperSpray(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            armorclass_bonus=2,
        )


class Wand(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, magic_bonus=1)


class SparklyBlaster(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, magic_bonus=2)

################################################################## ARMOR

class FaceMask(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            armorclass_bonus=1,
        )


class Hoodie(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            armorclass_bonus=2,
        )


class Sunglasses(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, strength_bonus=1)


class Platforms(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, strength_bonus=2)


class PartyHat(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, magic_bonus=1)


class HalloweenCostume(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, magic_bonus=2)


################################################################## RINGS

class TheOneRing(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.RING,
            strength_bonus=10,
            magic_bonus=10,
            armorclass_bonus=10,
        )


class MagicMoodRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RING, magic_bonus=4)


class StrengthMoodRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RING, strength_bonus=4)


class ArmorClassMoodRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RING, armorclass_bonus=4)
