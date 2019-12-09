from quest.game import QuestGame
from quest.map import Map, GridMapLayer
from quest.maze import Maze
import arcade
import random

SPRITE_SIZE = 32
GRID_COLUMNS = 33
GRID_ROWS = 33

class MazeGame(QuestGame):
    player_sprite_image = "images/boy_simple.png"
    player_scaling = 0.5
    player_movement_speed = 5
    player_initial_x = 1.5 * SPRITE_SIZE
    player_initial_y = 1.5 * SPRITE_SIZE
    score = 0
    max_score = 25

    def setup_maps(self):
        super().setup_maps()

        maze = Maze(GRID_COLUMNS, GRID_ROWS)
        maze.generate()
        walls = GridMapLayer(
            name="maze",
            columns=GRID_COLUMNS,
            rows=GRID_ROWS,
            pixel_width=GRID_COLUMNS * SPRITE_SIZE,
            pixel_height=GRID_ROWS * SPRITE_SIZE,
            roles=["wall", "display"]
        )
        for x, y in maze.get_walls():
            walls.add_sprite(x, y)

        loot = GridMapLayer(
            name="loot",
            columns=GRID_COLUMNS,
            rows=GRID_ROWS,
            pixel_width=GRID_COLUMNS * SPRITE_SIZE,
            pixel_height=GRID_ROWS * SPRITE_SIZE,
            sprite_filename="images/star.png",
            roles=["loot", "display"]
        )
        for x, y in random.sample(self.possible_loot_locations(), self.max_score):
            loot.add_sprite(x, y)

        maze_map = Map()
        maze_map.background_color = (20,80,20)
        maze_map.add_layer(walls)
        maze_map.add_layer(loot)
        self.add_map(maze_map)

    def possible_loot_locations(self):
        return [(i, j) for i in range(1, GRID_COLUMNS, 2) for j in range(1, GRID_ROWS, 2)]

    def on_loot_collected(self, loot):
        super().on_loot_collected(loot)
        self.score += 1

    def message(self):
        return "Score: {}/{}".format(self.score, self.max_score)

if __name__ == '__main__':
    game = MazeGame()
    game.setup()
    arcade.run()
