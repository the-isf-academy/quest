Intallation
===========

Quest will be distributed on PyPI, so that you can install it with pip. But for now, you have to install it manually. As usual, a virtual env is recommended but not required.
::

    $ python3 -m venv env
    $ source env/bin/activate
    $ git clone https://github.com/cproctor/quest.git
    $ cd quest
    $ pip install -r requirements.txt
    $ pip install -e .
    $ cd quest/examples
    $ python maze_demo.py
   
