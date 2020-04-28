from quest.contrib.removable import RemovableMixin
from quest.contrib.submodal import SubmodalMixin, CLOSE_SUBMODAL
from quest.modal import Modal
from collections import Counter
import arcade

class InventoryMixin(RemovableMixin):
    """A mixin for QuestGame which provides an inventory. 

    Pick up and drop  behavior can be implemented in a very simple way 
    because `RemovableMixin` provides most of what we need. Also creates an 
    `InventoryModal` and binds a key to open it (by default, 'i').

    Attributes:
        inventory_shortcut: A key which should open the inventory.
    """
    inventory_shortcut = arcade.key.I

    def __init__(self):
        self.removed_sprite_list_names.append("inventory")
        super().__init__()
        self.inventory_modal = InventoryModal(self, self.inventory())

    def inventory(self):
        "A helper to return the inventory"
        return self.removed_sprite_lists['inventory']

    def pick_up(self, sprite):
        """Removes a sprite from the game and adds it to the inventory.
        """
        self.remove_sprite_from_game(sprite, "inventory")

    def drop(self, sprite):
        """Removes a sprite from the inventory and adds it to the game.

        Moves the sprite to the player's position and sets its `dropped_by` property
        to the player (to make sure it doesn't immediately get picked up).
        """
        self.add_sprite_to_game(sprite)
        sprite.recently_dropped = True
        sprite.center_x = self.player.center_x
        sprite.center_y = self.player.center_y

    def on_key_press(self, key, modifier):
        """Overrides `on_key_press` so that when the inventory shortcut key is
        pressed, opens the inventory. Otherwise, delegates to the parent 
        `on_key_press` method.
        """
        if key == self.inventory_shortcut:
            self.open_modal(self.inventory_modal)
        else:
            super().on_key_press(key, modifier)

class InventoryItemMixin:
    """A mixin for QuestSprite which allows it to behave as an inventory item.

    Attributes:
        detailed_description (str): A more detailed description.
        dropped_by (QuestSprite): Keeps track of whether the sprite was recently dropped. 
        usable (bool): Indicates whether the item can be used. 
    """

    detailed_description = "An inventory item"
    recently_dropped = False
    usable = False

    def on_update(self, game):
        """When this sprite has recently been dropped, checks to see whether the 
        dropped (probably the player) is still colliding. If not, sets `self.dropped_by`
        to None, indicating that the sprite can be picked up again.
        """
        if self.recently_dropped:
            if not self.collides_with_sprite(game.player):
                self.recently_dropped = False

    def on_collision(self, sprite, game):
        """Causes the sprite to be picked up, unless it was just dropped.
        """
        if sprite == game.player and not self.recently_dropped:
            game.pick_up(self)

    def use(self, game):
        """What should happen when used. By default, kills the item.
        """
        self.kill()
            
class InventoryModal(SubmodalMixin, Modal):
    """An extension of Modal which interaacts with inventories.
    """
    welcome_message = "Your inventory:"
    close_modal_option = "OK"

    def __init__(self, game, inventory):
        self.inventory = inventory
        super().__init__(game)

    def text_label_contents(self):
        return [self.welcome_message]

    def option_label_contents(self):
        return self.item_descriptions() + [self.close_modal_option]

    def choose_option(self, value):
        if value == len(self.item_counts()):
            self.game.close_modal()
        else:
            chosen_description = self.option_label_contents()[value]
            for item in self.inventory:
                if chosen_description.startswith(item.description):
                    count = self.item_counts()[item.description]
                    self.submodal = InventoryItemModal(self.game, item, count)
                    return

    def item_counts(self):
        """Returns a dictionary of {item_description: count}
        """
        return Counter([item.description for item in self.inventory])

    def item_descriptions(self):
        """Returns a list of item descriptions, each including the item's count.
        """
        return ["{} ({})".format(desc, count) for desc, count in sorted(self.item_counts().items())]

class InventoryItemModal(Modal):
    """A modal for interacting with an inventory item. 
    """
    verbs = ["drop", "back"]

    def __init__(self, game, item, count):
        self.item = item
        self.count = count
        super().__init__(game)

    def text_label_contents(self):
        return [
            "{} ({})".format(self.item.description, self.count),
            self.item.detailed_description
        ]

    def option_label_contents(self):
        if self.item.usable:
            return ["use"] + self.verbs
        else:
            return self.verbs

    def choose_option(self, value):
        verb = self.option_label_contents()[value]
        if verb == "drop":
            self.game.drop(self.item) 
        if verb == "use":
            self.item.use(self.game)
        return CLOSE_SUBMODAL

