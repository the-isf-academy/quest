from PIL import Image
import xml.etree.ElementTree as ET
from itertools import product, chain
from pathlib import Path
from enum import Flag, auto

class Direction(Flag):
    NONE = 0
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    UPRIGHT = UP | RIGHT
    UPLEFT = UP | LEFT
    DOWNLEFT = DOWN | LEFT
    DOWNRIGHT = DOWN | RIGHT

    E = RIGHT
    N = UP
    S = DOWN
    W = LEFT
    NE = N | E
    NW = N | W
    SW = S | W
    SE = S | E

    PRIMARY_AXIS = LEFT | RIGHT

    @classmethod
    def from_vector(cls, vector, diagonal=True):
        """Assuming origin at bottom left
        """
        vx, vy = vector
        result = cls.NONE
        if vx < 0: 
            result |= cls.LEFT
        if vx > 0: 
            result |= cls.RIGHT
        if vy < 0:
            result |= cls.DOWN
        if vy > 0:
            result |= cls.UP
        if result.is_diagonal() and not diagonal:
            result &= cls.PRIMARY_AXIS
        return result

    def is_diagonal(self):
        return self in [self.NE, self.NW, self.SW, self.SE]

class SpriteListList:
    """Allows multiple SpriteLists to be treated as if they were a single SpriteList.
    """
    def __init__(self, sprite_lists):
        self.sprite_lists = sprite_lists

    def chain_sprite_lists(self):
        return chain.from_iterable(self.sprite_lists)

    def __iter__(self):
        return iter(self.chain_sprite_lists())

    def update(self):
        for sprite_list in self.chain_sprite_lists():
            sprite_list.update()

def tileset_to_collection(image_path, tile_size, output_dir, name="tileset", create_tsx=True):
    """Splits a tileset image into separate files.

    Quest relies on Arcade, which only works with collections of images. 
    A lot of game art is provided as a single tile image. This function can help split
    it out.

    Args:
        image_path: Path to an image containing a grid of tiles.
        tile_size: Size in pixels of each tile.
        output_dir: Directory for output files (there may be a lot of them).
        name: Name of the tileset.
        create_tsx: If True, also creates a tsx file which can be opened as a
            :doc:`Tileset <tiled:manual/editing-tilesets>` using 
            :doc:`Tiled <tiled:manual/introduction>`.

    """
    img = Image.open(image_path)
    width, height = img.size
    cols, rows = width // tile_size, height // tile_size
    for i, j in product(range(cols), range(rows)):
        left = i * tile_size
        upper = j * tile_size
        right = left + tile_size
        lower = upper + tile_size
        tile = img.crop((left, upper, right, lower))
        output_path = Path(output_dir) / "img_{}_{}.png".format(j, i)
        tile.save(output_path)

    if create_tsx:
        tileset = empty_tileset(tile_size, cols, rows, name)
        for ix, (j, i) in enumerate(product(range(rows), range(cols))):
            add_tile(tileset, ix, "img_{}_{}.png".format(j, i))
        with open(Path(output_dir) / "{}.tsx".format(name), 'wb') as f:
            ET.ElementTree(tileset).write(f, encoding="UTF-8", xml_declaration=True)

def empty_tileset(tile_size, cols, rows, name):
    tileset = ET.Element("tileset")
    tileset.set('version', "1.2")
    tileset.set('tiledversion',"1.3.1")
    tileset.set('name', name)
    tileset.set('tilewidth', str(cols))
    tileset.set('tileheight', str(rows))
    tileset.set('tilecount', str(cols * rows))
    tileset.set('columns', "0")
    grid = ET.SubElement(tileset, "grid")
    grid.set('orientation', "orthagonal")
    grid.set('width', "1")
    grid.set('height', "1")
    return tileset

def add_tile(tileset, tile_id, img_path):
    tile_element = ET.SubElement(tileset, 'tile')
    tile_element.set('id', str(tile_id) )
    img_element = ET.SubElement(tile_element, 'image')
    img_element.set('width', tileset.get('tilewidth'))
    img_element.set('height', tileset.get('tileheight'))
    img_element.set('source', img_path)
