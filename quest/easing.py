class Easing:
    """Base class for easing. 

    Easing refers to the rate at which something goes from start to finish. 
    This applies to many processes, like moving from one place to another or 
    fading in or out audio. 

    Linear easing, which goes at the same rate the whole time, can feel like
    it starts and ends abruptly. Other kinds of easing provide a smoother 
    experience. Easing is used by :py:class:`DiscretePhysicsEngine` to determine 
    how sprites should move from one tile to another. 

    The Easing class has a single method, :py:meth:`transform`, which takes a 
    value between 0 and 1 and returns a value between 0 and 1. Easing is implemented
    as a class instead of just a simple function because some forms of easing might 
    need to get configured with parameters. 
    """

    def transform(self, x):
        return x

class EasingLinear(Easing):
    """Linear easing.
    """

class EasingCubic(Easing):
    """Cubic easing. Provides a simple form of easing with a gentle start and finish.     
    """

    def transform(self, x):
        return x ** 3
