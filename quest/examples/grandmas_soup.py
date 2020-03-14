from quest.game import QuestGame
from quest.map import TiledMap
from quest.dialogue import Dialogue
from quest.modal import Modal, DialogueModal
from quest.sprite import QuestSprite, Wall, NPC
from quest.helpers import scale
from quest.strategy import RandomWalk
import arcade
import os
from pathlib import Path

def resolve_path(relative_path):
    here = Path(os.path.abspath(__file__)).parent
    return str(here / relative_path)

class Grandma(NPC):
    repel_distance = 10

    def on_collision(self, sprite, game):
        self.repel(sprite)
        game.talk_with_grandma()

    def repel(self, sprite):
        "Backs the sprite away from self"
        away = (self.center_x - sprite.center_x, self.center_y - sprite.center_y)
        away_x, away_y = scale(away, self.repel_distance)
        sprite.center_x = sprite.center_x - away_x
        sprite.center_y = sprite.center_y - away_y
        sprite.stop()

class Item(NPC):
    description = "item"
    def on_collision(self, sprite, game):
        game.got_item(self.description)
        self.kill()

class Carrots(Item):
    description = "carrots"

class Mushroom(Item):
    description = "mushroom"

class Potatoes(Item):
    description = "potatoes"

class Tomatos(Item):
    description = "tomatos"

class GrandmasSoupGame(QuestGame):
    """A very simple subclass of :py:class:`QuestGame`.

    :py:class:`GrandmasSoupGame` shows off the basic features of the Quest 
    framework, loading a map and letting the player explore it. 
    To run this example, make sure you have 
    :doc:`installed Quest <tutorial/install>`. Then run::

        $ python -m quest.examples.island

    After you play it, check out the sorce code by clicking on "source" in the
    blue bar just above.
    """

    player_sprite_image = resolve_path("images/boy_simple.png")
    screen_width = 500
    screen_height = 500
    left_viewport_margin = 96                            
    right_viewport_margin = 96
    bottom_viewport_margin = 96
    top_viewport_margin = 96
    player_initial_x = 300
    player_initial_y = 300
    player_speed = 8

    def __init__(self):
        super().__init__()
        self.dialogue = Dialogue.from_ink(resolve_path("grandma.ink"))
        self.modal = DialogueModal(self, self.dialogue)
        self.items = []

    def run(self):
        super().run()

    def setup_maps(self):
        """Sets up the map.

        Uses a :py:class:`TiledMap` to load the map from a ``.tmx`` file,
        created using :doc:`Tiled <tiled:manual/introduction>`. The layers
        in the map are assigned :doc:`roles <narrative/map>` so that their 
        sprites behave in particular ways.
        """
        super().setup_maps()
        sprite_classes = {
            "Obstacles": Wall,
            "Background": QuestSprite,
        }
        self.add_map(TiledMap(resolve_path("images/island/island.tmx"), sprite_classes))

    def setup_walls(self):
        self.wall_list = self.get_current_map().get_layer_by_name("Obstacles").sprite_list

    def setup_npcs(self):
        npc_data = [
            [Grandma, "images/people/grandma.png", 3, 400, 400],
            [Carrots, "images/items/carrots.png", 1, 220, 640],
            [Mushroom, "images/items/mushroom.png", 1, 1028, 264],
            [Potatoes, "images/items/potatoes.png", 1, 959, 991],
            [Tomatos, "images/items/tomatos.png", 1, 323, 1055],
        ]
        self.npc_list = arcade.SpriteList()
        for sprite_class, image, scale, x, y in npc_data:
            sprite = sprite_class(resolve_path(image), scale)
            sprite.center_x = x
            sprite.center_y = y
            self.npc_list.append(sprite)

        grandma = self.npc_list[0]
        walk = RandomWalk()
        grandma.strategy = walk

    def talk_with_grandma(self):
        self.open_modal(self.modal)

    def got_item(self, description):
        self.items.append(description.upper())
        if len(self.items) < 4:
            self.dialogue.run(self.items[-1])
        else:
            self.dialogue.run("SOUP")

if __name__ == '__main__':
    game = GrandmasSoupGame()
    game.run()
