#
#
#
#
#

from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent

from render_order import RenderOrder


if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor
    
    def __init__(self, hp: int, base_armorclass: int, base_strength: int, base_magic: int):
        self.max_hp = hp
        self._hp = hp
        self.base_armorclass = base_armorclass
        self.base_strength = base_strength
        self.base_magic = base_magic

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def armorclass(self) -> int:
        return self.base_armorclass + self.armorclass_bonus

    @property
    def strength(self) -> int:
        return self.base_strength + self.strength_bonus

    @property
    def armorclass_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.armorclass_bonus
        else:
            return 0

    @property
    def strength_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.strength_bonus
        else:
            return 0

    @property
    def magic(self) -> int:
        return self.base_magic + self.magic_bonus

    @property
    def magic_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.magic_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You perish..."
            death_message_color = color.player_die
        
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die
        if self.parent.name == "Closed Door":
            self.parent.char = "D"
            self.parent.color = (120, 87, 42)
            self.parent.blocks_movement = False
            self.parent.ai = None
            self.parent.name = f"The door falls open if front of you."
            self.parent.render_order = RenderOrder.CORPSE
        else:

            self.parent.char = "%"
            self.parent.color = (160, 0, 0)
            self.parent.blocks_movement = False
            self.parent.ai = None
            self.parent.name = f"dismembered corpse of {self.parent.name}"
            self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0
        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value -self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount




        

    
