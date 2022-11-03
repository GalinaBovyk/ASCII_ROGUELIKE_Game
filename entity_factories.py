#
#
##
#


from entity import Entity

player = Entity(char="@", color=(255,255,255), name="Player", blocks_movement=True)

big_evil_snake = Entity(char="S", color=(147,244,200), name="Big EVIL Snake", blocks_movement=True)
small_evil_snake = Entity(char="s", color=(112, 219, 175), name="Small EVIL Snake", blocks_movement=True)
worm = Entity(char="s", color=(112, 28, 70), name="Worm", blocks_movement=True)
duck = Entity(char="2", color=(145, 131, 102), name="Duck", blocks_movement=True)
golden_duck = Entity(char="2", color=(219, 156, 26), name="Golden Duck", blocks_movement=True)
