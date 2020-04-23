from arcade.sprite import Sprite
from arcade import calculate_points
from quest.helpers import scale
from quest.sprite import QuestSprite
from quest.game import QuestGame
from quest.examples.island import IslandAdventure
import arcade
import os

SPRITE_SCALING = 0.5

MOVEMENT_SPEED = 5

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP=3
TEXTURE_DOWN=2
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# +
#Code by Paul Vincent Craven


class Sprite_direction(QuestSprite):

    def __init__(self):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture("pirate.30.39 AM.png")
        self.textures.append(texture)
        texture = arcade.load_texture("pirate.30.39 AM.png", mirrored=True)
        self.textures.append(texture)
        texture = arcade.load_texture("piratetop.00.17 PM.png")
        self.textures.append(texture)
        texture = arcade.load_texture("piratetop.00.17 PM.png", mirrored=True)
        self.textures.append(texture)

        self.scale = SPRITE_SCALING
        # By default, face right.
        self.set_texture(TEXTURE_DOWN)

    def on_update(self, game):
        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

        if self.change_y < 0:
            self.texture = self.textures[TEXTURE_DOWN]
        elif self.change_y > 0:
            self.texture = self.textures[TEXTURE_UP]
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class testfeature(IslandAdventure):
        def setup_player(self):
            """Creates the player sprite.

            Initializes a sprite for the player, assigns its starting position,
            and appends the player sprite to a SpriteList (Arcade likes to work
            with sprites in SpriteLists).
            """
            self.player = Sprite_direction()
            self.player.center_x = self.player_initial_x
            self.player.center_y = self.player_initial_y
            self.player.speed = self.player_speed
            self.player_list = arcade.SpriteList()
            self.player_list.append(self.player)

        def on_key_press(self, key, modifiers):
            #Called whenever a key is pressed.
            if key == arcade.key.UP:
                self.player.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player.change_x = MOVEMENT_SPEED

        def on_key_release(self, key, modifiers):
            #Called when the user releases a key.
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player.change_x = 0

        def on_update(self, delta_time):
            """Updates the game's state.

            At every tick, the game needs to be updated. The physics engine
            updates sprite positions, and then sprite callbacks are executed.
            Finally, the viewport is scrolled. Note that `on_update` changes the
            state of the game, but does not draw anything to the screen.

            Args:
                delta_time: How much time has passed since the last update.
            """
            if self.running:
                self.player.on_update(self)
                for npc in self.npc_list:
                    npc.on_update(self)
                self.physics_engine.update()
                self.scroll_viewport()

if __name__ == '__main__':
    game = testfeature()
    game.run()
