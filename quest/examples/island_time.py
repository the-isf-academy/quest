# island_time.py
#
# game that extends the basic island game to implement a clock that changes the
# appearance of the sprites based on the time of the game

from quest.examples.island import IslandAdventure
from quest.engines import ContinuousPhysicsEngine
from quest.helpers import SpriteListList
import arcade
import os
from pathlib import Path

class IslandTime(IslandAdventure):

    def on_update(self, delta_time):
        """Updates the game's state.

        At every tick, the game needs to be updated. The physics engine
        updates sprite positions, and then sprite callbacks are executed.
        Finally, the viewport is scrolled. Note that `on_update` changes the
        state of the game, but does not draw anything to the screen.

        Args:
            delta_time: How much time has passed since the last update.
        """
        super().on_update(delta_time)

    def setup_physics_engine(self):
        """Uses :py:class:`TimeEngine` instead of the standard :py:class:`ContinuousPhysicsEngine`.
        The result is that the sprites in the game change their appearance as time progresses in
        the game.
        """
        self.physics_engine = TimeEngine(self)

class TimeEngine(ContinuousPhysicsEngine):

    def __init__(self, game):
        super().__init__(game)
        all_sprite_lists = [self.player_list, self.wall_list, self.npc_list]
        curr_map = self.game.get_current_map()
        for layer in curr_map.layers:
            all_sprite_lists.append(layer.sprite_list)
        self.all_sprites = SpriteListList(all_sprite_lists)

    def update(self):
        super().update()
        for sprite in self.all_sprites:
            sprite.color = (255, 255, 255)

if __name__ == '__main__':
    game = IslandTime()
    game.run()
