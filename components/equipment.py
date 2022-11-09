#
#
#
#

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item

class Equipment(BaseComponent):
    paret: Actor

    def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None, ring: Optional[Item] = None):
        self.weapon = weapon
        self.armor = armor
        self.ring = ring

    @property
    def armorclass_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.armorclass_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.armorclass_bonus

        if self.ring is not None and self.ring.equippable is not None:
            bonus += self.ring.equippable.armorclass_bonus
        return bonus
        
    @property
    def strength_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.strength_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.strength_bonus

        if self.ring is not None and self.ring.equippable is not None:
            bonus += self.ring.equippable.strength_bonus
        return bonus

    @property
    def magic_bonus(self) -> int:
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.magic_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.magic_bonus

        if self.ring is not None and self.ring.equippable is not None:
            bonus += self.ring.equippable.magic_bonus
        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item or self.ring == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove {item_name} from your person."
        )
    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You put {item_name} onto your person."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if(
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"

        elif (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.ARMOR
        ):
            slot = "armor"

        else:
            slot = "ring"

        if getattr(self, slot) == equippable_item:
            self.uneqip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)
        
    










    