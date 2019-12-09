from quest.game import QuestGame
from quest.map import TiledMap
import arcade

class IslandAdventure(QuestGame):

    player_sprite_image = "images/boy_simple.png"
    screen_width = 500
    screen_height = 500
    left_viewport_margin = 64                                                                        
    right_viewport_margin = 64                                                                       
    bottom_viewport_margin = 64                                                                      
    top_viewport_margin = 64 
    player_initial_x = 300
    player_initial_y = 300

    def setup_maps(self):
        super().setup_maps()
        layer_roles = {
            "Water": ["wall", "display"],
            "Deep Water": ["display"],
            "Grass": ["display"]
        }
        self.maps.append(TiledMap("images/island.tmx", layer_roles))

game = IslandAdventure()
game.setup()
arcade.run()
