####

from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item

    

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine
        
    def perform(self) -> None:
        raise NotImplementedError()

class PickupAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory
        #print("trying to pick up")

        for item in self.engine.game_map.items:
            if actor_location_x ==item.x and actor_location_y == item.y:
                if len(inventory.items)>= inventory.capacity:
                    raise exceptions.Impossible("Sadly not everyone gets a place in your pocket.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up a {item.name}. Neat!")
                return

        raise exceptions.Impossible("You stare at the empty floor... there is nothing to pick up there.")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) ->None:
        self.entity.inventory.drop(self.item)


##class EscapeAction(Action):
##    def perform(self) -> None:
##        raise SystemExit()

class WaitAction(Action):
    def perform(self) -> None:
        pass

class TakeStairsAction(Action):
    def perform(self) -> None:
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You stumble down the stairs.", color.descend
            )
        else:
            raise exceptions.Impossible("You cannot dig yourself a hole and sit in it.")

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)
        

    def perform(self) -> None:
        raise NotImplementedError()



class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("You are trying to hit the air... Not gonna work")
        damage = self.entity.fighter.strength - target.fighter.armorclass

        attack_desc = F"{self.entity.name.capitalize()} tries to strangle {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} and it hurts for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
         self.engine.message_log.add_message(
             f"{attack_desc}, but is too weak to deal any damage.", attack_color
        )
        

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

#You really can not walk trough walls... yet.
        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            raise exceptions.Impossible("Trying to walk off the map will do you no good.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise exceptions.Impossible("You really can not walk trough walls... yet.")
#            raise exceptions.Impossible()

        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            raise exceptions.Impossible("Eyes up! Someone is standing in your way!")

        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()



        
