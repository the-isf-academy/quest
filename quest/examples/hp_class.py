from quest.game import QuestGame
from quest.map import Map, GridMapLayer, TiledMap
from quest.sprite import Background, Wall
from quest.engines import DiscretePhysicsEngine
import os
from pathlib import Path
from quest.sprite import Player
from quest.sprite import NPC


def resolve_path(relative_path):
    """A helper function to find images and other resources.
    """
    here = Path(os.path.abspath(__file__)).parent
    return str(here / relative_path)

class hpclass():
insert _init_function here idk how to do it

    def __init__(self): something like this i guess
