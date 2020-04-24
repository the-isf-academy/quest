from quest.examples.island import IslandAdventure

class MouseMotion(IslandAdventure):

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        keep track of the mouse's new coordinates whenever it moves.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """

        if self.player.center_y != y:
            self.player.change_y = dy
        if self.player.center_x != x:
            self.player.change_x = dx

if __name__ == '__main__':
    game = MouseMotion()
    game.run()
