# shop.py example game
# by Team Yoshi and Jacob Wolf

import arcade
from quest.modal import Modal
from quest.text_label import TextLabelStack
from quest.helpers import resolve_resource_path


class ShopMixin:
    """ A mixin to add a shop to your game.

    Note that you will still need to add coins to the game in order
    to have something to shop with.
    """
    def __init__(self):
        super().__init__()
        self.shop = ShopModal(self, self.shop_file)
        self.item = []

    def on_key_press(self, key, modifiers):
        """Handles key pressess to open and shop.
        """
        super().on_key_press(key, modifiers)
        if key == arcade.key.Z:
            self.open_modal(self.shop)

    def got_item(self, description):
        """Adds item to list of items.
        """
        self.items.append(description.upper())


class ShopModal(Modal):
    """An extension of the modal class that implements a shop based
    a dictionary of items passed to the class constructor.

    Attributes:
        shop_dict: dictionary of item:price pairs
    """

    def __init__(self, game, shop_file):
        self.game = game
        self.shop_file = resolve_resource_path(shop_file)
        self.x_center = 0
        self.y_center = 0
        self.setup_shop()
        self.set_text_labels(self.shop_text["welcome"])
        self.set_option_labels(list(self.shop_items.keys()))

    def setup_shop(self):
        """Sets up a dictionary of shop items and their prices, a dictionary
        of scripts to put in place of shop (including welecome, item-purchased,
        select-item, and insufficient-funds), and a dictionary for shop options
        including (yes, no, and exit).
        """
        self.shop_items = {}
        self.shop_text = {}
        self.shop_options = {}
        self.read_shop_from_file(
            self.shop_file,
            self.shop_items,
            self.shop_text,
            self.shop_options
            )

    def format_item_description(self, item):
        """Formats the item's description to include the long name of the item
        with it's price followed by the description of the item.

        Args:
            item: dictionary of item properties

        Returns:
            list of strings where each string is a line in the item's full
                description
        """
        item_title = "{} ({} coins)".format(item["long_name"], item["price"])
        item_description = item["description"]
        return [item_title, item_description]

    def update_position(self, x, y):
        self.x_center = x
        self.y_center = y
        self.set_text_labels(self.shop_text["welcome"])
        self.set_option_labels(list(self.shop_items.keys()))

    def set_text_labels(self, text_list):
        """Sets the text of the modal to the text_list strings

        Args:
            text_list: list of strings for each line of the modal text
        """
        self.text_labels = TextLabelStack(
            text_list,
            self.x_center,
            self.y_center + self.height / 2
        )

    def set_option_labels(self, options_list):
        """Sets the options for the modal to the items in the options_list.
        Always appends the exit shop option to the list

        Args:
            options_list: list of strings for each option to display
        """
        options_list.append(self.shop_options["exit"])
        self.option_labels = TextLabelStack(
            options_list,
            self.x_center,
            self.y_center + 100
        )
        self.option_labels.set_highlight(0)

    def choose_option(self, value):
        """Implements the logic for running the shop modal. Assumes that the
        interaction will start on the welcome text with the list of items
        available for purchase. Interaction always follows the same flow:
        text/item_choice? --> description/purchase_item? --> text/item_choice?
        Interaction can always be stopped by choosing exit option.

        Note: the text of the interaction is populated by the shop_text and
        shop_items dictionary. You will only need to change this function if
        you want to change the flow of the interaction.
        """
        # choose to purchase item
        if value == self.shop_options["yes"]:
            item_value = int(self.shop_items[self.item_selected]["price"])
            if item_value <= self.game.coins_collected:
                # funds available, purchase item
                self.game.coins_collected -= item_value
                self.game.got_item(self.item_selected)
                self.set_text_labels(self.shop_text["item-purchased"])
                self.set_option_labels(list(self.shop_items.keys()))
            else:
                # funds not available, return to item list
                self.set_text_labels(self.shop_text["insufficient-funds"])
                self.set_option_labels(list(self.shop_items.keys()))
        elif value == self.shop_options["no"]:
            # choose not to purchase item
            self.item_selected = None
            self.set_text_labels(self.shop_text["select-item"])
            self.set_option_labels(list(self.shop_items.keys()))
        elif value == self.shop_options["exit"]:
            # exit shop
            self.item_selected = None
            self.game.close_modal()
        else:
            # choose an item to read more about
            self.item_selected = value
            item_description = self.format_item_description(self.shop_items[value])
            self.set_text_labels(item_description)
            self.set_option_labels([self.shop_options["yes"], self.shop_options["no"]])

    def on_key_press(self, key, modifiers):
        """Interprets key presses when the shop modal is open. If up or down key
        pressed, changes the highlighted option. If enter pressed, chooses the
        currenlty highlighted option.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            i = (self.option_labels.get_highlight() - 1) % len(self.option_labels)
            self.option_labels.set_highlight(i)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            i = (self.option_labels.get_highlight() + 1) % len(self.option_labels)
            self.option_labels.set_highlight(i)
        elif key == arcade.key.ENTER:
            self.choose_option(self.option_labels.get_highlight(value=True))

    def read_shop_from_file(self, shop_file, shop_items, shop_text, shop_options):
        """Reads the shop file in self.shop_file and populates the shop_items,
        shop_text, and shop_options dictionaries. File should have three sections
        separated by blank lines. See shop.txt for more specific formatting.
        """
        with open(shop_file) as f:
            # reading items
            line = f.readline().strip("\n")
            while "#" in line:
                line = f.readline().strip("\n")
            while True:
                if "#" in line:
                    continue
                if len(line) == 0:
                    break
                item = line
                shop_items[item] = {}
                while True:
                    line = f.readline().strip("\n")
                    if "#" in line:
                        continue
                    if ":" not in line:
                        break
                    key, value = line.split(": ")
                    shop_items[item][key] = value

            # reading text
            line = f.readline().strip("\n")
            while "#" in line:
                line = f.readline().strip("\n")
            while True:
                if "#" in line:
                    continue
                if len(line) == 0:
                    break
                text_type = line
                shop_text[text_type] = []
                while True:
                    line = f.readline().strip("\n")
                    if "#" in line:
                        continue
                    if "->" not in line:
                        break
                    text = line[3:]
                    shop_text[text_type].append(text)

            # reading options
            while True:
                line = f.readline().strip("\n")
                if "#" in line:
                    continue
                if len(line) == 0:
                    break
                option_type, option_text = line.split(": ")
                shop_options[option_type] = option_text
