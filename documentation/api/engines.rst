Engines
=======

During :py:meth:`quest.game.QuestGame.on_update`, a Physics Engine is used to 
update all the sprites' positions. Generally, a physics engine implements a
set of rules for movement. 

The :doc:`Arcade Library <arcade:index>` provides a number of physics engines 
such as :py:class:`arcade:arcade.PhysicsEngineSimple` (which keeps the player from 
bumping into walls) and :py:class:`arcade:arcade.PhysicsEnginePlatformer` (which
implements gravity, allows the player to jump, and lets the player rest on 
platforms, like in Mario.)

Generally, the :py:class:`arcade:arcade.PhysicsEngineSimple` is perfect for games in Quest 
but sometimes you want something even simpler. The 
:py:class:`quest.engine.NullPhysicsEngine` is perfect in this situation.

.. automodule:: quest.engines
   :members:
   :undoc-members:
