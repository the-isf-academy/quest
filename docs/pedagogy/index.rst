Pedagogy
========

Goals
-----

Skills
++++++

- Object-oriented programming
  - classes
  - inheritance
- Tick-based time system
- Introductory algorithms
  - terrain/maze generation
  - NPC behavior
- Using logging for evaluation

Practices
+++++++++

- Collaboration (students will work in groups to create a game)
- Planning (especially considering alternative possible implementations)
- Reading documentation
- Reading source code; navigating multiple-file projects
- Subclassing to change behavior of exisiting system

Possible Activities
-------------------

- Have students trace inheritance chain of classes, list method instances.
- Have students trace call execution through class methods
- Have students implement subclasses using method hooks
- Observe default behavior of existing framework and tracing the codebase to find where 
- Make trivial changes via subclassing. Each can be achieved by adding a single property.
  - change the player sprite filename
  - scale the player sprite to be larger or smaller. 
  - change the player speed
- Make small changes by overriding methods (with low task complexity)
  - change the input keys 
  - add a "run" mode: the character goes faster while spacebar is pressed
  - load a different map (eg load a Maze map but change the number of stars)
- Plan possible implementation strategies
  - Give students a list of possible game mechanics (eg an enemy chases you; add an inventory; moving between maps; a way to win the game; a key unlocks a door) and have them write a plan of what could be overridden/extended to make it happen. 
- As groups start developing games, brainstorm needed features as a class, and collaborate on implementing them. (This will reward good design, as we want an inventory system or an enemy behavior system that can work for everyone.)

