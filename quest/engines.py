# TODO:
# - Decide protocol for collisions (maybe just callbacks?) and implement
# - call sprite.on_collision(collided); the sprite can figure out what it is
# - player max tile off by one
# and deal with it. This means we need Wall sprites, NPC sprites, and a Player sprite.

import arcade
from arcade.sprite_list import SpriteList
from itertools import chain
from collections import defaultdict
from easing_functions import LinearInOut
from quest.helpers import Direction, SpriteListList
from time import time
from math import sqrt

class NullPhysicsEngine:
    """A physics engine which just updates the player's position.
    """
    def __init__(self, player_sprite):
        self.player_sprite = player_sprite

    def update(self):
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y
        return arcade.SpriteList()

class QuestPhysicsEngine:
    """Currently does not handle NPCs.
    """
    def __init__(self, player_list, wall_list=None, npc_list=None):
        self.player_list=player_list
        self.wall_list=wall_list
        self.npc_list=npc_list

    def update(self):
        collisions = {}
        return collisions

class ContinuousPhysicsEngine(QuestPhysicsEngine):
    """Currently does not handle NPCs.
    """
    def __init__(self, player_list, wall_list=None, npc_list=None):
        super().__init__(player_list, wall_list, npc_list)
        self.internal_engine = PhysicsEngineSimple(
            player=self.player(),
            walls=self.wall_list
        )

    def update(self):
        wall_colisions = self.internal_engine.update()
        return [(self.player(), wall) for wall in wall_collisions]

    def player(self):
        return self.player_list.sprite_list[0]

class DiscretePhysicsEngine(QuestPhysicsEngine):
    """A physics engine which snaps sprite movement to specific gridpoints.

    Some games work better when sprites occupy specific tiles, rather than 
    having continuous positions. This can make it easier to think about 
    relationships between sprites (for example, to calculate which are 
    adjacent, or to plan a route). :py:class:`DiscretePhysicsEngine` handles
    sprite movement in a discrete way, while animating sprites' transitions
    from tile to tile.

    Args:
        player_sprite (arcade.Sprite):
        dynamic_sprite_lists (bool): Whether new sprites might be added
            to sprite lists during the game. Performance is better when 
            False. Default True.

    Attributes:
        tile_transition_cutoff (float): Parametric t value at which a sprite's
            current tile should shift to the 
        
    """
    
    tile_transition_cutoff = 0.5
    default_easing_class = LinearInOut
    
    def __init__(self, player_list, grid_map_layer, walls=None, npcs=None, 
            diagonal=True, easing_class=None, check_for_new_sprites=True):
        self.player_list = player_list
        self.grid = grid_map_layer
        self.walls = walls or SpriteList()
        self.npcs = npcs or SpriteList()
        self.diagonal = diagonal
        self.easing = (easing_class or self.default_easing_class)()
        self.check_for_new_sprites = check_for_new_sprites
        self.wall_tiles = defaultdict(list)
        for wall in self.walls:
            tile = self.grid.get_tile_position((wall.center_x, wall.center_y))
            self.wall_tiles[tile].append(wall)
        sprite_lists = [self.player_list, self.walls, self.npcs]
        self.dynamic_sprites = SpriteListList([l for l in sprite_lists if not l.is_static])
        self.ensure_sprite_metadata()
        
    def update(self):
        if self.check_for_new_sprites:
            self.ensure_sprite_metadata()
        for sprite in self.dynamic_sprites:
            if (sprite.change_x or sprite.change_y) and not sprite.moving:
                self.begin_move(sprite)
            elif sprite.moving:
                self.continue_move(sprite)
        return [] # TEMP... expects collision list
        # No, here we need a defaultdict(list) of sprites by their current_positions. 
        # Use that for collision logic
                
    def begin_move(self, sprite):
        direction = Direction.from_vector((sprite.change_x, sprite.change_y), self.diagonal)
        destination = self.tile_in_direction(sprite.origin_tile, direction) 
        if self.grid.tile_in_grid(destination):
            if destination in self.wall_tiles:
                pass # Callback
            else:
                sprite.moving = True
                sprite.move_start = time()
                sprite.t = 0
                sprite.move_direction = direction
                sprite.destination_tile = destination

    def continue_move(self, sprite):
        duration = 1 / sprite.speed
        if sprite.move_direction.is_diagonal():
            duration *= sqrt(2)
        sprite.t = self.ease((time() - sprite.move_start) / duration)
        if sprite.t >= self.tile_transition_cutoff:
            sprite.current_tile = sprite.destination_tile
        if sprite.t >= 1.0:
            self.end_move(sprite)
        else:
            p0 = self.grid.get_pixel_position(sprite.origin_tile)
            p1 = self.grid.get_pixel_position(sprite.destination_tile)
            sprite.center_x, sprite.center_y = self.interpolate(p0, p1, sprite.t)

    def end_move(self, sprite):
        sprite.moving = False
        sprite.center_x, sprite.center_y = self.grid.get_pixel_position(sprite.destination_tile)
        sprite.origin_tile = sprite.current_tile = sprite.destination_tile

    def tile_in_direction(self, tile, direction):
        """Returns the next tile in a diven direction
        """
        tx, ty = tile
        if direction & Direction.RIGHT:
            tx += 1
        if direction & Direction.UP:
            ty += 1
        if direction & Direction.LEFT:
            tx -= 1
        if direction & Direction.DOWN:
            ty -= 1
        return tx, ty

    def interpolate(self, p0, p1, t):
        (x0, y0), (x1, y1) = p0, p1
        return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t

    def ease(self, x):
        return self.easing.ease(x)

    def ensure_sprite_metadata(self):
        for sprite in self.dynamic_sprites:
            if not hasattr(sprite, 'current_tile'):
                sprite.origin_tile = self.grid.get_tile_position((sprite.center_x, sprite.center_y))
                sprite.current_tile = sprite.origin_tile
                sprite.destination_tile = None
                sprite.move_start = None
                sprite.moving = False
                sprite.t = None
