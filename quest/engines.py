import arcade
from arcade.sprite_list import SpriteList
from arcade.physics_engines import PhysicsEngineSimple
from arcade import check_for_collision_with_list
from itertools import chain
from collections import defaultdict
from easing_functions import LinearInOut
from quest.helpers import Direction, SpriteListList
from time import time
from math import sqrt

class QuestPhysicsEngine:
    """Base class for Quest Physics Engines
    """
    def __init__(self, game):
        self.game = game
        self.player_list=game.player_list
        self.wall_list=game.wall_list
        self.npc_list=game.npc_list

    def update(self, game):
        pass

    def player(self):
        return self.player_list.sprite_list[0]

class ContinuousPhysicsEngine(QuestPhysicsEngine):
    """A continuous physics engine allows sprites to be at any point.
    """
    def __init__(self, game):
        super().__init__(game)
        self.internal_engine = PhysicsEngineSimple(self.player(), self.wall_list)

    def update(self):
        wall_collisions = self.internal_engine.update()
        for wall in wall_collisions:
            self.player().on_collision(wall, self.game)
            wall.on_collision(self.player(), self.game)
        npc_collisions = check_for_collision_with_list(self.player(), self.npc_list)
        for npc in npc_collisions:
            self.player().on_collision(npc, self.game)
            npc.on_collision(self.player(), self.game)

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
    easing_class = LinearInOut
    
    def __init__(self, game, grid_map_layer, diagonal=True, check_for_new_sprites=True):
        super().__init__(game)
        self.grid = grid_map_layer
        self.diagonal = diagonal
        self.easing = self.easing_class()
        self.check_for_new_sprites = check_for_new_sprites
        sprite_lists = [self.player_list, self.wall_list, self.npc_list]
        self.all_sprites = SpriteListList(sprite_lists)
        self.dynamic_sprites = SpriteListList([l for l in sprite_lists if not l.is_static])
        self.ensure_sprite_metadata(all_sprites=True)
        self.tile_positions = defaultdict(list)
        for sprite in self.all_sprites:
            self.tile_positions[sprite.current_tile].append(sprite)
        
    def update(self):
        if self.check_for_new_sprites:
            self.ensure_sprite_metadata()
        for sprite in self.dynamic_sprites:
            if (sprite.change_x or sprite.change_y) and not sprite.moving:
                self.begin_move(sprite)
            elif sprite.moving:
                self.continue_move(sprite)
                
    def begin_move(self, sprite):
        direction = Direction.from_vector((sprite.change_x, sprite.change_y), self.diagonal)
        ox, oy = sprite.origin_tile
        vx, vy = direction.to_vector()
        destination = (ox + vx, oy + vy)
        if self.grid.tile_in_grid(destination):
            wall = self.get_wall(self.tile_positions[destination])
            if wall:
                self.player().on_collision(wall, self.game)
                wall.on_collision(self.player(), self.game)
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
            self.tile_positions[sprite.current_tile].remove(sprite)
            sprite.current_tile = sprite.destination_tile
            for other_sprite in self.tile_positions[sprite.current_tile]:
                sprite.on_collision(other_sprite, self.game)
                other_sprite.on_collision(sprite, self.game)
            self.tile_positions[sprite.current_tile].append(sprite)
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

    def get_wall(self, sprite_list):
        for sprite in sprite_list:
            if sprite in self.wall_list:
                return sprite

    def interpolate(self, p0, p1, t):
        (x0, y0), (x1, y1) = p0, p1
        return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t

    def ease(self, x):
        return self.easing.ease(x)

    def ensure_sprite_metadata(self, all_sprites=False):
        sprites = self.all_sprites if all_sprites else self.dynamic_sprites
        for sprite in sprites:
            if not hasattr(sprite, 'current_tile'):
                sprite.origin_tile = self.grid.get_tile_position((sprite.center_x, sprite.center_y))
                sprite.current_tile = sprite.origin_tile
                sprite.destination_tile = None
                sprite.move_start = None
                sprite.moving = False
                sprite.t = None
