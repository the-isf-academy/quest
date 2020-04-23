from arcade.sprite import Sprite
from arcade import calculate_points
from quest.helpers import scale
import arcade
import os

SPRITE_SCALING = 0.5

MOVEMENT_SPEED = 5

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_UP=2
TEXTURE_DOWN=3

#Code by Paul Vincent Craven
<<<<<<< HEAD

    class Player(arcade.Sprite):
=======
class Player(arcade.Sprite):
>>>>>>> 6d700578958f5791cafca392757db534068f9468

    def __init__(self):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture(":resources:images/enemies/bee.png")
        self.textures.append(texture)
        texture = arcade.load_texture(":resources:images/enemies/bee.png", mirrored=True)
        self.textures.append(texture)
        texture = arcade.load_texture(":resources:images/enemies/bee.png")
        self.textures.append(texture)
        texture = arcade.load_texture(":resources:images/enemies/bee.png", mirrored=True)
        self.textures.append(texture)

        self.scale = SPRITE_SCALING
        # By default, face right.
        self.set_texture(TEXTURE_DOWN)

        def update(self):
            self.center_x += self.change_x
            self.center_y += self.change_y

            # Figure out if we should face left or right
            if self.change_x < 0:
                self.texture = self.textures[TEXTURE_LEFT]
            elif self.change_x > 0:
                self.texture = self.textures[TEXTURE_RIGHT]

            if self.change_y < 0:
                self.texture = self.textures[TEXTURE_DOWN]
            elif self.change_y > 0:
                self.texture = self.textures[TEXTURE_UP]

            if self.left < 0:
                self.left = 0
            elif self.right > SCREEN_WIDTH - 1:
                self.right = SCREEN_WIDTH - 1

            if self.bottom < 0:
                self.bottom = 0
            elif self.top > SCREEN_HEIGHT - 1:
                self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """
    def __init__(self, width, height, title):

        #Initializer


        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.all_sprites_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        #Set up the game and initialize the variables.

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):

        #Render the screen.


        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.all_sprites_list.draw()

    def on_key_press(self, key, modifiers):
        #Called whenever a key is pressed.

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        #Called when the user releases a key.

<<<<<<< HEAD
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player_sprite.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.change_x = 0

=======
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
>>>>>>> 6d700578958f5791cafca392757db534068f9468


class QuestSprite(Sprite):
    he base class for sprites in Quest.

    A :py:class:`QuestSprite` is a subclass of :py:class:`arcade.Sprite` with a
    few additional methods to help integrate into the Quest framework.

    Attributes:
        description: A string description of the sprite.
        strategy: If set, should be a :py:class:`quest.strategy.Strategy`, or another class
            instance with a :py:meth:`choose_course` method.
        speed: The sprite's speed.

    Arguments:
        filename: The only required argument is the name of the sprite's image file.
        kwargs: There are many optional keyword arguments inherited from :py:class:`arcade.Sprite`.

    description = "quest sprite"
    strategy = None
    speed = 1

    def set_course(self, vector):
        """Update the `change_x` and `change_y` properties using a vector.

        Normally, sprites' intended movement is set using the `change_x` and `change_y`
        properties. This method updates `change_x` and `change_y` based on an (x, y) vector
        whose magnitude is scaled to the sprite's speed. This is helpful when you have an
        (x, y) vector, for example a :py:class:`quest.helpers.Direction` or a vector to another
        sprite, and want to have this sprite head that direction at its speed. For example, if you wanted
        a sprite to always try to move down at its speed::

                def on_update(self):
                    self.set_course(Direction.DOWN.to_vector())

        """
        vx, vy = scale(vector, self.speed)
        self.change_x = vx
        self.change_y = vy

    def stop(self):
        """Set the sprite's `change_x` and `change_y` to zero.
        """
        self.change_x = 0
        self.change_y = 0

    def on_collision(self, other_sprite, game):
        """Called when the sprite collides with another sprite.

        Override this method to change the sprite's collision behavior.
        For example, an NPC sprite which represents an item that can be collected
        by the player would probably call a method on `game` to update the inventory
        and then call :py:meth:`self.kill()`.
        """
        pass

    def on_update(self, game):
        """Called on every tick, performs any needed updates.

        By default, if the sprite has a strategy, it uses the strategy
        to set its course.
        """
        self.all_sprites_list.update()

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

class Boat(Player):
    
