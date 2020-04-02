from quest.game import QuestGame
from quest.map import TiledMap
from quest.sprite import Background, Wall
import arcade
import os
from pathlib import Path

def resolve_path(relative_path):
    """A helper function to find images and other resources.
    """
    here = Path(os.path.abspath(__file__)).parent
    return str(here / relative_path)

class IslandAdventureMouse(IslandAdventure):
    """A very simple subclass of :py:class:`QuestGame`.

    To run this example::

        $ python -m quest.examples.island

    :py:class:`IslandAdventure` shows off the basic features of the Quest
    framework, loading a map and letting the player explore it.
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

    def on_mouse_motion

if __name__ == '__main__':
    game = IslandAdventureMouse()
    game.run()
