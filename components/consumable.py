#
#
#
#

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item

class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        print("trying to eat")
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError()

class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        print("really trying to eat")
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered> 0:
            self.engine.message_log.addmessage(
                f"You shove the {self.parent.name} down your throat and feel {amount_recovered} HP healthier!",
                color.health_recovered,
            )

        else:
            raise Impossible("You feel like you are already at your best.")
