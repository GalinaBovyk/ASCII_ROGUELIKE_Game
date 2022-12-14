####################
# 
# Galina Bovykina
# November 16 2022
#
# This is a library of reactions to player inputs.
# Code adopted from TStand90 rogueliketutorials.com
#
####################

from __future__ import annotations
import os
from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union
import tcod.event
import actions
from actions import Action, BumpAction, PickupAction, WaitAction
import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

# These are dictionaries of key actions
MOVE_KEYS = {
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),

    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),

}

WAIT_KEYS ={
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,

}

CONFIRM_KEYS = {
    tcod.event.K_RETURN,
    tcod.event.K_KP_ENTER,
    tcod.event.MouseButtonDown
}

ActionOrHandler = Union[Action, "BaseEventHandler"]
""" """

# This determines what's an event & if can happen in the first place
class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventhandler:
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self
    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()
    
    def ev_quit(self, console: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit


# This is specifically for the main menue pop-ups
class PopupMessage(BaseEventHandler):
    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.Console) -> None:
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //=8
        console.tiles_rgb["bg"] //=8

        console.print(
            console.width//2,
            console.height//2,
            self.text,
            fg=color.white,
            bg=color.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        return self.parent


# This is the basic class that handles events
class EventHandler(BaseEventHandler):

    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            if not self.engine.player.is_alive:
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)
        return self

    def handle_action(self, action: Option[Action]) -> bool:
        if action is None:
            return False
        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False
        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True
    
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)

# This event handler reacts to a player choosing somehting is a display
class AskUserEventHandler(EventHandler):
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        if event.sym in {
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return self.on_exit()

    #####  This part was specifically modified by me  #####
    #  For convinience I switched the exit button to confirm keys
    def ev_mousebuttondown(
        self, event: tcod.event.KeyDown 
    ) -> Optional[ActionOrHandler]:
        key = event.sym
        if tcod.event.MouseButtonDown:
            return self.on_exit()
        elif key in CONFIRM_KEYS:
            return self.on_exit()
            
        return None

    def on_exit(self) -> Optional[ActionOrHandler]:
        return MainGameEventHandler(self.engine)


# This shows the player the basic character stats display
class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Things That are Neat about You"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x= 0
        y = 0
        width = len(self.TITLE) +4
        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=10,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0,0,0),
        )
        console.print(
            x=x +1, y=y +2, string=f"{self.engine.player.name}"
        )
        console.print(
            x=x +1, y=y +3, string=f"Level: "
            f"{self.engine.player.level.current_level}"
        )
        console.print(
            x=x +1, y=y + 4, string=f"XP: "
            f"{self.engine.player.level.current_xp}"
        )
        console.print(
            x=x +1,
            y=y +5,
            string=f"XP untill next Level: "
            f"{self.engine.player.level.experience_to_next_level}",
        )
        console.print(
            x=x +1, y=y + 6, string=f"Strength Mod: "
            f"+{self.engine.player.fighter.strength}"
        )
        console.print(
            x=x +1, y=y +7, string=f"Armor Class: "
            f"{self.engine.player.fighter.armorclass}"
        )
        console.print(
            x=x +1, y=y +8, string=f"Magic Mod: "
            f"+{self.engine.player.fighter.magic}"
        )
        

# Thid handles the leveling up display
class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <=30:
            x= 40
        else:
            x = 0
        console.draw_frame(
            x=x,
            y=0,
            width=35,
            height=9,
            title=self.TITLE,
            clear=True,
            fg=(255,255,255),
            bg=(0,0,0),
        )

        console.print(x=x + 1, y=1, string="Quick Note:"
                      "You leveled up!")
        console.print(x=x + 1, y=2, string="Select an "
                      "attribute to increase.")

        console.print(
            x=x  +1,
            y=4,
            string=f"a) Health (+5 HP from "
            f"{self.engine.player.fighter.max_hp})",
        )

        console.print(
            x=x  +1,
            y=5,
            string=f"b) Strength (+1 from "
            f"{self.engine.player.fighter.strength})",
        )

        console.print(
            x=x  +1,
            y=6,
            string=f"c) Armour Class (+1 from "
            f"{self.engine.player.fighter.armorclass})",
        )

        console.print(
            x=x  +1,
            y=7,
            string=f"d) Magic Power (+1 from "
            f"{self.engine.player.fighter.magic})",
        )

    def ev_keydown(self, event: tcod.event.keyDown) ->Optional[ActionOnHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 3:
            if index == 0:
                player.level.increase_max_hp()
            elif index ==1:
                player.level.increase_strength()
            elif index == 2:
                player.level.increase_armorclass()
            else:
                player.level.increase_magic()
        else:
            self.engine.message_log.add_message("Invalid entry.", color.invalid)
            return None
        return super().ev_keydown(event)

    def ev_mousebutton(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOnhandler]:

        return None

# This handles the inventory
class InventoryEventHandler(AskUserEventHandler):
    TITLE = "<missing title>"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)

        height = number_of_items_in_inventory + 2
        if height <=3:
            height = 3

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0
        y = 0

        width = len(self.TITLE) + 14

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(20, 20, 20),
        )
        if number_of_items_in_inventory>0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)

                is_equipped = self.engine.player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                if is_equipped:
                    item_string = f"{item_string} (wearing rn)"

                console.print(x +1, y + i + 1, item_string)
        else:
            console.print(x +1, y + 1, "(empty pockets)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <=index <=26:
            try:
                selected_item = player.inventory.items[index]
                
            except IndexError:
                self.engine.message_log.add_message(
                    "Invalid entery/You dot have this item",
                    color.invalid,
                )
                return None
                
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        raise NotImplementedError()


# This is an extra subclass that specifically handles the items
# differently, depending on the type of the Item
class InventoryActivateHandler(InventoryEventHandler):
    TITLE = "What do you want to use?"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.EquipAction(self.engine.player, item)
        else:
            return None
            

# This handles removing Items from inventory
class InventoryDropHandler(InventoryEventHandler):
    TITLE = "What do you want to take out of your pockets?"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        return actions.DropItem(self.engine.player, item)


# This specifically handles inputs for scrolling
class SelectIndexHandler(AskUserEventHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        player = self.engine.player
        engine.mousee_location = player.x, player.y

    def on_render(self, console: tcod.Console) ->None:
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb["bg"][x,y] = color.white
        console.tiles_rgb["fg"][x,y] = color.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1
            if event.mod &(tcod.event.KMOD_LSHIFT| tcod.event.KMOD_RSHIFT):
                modifier *=5
            if event.mod &(tcod.event.KMOD_LCTRL| tcod.event.KMOD_RCTRL):
                modifier *=10
            if event.mod &(tcod.event.KMOD_LALT| tcod.event.KMOD_RALT):
                modifier *=20
            x,y = self.engine.mouse_location
            dx,dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            x = max(0, min(x, slef.engine.game_map.width -1))
            y = max(0, min(y, self.engine.game_map.height -1))
            self.engine.mouse_location = x,y
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)
    
    def ev_mousebutton(
        self, event: tcod.event.MouseButtonDown
    ) ->  Optional[ActionOrHandler]:
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button ==1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[AttackOrHandler]:
        raise NotImplementedError()


# This lets the main game handler to become the main event handler again
class LookHandler(SelectIndexHandler):
    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        self.engine.event_handler = MainGameEventHandler(self.engine)


# This lets the user to choose a target
class SingleRangedAttackHandler(SelectIndexHandler):
    def __init__(
        self,
        engine: Engine,
        callback: Callable[[Tuple[int, int]],
        Optional[Action]]
    ):
        super().__init__(engine)
        self.callback = callback
    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x,y))


# This selects all the entities in the user selected radius
class AreaRangedAttackHandler(SelectIndexHandler):
    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optiona[Action]],
    ):
        super().__init__(engine)

        self.radius  = radius
        self.callback = callback
        
    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        x, y = self.engine.mouse_location

        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )
    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x,y))
            

# This handles the main game events caused by user input
class MainGameEventHandler(EventHandler):

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        action: Optional[Action] = None

        key = event.sym
        modifier = event.mod

        player = self.engine.player

        if key == tcod.event.K_PERIOD and modifier &(
            tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return actions.TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == tcod.event.K_v:
            return HistoryViewer(self.engine)
        elif key == tcod.event.K_g:
            action = PickupAction(player)
        elif key == tcod.event.K_i:
            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.K_d:
            return InventoryDropHandler(self.engine)
        elif key == tcod.event.K_c:
            return CharacterScreenEventHandler(self.engine)
        elif key == tcod.event.K_SLASH:
            return LookHandler(self.engine)
        elif key == tcod.event.K_h:
            return HelpEventHandler(self.engine)
        return action


# This handles the Game over event
class GameOverEventHandler(EventHandler):
    def on_quit(self) -> None:
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")
        raise exceptions.QuitWithoutSaving()
    
    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_ESCAPE:
            self.on_quit()

CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,

}


# This creates the message log history window
class HistoryViewer(EventHandler):

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length -1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        log_console = tcod.Console(console.width - 6, console.height - 6)

        log_console.draw_frame(0,0, log_console.width, log_console.height)

        log_console.print_box(
            0,
            0,
            log_console.width,
            1,
            "Here is what you missed on the live broadcast",
            alignment=tcod.CENTER,
        )

        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor +1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust <0 and self.cursor == 0:
                self.cursor = self.log_length - 1
            elif adjust >0 and self.cursor == self.log_length -1:
                self.cursor = 0
            else:
                return MainGameEventHandler(self.engine)
            return None
        

#####  This part was specifically modified by me  #####
# All the next handlers were added in by me for a better user experience
# They were based on and expanded from the HistoryEventHandler
class HelpEventHandler(EventHandler):

    def __init__(self, engine: Engine):
        super().__init__(engine)
        

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        help_console = tcod.Console(console.width - 6, console.height - 6)

        help_console.draw_frame(0,0, help_console.width, help_console.height)

        for i, text in enumerate(
            ["So you have some questions about how to play this game?",
             "Its actually not too complicated -",
             "You desend down the Monty dungeon, gathering XP and Items.",
             "There are enemies that will try to attack you.",
             "Luckily you have STRENGTH, MAGIC and ARMOR CLASS",
             "to fight with and protect you.",
             "",
             "THE MAIN MOVEMENT CONTROLLS: ",
             "",
             "ARROW KEYS - movement",
             "NUM PAD - movement(8,4,6,2) + diagonal movement(7,9,1,3)",
             "",
             "DISPLAY CONTROLS:",
             "",
             "v - log history (press down arrow to exit)",
             "c - character stat display (press any key to exit)",
             "",
             "ACTION CONTROLS:",
             "",
             "i - display Inventory (click Enter to exit)",
             "",
             "While in the Inventory you can use an object to:",
             "",
             "1) Consume a healing object",
             "2) Wear an Item",
             "3) Cast a spell",
             "",
             "You do this by pressing the index number",
             "Some scrolls require aiming - you do that with the mouse",
             "and the confirm it with the Enter key",
             "",
             "g - grab an object from the ground(adds it to your inventory)",
             "d - drop an object from the inventory",
             "",
             "> (shift + .) - to go down the stairs",
             "",
             "if you don't know what something is - ",
             "you can point your mouse at it to find basic information",
             "(mouse click to exit)",
             ]
        ):
            help_console.print(
                help_console.width //2 +4,
                help_console.height//2 - 18 + i ,
                text.ljust(help_console.width - 5),
                fg=color.white,
                alignment=tcod.CENTER,
            )
        help_console.print_box(
            0,
            0,
            help_console.width,
            1,
            "Here is some helpful tips about controls:",
            alignment=tcod.CENTER
        )
        
        help_console.blit(console, 3, 3)


    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown,
    ) -> Optional[ActionOrHandler]:
        
        return MainGameEventHandler(self.engine)


class EndgameEventHandler(EventHandler):

    def __init__(self, engine: Engine):
        super().__init__(engine)

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        end_console = tcod.Console(console.width - 10, console.height - 12)


        end_console.draw_frame(0, 0, end_console.width, end_console.height)


        for i, text in enumerate(
                ["You: So... You are the Monty Python?",
                 " ",
                 " ",
                 " ",
                 "Monty Python: Yessss",
                 " ",
                 " ",
                 " ",
                 "You: That doesn't make any sense... "
                 " ",
                 " ",
                 " ",
                 "Monty Python: You see, it's like a referencssee...",
                 " ",
                 " ",
                 " ",
                 "You: Wait, so this whole thing is like one big joke?",
                 " ",
                 " ",
                 " ",
                 "Monty Python: I guesss...",
                 " ",
                 " ",
                 " ",
                 "You: Well that's underwhelming. "
                 " ",
                 " ",
                 " ",
                 "You: ... ",
                 " ",
                 " ",
                 " ",
                 "Monty Python: ... ",
                 " ",
                 " ",
                 " ",
                 "Monty Python: Do you want tea?",
                 ]
        ):
            end_console.print(
                end_console.width // 2 + 4,
                end_console.height // 2 - 18 + i,
                text.ljust(end_console.width - 4),
                fg=color.white,
                alignment=tcod.CENTER,
            )
        end_console.print_box(
            0, 0, end_console.width, 1, "Fnord", alignment=tcod.CENTER
        )

        end_console.blit(console, 3, 3)

    def ev_mousebuttondown(
            self, event: tcod.event.MouseButtonDown,
    ) -> Optional[ActionOrHandler]:
        return GameOverEventHandler(self.engine)
