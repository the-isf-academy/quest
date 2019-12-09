# Map
# Roles: "wall", "display", "responsive"

import arcade
from quest.errors import NoLayerError, MultipleLayersError

RED = 0
GREEN = 0
BLUE = 0

class Map:
    """
    Represents a map with multiple layers, where each layer has multiple sprites
    performing certain roles. Maps and Map layers are meant to represent stationary
    sprites in the game.
    """
    background_color = (RED, GREEN, BLUE)
    tile_scaling = 1

    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        for existing_layer in self.layers:
            if existing_layer.name == layer.name:
                raise ValueError("Map already has a layer named {}".format(layer.name))
        self.layers.append(layer)

    def get_layer_by_name(self, layer_name):
        layers = [layer for layer in self.layers if layer.name == layer_name]
        if len(layers) == 0:
            raise NoLayerError("Map has no layer named {}".format(layer_name))
        elif len(layers) > 1: 
            raise MultipleLayersError("Map has more than one layer named {}".format(layer_name))
        else:
            return layers[0]

    def get_layers_for_role(self, role):
        return [layer for layer in self.layers if role in layer.roles]

    def get_single_layer_for_role(self, role):
        layers = self.get_layers_for_role(role)
        if len(layers) == 0:
            raise NoLayerError("Map has no layer for role {}".format(role))
        elif len(layers) > 1: 
            raise MultipleLayersError("Map has more than one layer with role {}".format(role))
        else:
            return layers[0]

class TiledMap(Map):
    """
    A Map which is initialized with a .tmx file. Use TiledMap when you want to design your map using
    [Tiled](https://www.mapeditor.org/). 
    """
    def __init__(self, filename, layer_roles):
        super().__init__()
        tilemap = arcade.tilemap.read_tmx(filename)
        for layer_name, roles in layer_roles.items():
            sprite_list = arcade.tilemap.process_layer(tilemap, layer_name, self.tile_scaling)
            layer = MapLayer(layer_name, sprite_list, roles)
            self.add_layer(layer)

class MapLayer:
    """
    Each Map is made up of one or more MapLayers. Each MapLayer contains sprites assigned to particular
    roles in the game. (The game defines the meaning of roles, but several are built-in:
    layers with the "display" role will be shown and sprites in layers with the "wall" role will prevent 
    the player from walking into them.
    """
    def __init__(self, name, sprite_list=None, roles=None):
        self.name = name
        self.sprite_list = sprite_list or arcade.SpriteList()
        self.roles = roles or []

    def draw(self):
        self.sprite_list.draw()

class GridMapLayer(MapLayer):
    """
    A MapLayer designed for use with GridMap. Makes it easy to add new sprites at particular grid locations.
    """
    sprite_filename = "images/box.png"

    def __init__(self, name, columns, rows, pixel_width, pixel_height, sprite_filename=None, roles=None):
        super().__init__(name, roles=roles)
        self.columns = columns
        self.rows = rows
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.sprite_filename = sprite_filename or self.sprite_filename

    def add_sprite(self, x, y, sprite=None):
        sprite = sprite or self.create_sprite()
        sprite.left, sprite.bottom = self.get_pixel_position(x, y)
        self.sprite_list.append(sprite)

    def create_sprite(self):
        return arcade.Sprite(self.sprite_filename)

    def get_pixel_position(self, x, y):
        if x < 0 or x >= self.columns:
            raise ValueError("Invalid x value of {} on layer with {} columns".format(x, self.columns))
        if y < 0 or y >= self.rows:
            raise ValueError("Invalid y value of {} on layer with {} rows".format(y, self.rows))
        left = self.pixel_width * (x / self.columns)
        bottom = self.pixel_height * (y / self.rows)
        return (left, bottom)

