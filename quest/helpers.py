from PIL import Image
import xml.etree.ElementTree as ET
from itertools import product
from pathlib import Path

def tileset_to_collection(image_path, tile_size, output_dir, name="tileset", create_tsx=True):
    """Splits a tileset image into separate files.

    Quest relies on Arcade, which only works with collections of images. 
    A lot of game art

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
    """Creates an empty tileset.

    Args:
        tile_size: Size of each tile, in pixels.
        cols: Number of columns.
        rows: Number of rows.
        name: Tileset name.

    Returns:
        An xml document set up as a tileset.
    """
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
    """Adds a tile to the tileset.

    Args:
        tileset: An xml document, like the return value of `empty_tileset`.
        tile_id: A unique number.
        img_path: Path to the image, relative to where this tileset will be saved.
    """
    tile_element = ET.SubElement(tileset, 'tile')
    tile_element.set('id', str(tile_id) )
    img_element = ET.SubElement(tile_element, 'image')
    img_element.set('width', tileset.get('tilewidth'))
    img_element.set('height', tileset.get('tileheight'))
    img_element.set('source', img_path)

if __name__ == '__main__':
    tileset_to_collection("examples/images/wood_tileset.png", 32, "examples/images/wood_tileset")
