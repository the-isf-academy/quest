# Modal
# -------------------
# A modal window is a "pop-up" that creates a mode--it pauses the game until the 
# window

import arcade
from quest.text_label import TextLabelStack

class Modal:
    """ A modal window is a pop-up that pauses the game until it is resolved.
    It is called a Modal because it puts the game into a new mode. 

    Arguments: 
        game: The game which the Modal is part of.
    """
    width = 400
    height = 400
    line_height = 20
    background_color = arcade.color.LIGHT_GRAY
    active = True

    def __init__(self, game):
        self.game = game
        self.x_center = 0
        self.y_center = 0
        self.current_option = 0
        self.set_text_labels()
        self.set_option_labels()

    def update_position(self, x, y):
        self.x_center = x
        self.y_center = y
        self.set_text_labels()
        self.set_option_labels()

    def text_label_contents(self):
        "Returns a list of strings to be presented as text labels."

        return ["Sorry to bother you with this modal.", "But it's important."]

    def option_label_contents(self):
        "Returns a list of strings to be presented as option labels."
        
        return ["OK", "Fine"]

    def set_text_labels(self):
        """Creates text labels.
        """
        self.text_labels = TextLabelStack(
            self.text_label_contents(),
            self.x_center,
            self.y_center + self.height / 2
        )

    def set_option_labels(self):
        """Creates option labels. 
        """
        options = self.option_label_contents()
        disposable_stack = TextLabelStack(options, 0, 0)
        self.option_labels = TextLabelStack(
            options,
            self.x_center,
            self.y_center - self.height / 2 + disposable_stack.height()
        )
        self.current_option = 0
        self.option_labels.set_highlight(self.current_option)

    def choose_option(self, value):
        """When a button is clicked, it calls choose_option with its value.
        """
        self.game.close_modal()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.handle_change_option(-1)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.handle_change_option(1)
        elif key == arcade.key.ENTER:
            self.handle_choice()

    def handle_change_option(self, change):
        self.current_option = (self.current_option + change) % len(self.option_labels)
        self.option_labels.set_highlight(self.current_option)
    
    def handle_choice(self):
        self.choose_option(self.current_option)
        self.set_text_labels()
        self.set_option_labels()

    def on_draw(self):
        arcade.draw_rectangle_filled(
            self.x_center, 
            self.y_center, 
            self.width, 
            self.height, 
            self.background_color
        )
        self.text_labels.draw()
        self.option_labels.draw()

class DialogueModal(Modal):
    """A modal window powered by a Dialogue object.
    """
    def __init__(self, game, dialogue):
        self.dialogue = dialogue
        super().__init__(game)

    def text_label_contents(self):
        return self.dialogue.get_content()

    def option_label_contents(self):
        return self.dialogue.get_options()

    def choose_option(self, value):
        print("Choosing {}".format(value))
        self.dialogue.choose(value)
        if not self.dialogue.running:
            self.game.close_modal()

class AlertModal(Modal):
    "A simple modal, just used to return a result."
    def __init__(self, game, message, response="OK"):
        self.message = message
        self.response = response
        super().__init__(game)

    def text_label_contents(self):
        return [self.message]

    def option_label_contents(self):
        return [self.response]

    def handle_choice(self):
        self.choose_option(self.current_option)
        self.game.close_modal()

    def choose_option(self, value):
        self.active = False
