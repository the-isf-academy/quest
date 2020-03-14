from quest.game import QuestGame
from quest.map import Map, GridMapLayer, TiledMap
from quest.engines import DiscretePhysicsEngine
from quest.sprite import Player, Wall, Background
import os
from pathlib import Path

class DebugPlayer(Player):
    def on_collision(self, sprite):
        print("Collided with {}".format(sprite))

def resolve_path(relative_path):
    here = Path(os.path.abspath(__file__)).parent
    return str(here / relative_path)

class IslandDiscrete(QuestGame):
    player_sprite_image = resolve_path("images/boy_simple.png")
    player_initial_x = 300
    player_initial_y = 300
    player_class = DebugPlayer
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
        layer = GridMapLayer("grid", 40, 40, 40*32, 40*32)
        self.get_current_map().add_layer(layer)

    def setup_walls(self):
        self.wall_list = self.get_current_map().get_layer_by_name("Obstacles").sprite_list

    def setup_physics_engine(self):
        grid = self.get_current_map().get_layer_by_name('grid')
        self.physics_engine = DiscretePhysicsEngine(self, grid)
        
if __name__ == '__main__':
    game = IslandDiscrete()
    game.run()

