def chase_function():

    sprite.center_x = Xn
    sprite.center_y = Yn

    Game.player.center_x = Xp
    Game.player.center_y = Yp

    X_int = abs(self,npc,Xp-Yn)
    Y_int = Abs (Yp-Yn)

    If Xn<Xp
    	Return choose_course(Xn + X_int)

    If Xn>Xp
    	Return choose_course (Xn - X_int)

    If Yn<Yp
    	Return choose_course (Yn + Y_int)

    If Yn> Yp
    	Return choose_course (Yn - Y_int)

    #Movement for NPC

    Class Chase(strategy)

    def choose_course(self, sprite, game):
            """Possibly chooses a new random direction, then returns the current direction.

            Arguments:
                sprite: The sprite who is about to act.
                game: The game object (to access attributes useful in choosing the course).
            """
            if random() < self.change_prob:
                self.set_random_direction()

    	If Xn<Xp
     return (X_int, self.y)

    	If Xn>Xp
     return (-X_int, self.y)

    	If Yn<Yp
     return (self.x, Y_int)

    	If Yn<Yp
     return (self.x, -Y_int)
