from quest.game import QuestGame
from quest.map import TiledMap
import arcade

class IslandAdventure(QuestGame):

    player_sprite_image = "images/boy_simple.png"
    screen_width = 500
    screen_height = 500
    left_viewport_margin = 96                            
    right_viewport_margin = 96
    bottom_viewport_margin = 96
    top_viewport_margin = 96
    player_initial_x = 300
    player_initial_y = 300
    player_movement_speed = 6

    def setup_maps(self):
        super().setup_maps()
        layer_roles = {
            "Obstacles": ["wall", "display"],
            "Background": ["display"],
        }
        self.add_map(TiledMap("images/island/island.tmx", layer_roles))

if __name__ == '__main__':
    game = IslandAdventure()
    game.run()
