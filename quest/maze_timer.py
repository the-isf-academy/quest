from quest.examples.maze import MazeGame
from quest.engines import ContinuousPhysicsEngine
import time

class MazeTimer(MazeGame):
    """An extension of the MazeGame class with a timer in it."""

    def __init__(self, init_start_time):
        """Initializes the game window and sets up other classes.
        """
        super().__init__()
        self.start_time = init_start_time

    def setup_physics_engine(self):
        """Passes optional `time` parameter to the standard :py:class:`ContinuousPhysicsEngine`.
        The result is that the sprites in the game change their appearance as time progresses in
        the game.
        """
        self.physics_engine = ContinuousPhysicsEngine(self, time=True)

    

#    def countdown(t):
        while t >= 0:
            print(t)
            t-= 1
            time.sleep(1)

#    def add_time(old_t, extra_t):
#        new_t = old_t + extra_t
#        MazeTimer.countdown(new_t)
#        return new_t

t=5
MazeTimer.countdown(t)
