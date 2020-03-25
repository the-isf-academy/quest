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
from time import time

class IslandTime(IslandAdventure):

    def __init__(self):
        """Initializes the game and begins tracking the time since the game began.
        """
        self.start_time = time()
        super().__init__()

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

    CYCLE_SECS = 30
    MAX_DARKNESS = 100

    def __init__(self, game):
        """Initializes the :py:class:`ContinuousPhysicsEngine` and then adds a property to track all
        of the sprites in the game to be used for time updates.
        """
        super().__init__(game)
        all_sprite_lists = [self.player_list, self.wall_list, self.npc_list]
        curr_map = self.game.get_current_map()
        for layer in curr_map.layers:
            all_sprite_lists.append(layer.sprite_list)
        self.all_sprites = SpriteListList(all_sprite_lists)

    def update(self):
        """Updates the game using the update() function from the :py:class:`ContinuousPhysicsEngine`
        and then updates the shade of the sprites in the game based on the time that has passed
        since the game started.

        Calculates shade by converting the time passed since the start of the game to a percentage
        of the current time cycle ()
        """
        super().update()
        time_since_start = time()-self.game.start_time
        color_value = (time_since_start%self.CYCLE_SECS)/self.CYCLE_SECS*(255-self.MAX_DARKNESS) + self.MAX_DARKNESS
        for sprite in self.all_sprites:
            sprite.color = (color_value, color_value, color_value)

if __name__ == '__main__':
    game = IslandTime()
    game.run()
