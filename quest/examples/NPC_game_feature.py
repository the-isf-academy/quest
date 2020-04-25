class NPC_Maze_Walk(Strategy):
""" Lets NPC solve the maze game so you can vs them too!

Attributes:
      INIT_ARG_0: description of the first argument in the class's __init__() function
      INIT_ARG_1: description of the second argument in the class's __init__() function
"""
    def choose_course(self, sprite, game):
        """Possibly chooses a new random direction, then returns the current direction.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """
        if random() < self.change_prob:
            self.set_random_direction()
        return (self.x, self.y)

    def dead_end(self, sprite, game):
        """When the NPC walks into the dead_end and identify it as a dead end.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """
        if wall is 0.1m:
            list.extend(stored_coords)
        return (self.x, self.y)
        """replace the 0.1m with something python understands"""

    def stored_coords(self, sprite, game):
        """Stores data of NPC corrdinations from dead end

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).
        """
        stored_coords = []


if __name__ == '__main__':
    game = NPC_Maze_Solve()
    game.run()
