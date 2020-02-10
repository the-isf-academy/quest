
import arcade

class NullPhysicsEngine:
    """A physics engine which just updates the player's position.
    """
    def __init__(self, player_sprite):
        self.player_sprite = player_sprite

    def update(self):
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y
        return arcade.SpriteList()
