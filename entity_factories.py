#
#
##
#

from components.ai import HostileEnemy, SnakeEnemy, WormEnemy, ClosedDoor
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item
import random
import tcod
from input_handlers import EndgameEventHandler



player = Actor(
    char="@",
    color=(255,255,255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_armorclass=5, base_strength=5, base_magic=3),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

############################################################## Monsters

big_evil_snake = Actor(
    char="S",
    color=(147,244,200),
    name="Big EVIL Snake",
#    ai_cls=HostileEnemy,
    ai_cls=SnakeEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_armorclass=1, base_strength=3, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

small_evil_snake = Actor(
    char="s",
    color=(112, 219, 175),
    name="Small EVIL Snake",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=7, base_armorclass=0, base_strength=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=30),
)

worm = Actor(
    char="s",
    color=(112, 28, 70),
    name="Worm",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=5, base_armorclass=0, base_strength=1, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=10),
)

duck = Actor(
    char="2",
    color=(145, 131, 102)
    , name="Duck",
    #ai_cls=WormEnemy,
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_armorclass=0, base_strength=3, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

golden_duck = Actor(
    char="2",
    color=(219, 156, 26),
    name="Golden Duck",
##    ai_cls=SnakeEnemy,
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_armorclass=2, base_strength=5, base_magic=0),
    inventory=Inventory(capacity=1),
    level=Level(xp_given=200),
)

anim_student = Actor(
    char="A",
    color=(240, 240, 14),
    name="Dehyudrated Animation Student",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=15, base_armorclass=3, base_strength=7, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=110),
)

professor = Actor(
    char="P",
    color=(237, 24, 52),
    name="Angry Professor",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_armorclass=3, base_strength=9, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=120),
)

paulla_wallace = Actor(
    char="W",
    color=(255, 132, 0),
    name="Walla Paulice",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_armorclass=5, base_strength=10, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=300),
)

spider = Actor(
    char="x",
    color=(189, 214, 217),
    name="Itsy Bitsy Spider",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_armorclass=0, base_strength=0, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=10),
)

renderfarm_animal = Actor(
    char="n",
    color=(165, 29, 219),
    name="Renderfarm Animal",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_armorclass=0, base_strength=5, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

door_strength = random.randint(5,50)
closed_door = Actor(
    char="B",
    color=(219, 156, 26),
    name="Closed Door",
    ai_cls=ClosedDoor,
    equipment=Equipment(),
    fighter=Fighter(hp=door_strength, base_armorclass=0, base_strength=0, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
)

############################################################## Healing

energy_drink = Item(
    char="!",
    color=(148, 252, 50),
    name="Energy Drink",
    consumable=consumable.HealingConsumable(amount=4)
)

meal_plan = Item(
    char="+",
    color=(219, 218, 134),
    name="Spare Meal Plan",
    consumable=consumable.HealingConsumable(amount=10)
)

stolen_chipotle = Item(
    char="~",
    color=(237, 175, 19),
    name="Unattended Chipotley Delivery",
    consumable=consumable.HealingConsumable(amount=6)
)

nice_note = Item(
    char="&",
    color=(255,230,210),
    name="Nice Note from Your Friends",
    consumable=consumable.HealingConsumable(amount=1)
)

############################################################## Spells

deadline_list = Item(
    char="?",
    color=(234, 177, 252),
    name= "List of Deadlines",
    consumable=consumable.FatigueDamageConsumable(damage=10, maximum_range=5),
)

ink_bottle = Item(
    char="i",
    color=(191, 180, 186),
    name= "Bottle of Ink",
    consumable=consumable.InkDamageConsumable(damage=15, maximum_range=3),
)
parent_phone = Item(
    char="I",
    color=(115, 73, 98),
    name= "Strudent Parent Contsct Info",
    consumable=consumable.ParentDamageConsumable(damage=5, maximum_range=7),
)

complicated_math_equation = Item(
    char="?",
    color=(66, 245, 239),
    name ="Complicated Math Equasions",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
    

stink_bomb = Item(
    char="Q",
    color=(144, 173, 10),
    name="Stink Bomb",
    consumable=consumable.StinkBombConsumable(damage=12, radius=3),
)

############################################################## Weapons

computer_mouse = Item(
    char="o",
    color=(202, 219, 230),
    name="Computer Mouse",
    equippable=equippable.ComputerMouse(),
)

keyboard = Item(
    char="/",
    color=(202, 219, 230),
    name="Keyboard",
    equippable=equippable.Keyboard(),
)

emergency_towel = Item(
    char="t",
    color=(143, 184, 174),
    name="Emergency Towel",
    equippable=equippable.EmergencyTowel(),
)

pepper_spray = Item(
    char="p",
    color=(81, 122, 29),
    name="Pepper Spray",
    equippable=equippable.PepperSpray(),
)

wand = Item(
    char="/",
    color=(209, 138, 184),
    name="Magical Wand",
    equippable=equippable.Wand(),
)

nerf_blaster = Item(
    char="F",
    color=(247, 145, 49),
    name="Sparkly Nefr Blaster",
    equippable=equippable.SparklyBlaster(),
)


############################################################## Armor

face_mask = Item(
    char="{",
    color=(138, 183, 212),
    name="Face Mask",
    equippable=equippable.FaceMask(),
)

hoodie = Item(
    char="[",
    color=(191, 179, 172),
    name="Comfy Hoodie",
    equippable=equippable.Hoodie(),
)

sunglasses = Item(
    char="{",
    color=(138, 183, 212),
    name="Cool Sunglasses",
    equippable=equippable.Sunglasses(),
)

platforms = Item(
    char="[",
    color=(191, 179, 172),
    name="Platform Boots",
    equippable=equippable.Platforms(),
)

partyhat = Item(
    char="{",
    color=(138, 183, 212),
    name="Party Hat",
    equippable=equippable.PartyHat(),
)

costume = Item(
    char="[",
    color=(191, 179, 172),
    name="halloween Constume",
    equippable=equippable.HalloweenCostume(),
)

############################################################## Ring

the_one_ring = Item(
    char="=",
    color=(224, 36, 190),
    name="The One Ring",
    equippable=equippable.TheOneRing(),
)

magic_mood_ring = Item(
    char="=",
    color=(148, 3, 252),
    name="Pink Mood Ring",
    equippable=equippable.MagicMoodRing(),
)

strength_mood_ring = Item(
    char="=",
    color=(168, 240, 0),
    name="Green Mood Ring",
    equippable=equippable.StrengthMoodRing(),
)

armorclass_mood_ring = Item(
    char="=",
    color=(15, 248, 252),
    name="Blue Mood Ring",
    equippable=equippable.ArmorClassMoodRing(),
)

############################################################## Other

epilouge = Item(
    char="&",
    color=(8, 153, 15),
    name="Epilouge",
    consumable=consumable.Endgame()
)
