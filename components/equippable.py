#
#
#
#

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
    ):
        self.equipment_type = equipment_type
        self.strength_bonus = strength_bonus
        self.armorclass_bonus = armorclass_bonus

class ComputerMouse(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, strength_bonus=1)

class Keyboard(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, strength_bonus=2)

class FaceMask(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, armorclass_bonus=2)

class Hoodie(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, armorclass_bonus=2)

class TheOneRing(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.RING, strength_bonus=10)
        # change rins to int and other shit
    

    

    

    
                 
