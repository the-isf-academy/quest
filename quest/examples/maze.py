from quest.game import QuestGame
from quest.map import Map, GridMapLayer
from quest.maze import Maze
from itertools import product
import arcade
import random
from datetime import datetime

# TODO: Add a time, change to score reporting after completion

class MazeMap(Map):
    """A Map which creates a wall layer using a Maze.

    MazeMap is a subclass of Map which automatically generates a 
    maze. It uses a `quest.maze.Maze` to figure out where to put walls, 
    and adds wall sprites to a map layer in a corresponding pattern.

    Args:
        columns: The number of columns of tiles in the map
        rows: The number of rows of tiles in the map
        tile_size: The size (in pixels) of each square tile
        num_loot: The number of loot sprites to add to the map
        
    """
    def __init__(self, columns, rows, tile_size, num_loot):
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.tile_size = tile_size
        self.num_loot = num_loot
        self.maze = Maze(self.columns, self.rows)

        self.background_color = (20,80,20)
        self.add_layer(self.get_wall_map_layer())
        self.add_layer(self.get_loot_map_layer())
        self.generate_maze()

    def generate_maze(self, seed=None):
        self.maze.generate(seed)
        wall_map_layer = self.get_single_layer_for_role("wall")
        for x, y in self.maze.get_walls():
            wall_map_layer.add_sprite(x, y)
        loot_map_layer = self.get_single_layer_for_role("loot")
        for x, y in random.sample(self.possible_loot_locations(), self.num_loot):
            loot_map_layer.add_sprite(x, y)

    def get_wall_map_layer(self):
        return GridMapLayer(
            name="maze",
            columns=self.columns,
            rows=self.rows,
            pixel_width=self.columns * self.tile_size,
            pixel_height=self.rows * self.tile_size,
            roles=["wall", "display"]
        )

    def get_loot_map_layer(self):
        return GridMapLayer(
            name="loot",
            columns=self.columns,
            rows=self.rows,
            pixel_width=self.columns * self.tile_size,
            pixel_height=self.rows * self.tile_size,
            sprite_filename="images/star.png",
            roles=["loot", "display"]
        )

    def possible_loot_locations(self):
        X = range(1, self.columns, 2)
        Y = range(1, self.rows, 2)
        return list(product(X, Y))


class MazeGame(QuestGame):
    """A sample game in which a player explores a maze and looks for loot.

    MazeGame is an example of how you can make a fairly complex game without 
    making too many changes to QuestGame. The main changes we need to make are 
    how the 

    Because MazeGame is a subclass of QuestGame, we just need to change the 
    parts we want to work differently.
        

    Attributes:
        tile_size=32: Each square tile in the map is 32 pixels across.
        grid_columns=33: The map will have 33 columns of tiles.
        grid_rows=33: The map will have 33 rows of tiles.
        player_sprite_image="images/boy_simple.png": The sprite's image file.
        player_scaling=0.5: The image is too big, so we scale it down. (We could
            also just resize the image itself.)
        player_initial_x=1.5 * tile_size: By starting the player at 1.5 times `tile_size`, 
            the player will initially be positioned at the center of tile (1, 1).
            The outer edge of the map is walls.
        player_initial_y=1.5 * tile_size: Again, centering the player at (1, 1)
        score=0: Keeps track of how much loot has been collected.
        max_score=25: Total amount of loot to be distributed through the maze.
        game_over=False: Keeps track of whether the game has ended.
    """
    tile_size = 32
    grid_columns = 33
    grid_rows = 33
    player_sprite_image = "images/boy_simple.png"
    player_scaling = 0.5
    player_movement_speed = 5
    player_initial_x = 1.5 * tile_size
    player_initial_y = 1.5 * tile_size
    score = 0
    max_score = 25
    game_over = False

    def __init__(self):
        super().__init__()
        self.level_start = datetime.now()

    def setup_maps(self):
        """Sets up the MazeMap and adds it to game's list of maps.
        """
        super().setup_maps()
        maze_map = MazeMap(self.grid_columns, self.grid_rows, self.tile_size, self.max_score)
        self.add_map(maze_map)

    def on_loot_collected(self, loot):
        """Called whenever loot is collected.

        Calls the superclass method (which kills the loot), increments the score, 
        and checks whether the game is over.
        """
        super().on_loot_collected(loot)
        self.score += 1
        if self.score == self.max_score:
            self.game_over = True
            self.final_elapsed_time = (datetime.now() - self.level_start).seconds

    def message(self):
        """Returns a string showing the score and total loot, like "Score: 12/25."
        """
        if self.game_over:
            return "You won in {} seconds!".format(self.final_elapsed_time)
        else:
            elapsed_time = datetime.now() - self.level_start
            return "Time: {}. Score: {}/{}".format(elapsed_time.seconds, self.score, self.max_score)

if __name__ == '__main__':
    game = MazeGame()
    game.run()