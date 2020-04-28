# shop.py example game
# by Team Yoshi and Jacob Wolf

from quest.dialogue import Dialogue
from quest.modal import DialogueModal
from quest.helpers import resolve_resource_path
from quest.examples.grandmas_soup import GrandmasSoupGame
from quest.contrib.shop import ShopMixin
from quest.contrib.coin import CoinMixin


NUM_ITEMS_FOR_SOUP = 7
DIALOGUE_FILE = "contrib/grandma_shop.ink"
MAP = "images/island/island_walkable.tmx"


class GrandmasSoupShop(ShopMixin, CoinMixin, GrandmasSoupGame):
    """Grandma has moved into the 21st century and foraging will no longer do,
    Now, in addition to foraging items, you'll need to collect coins so you
    can purchase the items which aren't available on your island.

    This game demonstrates how to use a shop attribute as part of a game.

    Attributes:
        coins: variable to store the number of coins the player has collected.
    """

    shop_file = "contrib/shop.txt"
    total_coins = 10
    map_dimensions = [1000, 1000]

    def __init__(self):
        super().__init__()
        self.dialogue = Dialogue.from_ink(resolve_resource_path(DIALOGUE_FILE))
        self.modal = DialogueModal(self, self.dialogue)

    def got_item(self, description):
        super().got_item(description)
        if len(self.items) < NUM_ITEMS_FOR_SOUP:
            self.dialogue.run(self.items[-1])
        else:
            self.dialogue.run("SOUP")


if __name__ == '__main__':
    game = GrandmasSoupShop()
    game.run()
