from arcade.sprite import Sprite
from arcade import calculate_points
from quest.helpers import normalize

class QuestSprite(Sprite):
    """Quest base class.
    """
    description = "quest sprite"
    strategy = None
    speed = 1

    def set_course(self, vector):
        vx, vy = normalize(vector)
        self.change_x = vx * self.speed
        self.change_y = vy * self.speed

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def on_collision(self, other_sprite, game):
        pass

    def on_update(self, game):
        if self.strategy:
            self.set_course(self.strategy.choose_course(self, game))

    def __str__(self):
        return "<{}>".format(self.description)


class Wall(QuestSprite):
    """Wall.
    """
    description = "wall"

class Player(QuestSprite):
    """Player
    """
    description = "player"

class NPC(QuestSprite):
    """Non-playable character
    """
    description = "npc"

class Background(QuestSprite):
    """A sprite that does nothing.
    """
    description = "background"
