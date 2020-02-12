from quest.game import QuestGame
from quest.map import Map, GridMapLayer, TiledMap
from quest.engines import DiscretePhysicsEngine
import os
from pathlib import Path

def resolve_path(relative_path):
    here = Path(os.path.abspath(__file__)).parent
    return str(here / relative_path)

class TinyGridTest(QuestGame):
    player_sprite_image = resolve_path("images/boy_simple.png")
    player_initial_x = 300
    player_initial_y = 300
    player_speed = 10

    def setup_maps(self):
        """Sets up the map.

        Uses a :py:class:`TiledMap` to load the map from a ``.tmx`` file,
        created using :doc:`Tiled <tiled:manual/introduction>`. The layers
        in the map are assigned :doc:`roles <narrative/map>` so that their 
        sprites behave in particular ways.
        """
        super().setup_maps()
        layer_roles = {
            "Obstacles": ["wall", "display"],
            "Background": ["display"],
        }
        self.add_map(TiledMap(resolve_path("images/island/island.tmx"), layer_roles))

        layer = GridMapLayer("grid", 40, 40, 40*32, 40*32)
        self.get_current_map().add_layer(layer)

    def setup_physics_engine(self):
        grid = self.get_current_map().get_layer_by_name('grid')
        self.physics_engine = DiscretePhysicsEngine(self.player_list, grid, 
            walls=self.get_current_map().get_single_layer_for_role('wall').sprite_list)
        
if __name__ == '__main__':
    game = TinyGridTest()
    game.run()

