from quest.game import QuestGame
from quest.map import TiledMap
from quest.sprite import Background, Wall
import arcade
import os
from pathlib import Path

def resolve_path(relative_path):
    here = Path(os.path.abspath(__file__)).parent
    return str(here / relative_path)

class IslandAdventure(QuestGame):
    """A very simple subclass of :py:class:`QuestGame`.

    :py:class:`IslandAdventure` shows off the basic features of the Quest 
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
    player_speed = 6

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
            "Background": Background,
        }
        self.add_map(TiledMap(resolve_path("images/island/island.tmx"), sprite_classes))

    def setup_walls(self):
        self.wall_list = self.get_current_map().get_layer_by_name("Obstacles").sprite_list

if __name__ == '__main__':
    game = IslandAdventure()
    game.run()
