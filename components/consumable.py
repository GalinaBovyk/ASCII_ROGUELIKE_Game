#
#
#
#

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import random
import color
import tcod
import components.ai
import components.inventory
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import ActionOrHandler, AreaRangedAttackHandler, SingleRangedAttackHandler, EndgameEventHandler

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError()

    def consume(self) -> None:
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)

class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered> 0:
            self.engine.message_log.add_message(
                f"You shove the {self.parent.name} down your throat and feel {amount_recovered} HP healthier!",
                color.health_recovered,
            )
            self.consume()

        else:
            raise Impossible("You feel like you are already at your best.")

class FatigueDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction)-> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0
        self.act_damage = consumer.fighter.magic + self.damage + random.randint(0,5)

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance
    

        if target:
            self.engine.message_log.add_message(
                f"You read out a list of the upcomping deadlines. A wave of exhaustion washes over {target.name} and it takes {self.act_damage} damage."
            )
            target.fighter.take_damage(self.act_damage)
            self.consume()
        else:
            raise Impossible("No one is close enough to strike.")

class InkDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction)-> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0
        self.act_damage = consumer.fighter.magic + self.damage + random.randint(0,5)

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance
    

        if target:
            self.engine.message_log.add_message(
                f"You fake trip in front of the {target.name} and spill ink over its homework. {target.name} fails their assigment and takes {self.act_damage} damage."
            )
            target.fighter.take_damage(self.act_damage)
            self.consume()
        else:
            raise Impossible("No one is close enough to strike.")

class ParentDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction)-> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0
        self.act_damage = consumer.fighter.magic + self.damage + random.randint(0,5)

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance
    

        if target:
            self.engine.message_log.add_message(
                f"You call {target.name}'s parents and tell them how much of a faliure {target.name} is. {target.name} is consumed by shame and takes {self.act_damage} damage."
            )
            target.fighter.take_damage(self.act_damage)
            self.consume()
        else:
            raise Impossible("No one is close enough to strike.")
        


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Choose target location.", color.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor
        self.act_number_of_turns = self.number_of_turns + consumer.fighter.magic


        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("It's too dark to focus on a target.")
        if not target:
            raise Impossible("Don't waste the scroll on empty space. Target someone!")
        if target is consumer:
            raise Impossible ("You are already confused as it is, you should target someone else.")

        self.engine.message_log.add_message(
            f"You say a complicated mathematical term. Last braincells leave {target.name}'s eyes and it starts to stumble around.",
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.act_number_of_turns,
        )
        self.consume()


class StinkBombConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage 
        self.radius = radius
    def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
        self.engine.message_log.add_message(
            "Choose where to throw the Stink Bomb", color.needs_target
        )
        
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        

    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy
        consumer = action.entity
        self.act_damage = consumer.fighter.magic + self.damage + random.randint(0,5)

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("It's too dark to focus on a target.")
        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <=self.radius:
                self.engine.message_log.add_message(
                    f"A Stink Cloud engulfs the {actor.name}, making it cough out its lungs for {self.act_damage} damge!"
                )
                actor.fighter.take_damage(self.act_damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("No one is here to witness your Stink Bomb, so you decide to save it for later.")
        self.consume()

class Endgame(Consumable):
  #  def __init__(self):

    def get_action(self, consumer: Actor) -> EndgameEventHandler:
        return EndgameEventHandler(self.engine)


    def activate(self, action: actions.ItemAction) -> EndgameEventHandler:
        self.engine.message_log.add_message(
            "You pick up the note and write on it everything you and the Python talked about.", color.white
        )
        return EndgameEventHandler(self.engine)












            
