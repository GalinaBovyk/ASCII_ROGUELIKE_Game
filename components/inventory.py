####################
# 
# Galina Bovykina
# November 16 2022
#
# This sets up the Inventory
# Code adopted from TStand90 rogueliketutorials.com
#
####################

from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item:Item) -> None:
        self.items.remove(item)

        self.engine.message_log.add_message(
            f"You remove {item.name} from your pocket and place it on the gorund."
        )
