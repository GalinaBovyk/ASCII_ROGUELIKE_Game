####################
# 
# Galina Bovykina
# November 16 2022
#
# This has the classes of what one ac encounter in the dungeon
# Code adopted from TStand90 rogueliketutorials.com
#
####################

from __future__ import annotations
import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union
from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from componrnts.equipment import Equipment
    from components.equippable import Equippable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from components.level import Level
    from game_map import Gamemap

T = TypeVar("T", bound="Entity")

# This is a super class for the things that one can encounter 
class Entity:
    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y:int = 0,
        char: str = "?",
        color: Tuple[int,int,int] = (255,255,255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            self.parent = gamemap
            gamemap.entities.add(self)

    @property
    def gamemap(self) ->GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x:bint, y: int, gamemap: Optional[GameMap] = None) -> None:
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):
                if self.parent is self.parent:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def  distance(self, x: int, y: int) -> float:
        return math.sqrt((x- self.x)**2 + (y - self.y)**2)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


class Actor(Entity):
    #  This is specifically the class of the NPC's and the player
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int,int,int] = (255,255,255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        level: Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: optional[BaseAi] = ai_cls(self)

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.level = level
        self.level.parent = self

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)


class Item(Entity):
    #  This is the class pf objects that one can pick up in the dungeon
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int,int,int] = (255,255,255),
        name: str = "<Unnamed>",
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )
        self.consumable = consumable

        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable

        if self.equippable:
            self.equippable.parent = self
        
