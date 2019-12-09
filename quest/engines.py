
import arcade

class NullPhysicsEngine:
    def __init__(self, player_sprite):
        self.player_sprite = player_sprite

    def update(self):
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y
