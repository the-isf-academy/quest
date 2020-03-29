# island_time.py
#
# game that extends the basic island game to implement a clock that changes the
# appearance of the sprites based on the time of the game

from quest.examples.island import IslandAdventure
from quest.engines import ContinuousPhysicsEngine, DiscretePhysicsEngine
import arcade
import os
from pathlib import Path

class IslandTime(IslandAdventure):

    def setup_physics_engine(self):
        """Passes optional `time` parameter to the standard :py:class:`ContinuousPhysicsEngine`.
        The result is that the sprites in the game change their appearance as time progresses in
        the game.
        """
        self.physics_engine = ContinuousPhysicsEngine(self, time=True)

if __name__ == '__main__':
    game = IslandTime()
    game.run()
