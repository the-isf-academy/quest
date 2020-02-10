import arcade
from quest.errors import NoLayerError, MultipleLayersError

RED = 0
GREEN = 0
BLUE = 0

class Map:
    """Implements a map for a level or stage in the game.

    Each QuestGame may have multiple Maps. Each Map represents a game map with 
    multiple layers, allowing the map to describe walls, loot, and multiple layers
    of background imagery.

    Attributes:
        background_color: a 3-tuple of integers for red, green, blue. Each from 0-255.
            The :py:module:`arcade:color` module also predefines many colors.
        tile_scaling: Factor by which to scale all map tiles. Default is 1.
    """
    background_color = (RED, GREEN, BLUE)
    tile_scaling = 1

    def __init__(self):
        """Initialize a Map with an empty layers list.
        """
        self.layers = []

    def add_layer(self, layer):
        """Add a layer the the layers list.

        Checks to make sure the layer's name is unique.

        Args:
            layer: The MapLayer to add.
        """
        for existing_layer in self.layers:
            if existing_layer.name == layer.name:
                raise ValueError("Map already has a layer named {}".format(layer.name))
        self.layers.append(layer)

    def get_layer_by_name(self, layer_name):
        """Looks up a map layer by name. 

        There should only be one layer with each name. If there is not exactly one layer,
        raises an error. 

        Args:
            layer_name: The name of the layer.

        Returns: The layer.
        """
        layers = [layer for layer in self.layers if layer.name == layer_name]
        if len(layers) == 0:
            raise NoLayerError("Map has no layer named {}".format(layer_name))
        elif len(layers) > 1: 
            raise MultipleLayersError("Map has more than one layer named {}".format(layer_name))
        else:
            return layers[0]

    def get_layers_for_role(self, role):
        """Looks up all layers having a particular role.

        Args:
            role: A string naming the role.

        Returns: A list of zero or more MapLayers.
        
        """
        return [layer for layer in self.layers if role in layer.roles]

    def get_single_layer_for_role(self, role):
        """Looks up a single layer having a particular role.

        Returns the one layer having a role. If there is not exactly one layer,
        raises an error.

        Args:
            role: A string naming the role.
            
        Returns: One MapLayer
        """
        layers = self.get_layers_for_role(role)
        if len(layers) == 0:
            raise NoLayerError("Map has no layer for role {}".format(role))
        elif len(layers) > 1: 
            raise MultipleLayersError("Map has more than one layer with role {}".format(role))
        else:
            return layers[0]

class TiledMap(Map):
    """A subclass of Map which loads its layers from a TMX file.

    Use TiledMap when you want to design your map using
    [Tiled](https://www.mapeditor.org/). This app saves maps as TMX files.
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

    def clear(self):
        """Delete all this layer's sprites.
        """
        while len(self.sprite_list) > 0:
            self.sprite_list.pop()

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

