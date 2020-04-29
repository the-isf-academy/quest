import arcade
from quest.modal import AlertModal
from quest.contrib.removable import RemovableMixin
from quest.contrib.submodal import SubmodalMixin, CLOSE_SUBMODAL
from quest.contrib.inventory import (
    InventoryModal, 
    InventoryItemModal, 
    InventoryItemMixin
)

class ShopMixin(RemovableMixin):
    """A mixin for `QuestGame` which implements a shop.
    """
    shop_shortcut = arcade.key.Z
    money = 0

    def __init__(self):
        super().__init__()
        self.shop_modal = ShopModal(self, self.removed_sprite_lists['shop'])

    def shop_inventory(self):
        "A helper to return the shop inventory"
        return self.removed_sprite_lists['shop']

    def on_key_press(self, key, modifier):
        """Overrides `on_key_press` so that when the inventory shortcut key is
        pressed, opens the inventory. Otherwise, delegates to the parent 
        `on_key_press` method.
        """
        if key == self.shop_shortcut:
            self.open_modal(self.shop_modal)
        else:
            super().on_key_press(key, modifier)

    def buy_item(self, item):
        """Buys an item.

        Reduces money by the item's price, removes the item from the shop inventory,
        and (if InventoryMixin is also being used) adds the item to the player's inventory.
        """
        self.money -= item.price
        self.shop_inventory().remove(item)
        if hasattr(self, "inventory"):
            self.inventory().append(item)

class ShopItemModal(SubmodalMixin, InventoryItemModal):
    purchase_message = "Pleasure doing business with you."
    fail_message = "Uh, you can't afford that."
    verbs = ["buy", "back"]

    def text_label_contents(self):
        return [
            "[${}] {}".format(self.item.price, self.item.description),
            self.item.detailed_description,
            self.money_message()
        ]

    def choose_option(self, value):
        verb = self.option_label_contents()[value]
        if verb == "buy":
            if self.item.price <= self.game.money:
                self.game.buy_item(self.item)
                self.submodal = AlertModal(self.game, self.purchase_message)
            else:
                self.submodal = AlertModal(self.game, self.fail_message)
        #return CLOSE_SUBMODAL

    def money_message(self):
        return "You have ${}.".format(self.game.money)

class ShopModal(InventoryModal):
    """Opens a shop modal. 
    
    A shop is really just an inventory--someone else's inventory--that you can 
    buy stuff from. Therefore, we can easily implement ShopModal by subclassing
    InventoryModal.
    """
    welcome_message = "Welcome to the shop."
    close_modal_option = "Thanks, bye."
    detail_modal_class = ShopItemModal

    def item_descriptions(self):
        return ["[${}] {}".format(i.price, i.description) for i in self.inventory]
