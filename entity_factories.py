#
#
##
#

from components.ai import HostileEnemy, SnakeEnemy, WormEnemy, ClosedDoor
from components.consumable import HealingConsumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item



player = Actor(
    char="@",
    color=(255,255,255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, armorclass=2, strength=5),
    inventory=Inventory(capacity=26),
)

big_evil_snake = Actor(
    char="S",
    color=(147,244,200),
    name="Big EVIL Snake",
#    ai_cls=HostileEnemy,
    ai_cls=SnakeEnemy,
    fighter=Fighter(hp=16, armorclass=1, strength=3),
    inventory=Inventory(capacity=0),
)

small_evil_snake = Actor(
    char="s",
    color=(112, 219, 175),
    name="Small EVIL Snake",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, armorclass=0, strength=2),
    inventory=Inventory(capacity=0),
)

worm = Actor(
    char="s",
    color=(112, 28, 70),
    name="Worm",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=5, armorclass=0, strength=0),
    inventory=Inventory(capacity=0),
)

duck = Actor(
    char="2",
    color=(145, 131, 102)
    , name="Duck",
    #ai_cls=WormEnemy,
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, armorclass=0, strength=1),
    inventory=Inventory(capacity=0),
)

golden_duck = Actor(
    char="2",
    color=(219, 156, 26),
    name="Golden Duck",
##    ai_cls=SnakeEnemy,
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=20, armorclass=2, strength=3),
    inventory=Inventory(capacity=1),
)

closed_door = Actor(
    char="B",
    color=(219, 156, 26),
    name="Closed Door",
    ai_cls=ClosedDoor,
    fighter=Fighter(hp=2, armorclass=0, strength=0),
    inventory=Inventory(capacity=0),
)

energy_drink = Item(
    char="!",
    color=(148, 252, 50),
    name="Energy Drink",
    consumable=HealingConsumable(amount=4)
)

nice_note = Item(
    char="&",
    color=(255,230,210),
    name="Nice Note from Your friends",
    consumable=HealingConsumable(amount=1)
)
    


