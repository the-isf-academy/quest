from quest.examples.maze import MazeGame
import time

class MazeTimer(MazeGame):
    """An extension of the MazeGame class with a timer in it."""

    def __init__(self):
        """Initializes the game window and sets up other classes.
        """
        super().__init__()
        #self.timer() =

    def countdown(t):
        while t >= 0:
            print(t)
            t-= 1
            time.sleep(1)

    def add_time(old_t, extra_t):
        new_t = old_t + extra_t
#        MazeTimer.countdown(new_t)
        return new_t

t=5
MazeTimer.countdown(t)
#old_t =
t = MazeTimer.add_time(old_t, 5)
MazeTimer.countdown(t)
