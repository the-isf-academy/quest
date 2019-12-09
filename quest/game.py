# QuestGame

import arcade
from quest.engines import NullPhysicsEngine
from quest.errors import NoMapError, NoLayerError

class QuestGame(arcade.Window):
    """
    QuestGame is a subclass of arcade.Window.
    """
    screen_width = 600
    screen_height = 600
    left_viewport_margin = 100
    right_viewport_margin = 100
    bottom_viewport_margin = 100
    top_viewport_margin = 100
    screen_title = "Quest"
    player_scaling = 1
    player_sprite_image = None
    player_movement_speed = 10
    player_initial_x = 0
    player_initial_y = 0

    def __init__(self):
        super().__init__(self.screen_width, self.screen_height, self.screen_title)
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.setup_player()
        self.setup_maps()
        if len(self.maps) > 0:
            self.set_current_map(0)
        self.setup_non_playable_characters()
        self.setup_physics_engine()
        self.center_view_on_player()

    def setup_player(self):
        self.player_sprite = arcade.Sprite(self.player_sprite_image, self.player_scaling)
        self.set_player_initial_position()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

    def set_player_initial_position(self):
        self.player_sprite.center_x = self.player_initial_x
        self.player_sprite.center_y = self.player_initial_y

    def setup_maps(self):
        self.maps = []

    def add_map(self, game_map):
        self.maps.append(game_map)

    def get_current_map(self):
        if self.current_map_index is None:
            raise NoMapError("The game has no maps")
        return self.maps[self.current_map_index]

    def set_current_map(self, index):
        if index < 0 or index >= len(self.maps):
            raise ValueError("Cannot set current map to {}; there are {} maps.".format(
                    index, len(self.maps)))
        self.current_map_index = index

    def setup_non_playable_characters(self):
        self.non_playable_characters = arcade.SpriteList()

    def setup_physics_engine(self):
        try:
            walls = self.get_current_map().get_single_layer_for_role("wall").sprite_list
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls)
        except (NoMapError, NoLayerError):
            self.physics_engine = NullPhysicsEngine(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(self.get_current_map().background_color)
        for layer in self.get_current_map().get_layers_for_role("display"):
            layer.draw()
        self.player_list.draw()
        message = self.message()
        if message:
            arcade.draw_text(message, 10 + self.view_left, 10 + self.view_bottom,
                    arcade.csscolor.WHITE, 18)

    def on_update(self, delta_time):
        self.physics_engine.update()
        for layer in self.get_current_map().get_layers_for_role("loot"):
            for loot in arcade.check_for_collision_with_list(self.player_sprite, layer.sprite_list):
                self.on_loot_collected(loot)
        self.scroll_viewport()

    def on_loot_collected(self, loot):
        loot.kill()

    def on_key_press(self, key, modifiers):
        """
        While a key is pressed, the sprite's x- and y- change values are set
        to the player's movement speed. Think of this as a request to move--
        it's up to the physics engine to decide whether this actually 
        results in movement. For example, the physics engine will prevent 
        players from moving into walls.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = self.player_movement_speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -self.player_movement_speed
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -self.player_movement_speed 
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = self.player_movement_speed 

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_view_on_player(self):
        self.view_left = self.player_sprite.center_x - self.screen_width / 2
        self.view_bottom = self.player_sprite.center_y - self.screen_height / 2
        self.update_viewport()
        self.scroll_viewport()

    def scroll_viewport(self):
        changed = False

        left_boundary = self.view_left + self.left_viewport_margin
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + self.screen_width - self.right_viewport_margin
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + self.screen_height - self.top_viewport_margin
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + self.bottom_viewport_margin
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            self.update_viewport()

    def update_viewport(self):
        arcade.set_viewport(
            self.view_left,
            self.screen_width + self.view_left,
            self.view_bottom,
            self.screen_height + self.view_bottom
        )

    def message(self):
        return None
        
        
