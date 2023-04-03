# Final Project CMSC 14200
Robert Wang (Group Leader), Alex Fan, Ethan Jiang

# Checkers

This repository contains a design and implementation for Checkers.

Before running the game, copy all text from the requirements.txt file and paste
it into the terminal. Press enter.

# Running the GUI

To run the GUI, run the following from the root of the repository:

    python3 src/GUI.py

The GUI displays the state of the board. Normal pieces are represented as 
circles, either white or gray, and kings are represented as circles with 
a black circle in the middle.

Moving pieces occurs in two steps.
1) First, click a piece on the board. Blue dots will show up in the squares 
you can move this piece to.
2) Next, click on one of the blue dots. This will move the piece to the
assigned square.
2a) If nothing happens when you click the blue dot, it is because you 
are making a non-capture move when a capture move is available. Try 
selecting another piece and making a capture move.
3) When the game finishes, return to the terminal to find out who won.

You can play against a bot, or have two bots play
against each other like this:

    python3 src/GUI.py --player2 <bot>

    python3 src/GUI.py --player1 <bot> --player2 <bot>

Replace <bot> with either random-bot or smart-bot.

The ``--bot-delay <seconds>`` parameter is also supported.

THe GUI also supports different board sizes. To customize board size, use:

    python3 src/GUI.py --board-size <n>
    
where the size of the board is (2n+2) x (2n+2).

To see the GUI in its ultimate form, combine these parameters:

    python3 src/GUI.py --player1 "random-bot" --player2 "random-bot" --bot-delay 0.1 --board-size 10

# Bot
The `` bots.py `` file has a single class:
- ``Bot``: Using a given depth, the bot will use the minimax algorithm with alpha-beta pruning to determine a move for its turn and color. Depths of 0 will create a random bot that will choose a move from a given list at random.

# Testing Smart Bot Accuracy

This Class is used in the GUI, but you can also run ``bots.py`` to run a given number of simulated games where two bots can play against each other and see the percentage of wins per bot and ties. For Example:

    $python3 src/bot.py -n 5 --bot1 2 --bot2 0
    Bot1 (Smart, Depth of 2): won 5/5 or 100% of games
    Bot2 (Random): won 0/0 or 0% of games
    Ties: 0.0%
    Average Time Per Game: 1.8834144592285156

You can control the number of games using the ``-n <number of games>`` parameter to bots.
You can expand the size of the board using the ``--play_len <number of playable rows>`` parameter in bots. ``play_len`` is not the board length but the number of playable rows which can be translated to the board side length through 2 * ``play_len`` + 2. 

Please note that bots with a parameter of ``depth`` set to 0 will be random, this was done to allow users to choose the depth of the bots they sought to play against or see play each other. Fastest >50% winrate ``depth`` is been 2.

Please also note that runs on my personal computer finish within 1-2 seconds on average at a ``depth`` of 2, however, could last anywhere from 4-50 seconds per game when run on linux servers. When encountering this issue, the default ``-n <number of games>`` has been set to 100, simply change ``-n`` into a smaller value for quicker, but less representative, win rates.
