#
#
##
#

from components.ai import HostileEnemy, SnakeEnemy, WormEnemy, ClosedDoor
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item



player = Actor(
    char="@",
    color=(255,255,255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, armorclass=2, strength=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

big_evil_snake = Actor(
    char="S",
    color=(147,244,200),
    name="Big EVIL Snake",
#    ai_cls=HostileEnemy,
    ai_cls=SnakeEnemy,
    fighter=Fighter(hp=16, armorclass=1, strength=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

small_evil_snake = Actor(
    char="s",
    color=(112, 219, 175),
    name="Small EVIL Snake",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, armorclass=0, strength=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=300),
)

worm = Actor(
    char="s",
    color=(112, 28, 70),
    name="Worm",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=5, armorclass=0, strength=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=10),
)

duck = Actor(
    char="2",
    color=(145, 131, 102)
    , name="Duck",
    #ai_cls=WormEnemy,
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, armorclass=0, strength=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

golden_duck = Actor(
    char="2",
    color=(219, 156, 26),
    name="Golden Duck",
##    ai_cls=SnakeEnemy,
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=20, armorclass=2, strength=3),
    inventory=Inventory(capacity=1),
    level=Level(xp_given=200),
)

closed_door = Actor(
    char="B",
    color=(219, 156, 26),
    name="Closed Door",
    ai_cls=ClosedDoor,
    fighter=Fighter(hp=2, armorclass=0, strength=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
)

energy_drink = Item(
    char="!",
    color=(148, 252, 50),
    name="Energy Drink",
    consumable=consumable.HealingConsumable(amount=4)
)

nice_note = Item(
    char="&",
    color=(255,230,210),
    name="Nice Note from Your Friends",
    consumable=consumable.HealingConsumable(amount=1)
)

deadline_list = Item(
    char="?",
    color=(216, 191, 219),
    name= "List of Deadlines",
    consumable=consumable.FatigueDamageConsumable(damage=10, maximum_range=5),
)

complicated_math_equation = Item(
    char="?",
    color=(197, 191, 219),
    name ="Complicated Math Equasions",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
    

stink_bomb = Item(
    char="Q",
    color=(144, 173, 10),
    name="Stink Bomb",
    consumable=consumable.StinkBombConsumable(damage=12, radius=3),
)
