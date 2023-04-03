# this is the minimax
# resources used:
#   - https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
#       - provided pseudocode for the minimax algorithm
import numpy as np
from checkers import *
import random
from copy import deepcopy
import time
import click


class Bot:
    """
    This Class will house all of the methods and information required to
    implement a bot that can play the checkers game from ../src/checkers.py.
    The bot can interact with the game in real time by playing either random
    or algorithmically optimized moves through the minimax algorithm
    """

    def __init__(self, depth, color):
        """
        Constructor
        Attributes:
        depth (int): how many layers of the minimax tree will this bot go
        color(str): either "LIGHT" or "DARK"
        random(bool): if the bot is random or not

        Parameters:
        depth(int): how many layers of minimax the bot will run through, 0 or
        less will be a random bot
        color(str): which side the bot will play on

        Initializes empty bot
        """
        assert color == "LIGHT" or color == "DARK"
        self.depth = depth
        self.color = color
        self.random = False
        if depth <= 0:
            self.random = True

    def minimax(self, game, depth, maxing, alpha, beta):
        """
        This is the algorithm for sorting through possible checkers gamestates
        at a given depth and choosing the optimal move based on a minimax
        algorithm with alpha-beta pruning.
        Inputs:
        - game(Checkers obj): the current boardstate
        - depth(int): the depth to which the algorithm should search possible
        gamestates
        - maxing(bool): which side the player is on, whether the maxing(LIGHT)
        or minimizing(DARK) side
        - alpha(float or int): the alpha used in alpha-beta pruning
        - beta(float or int): the beta used in alpha-beta pruning

        Output:
        - tuple(
            int,
            tuple(tuple(int,int), tuple(int, int, str))
            )
        """
        # base case
        if depth == 0 or game.board.winner is not None:
            return game.calculate_boardstate(), ""
        # white
        if maxing:
            color = "LIGHT"
            max_eval = np.NINF
            best_move = None
            w_all = game.all_moves(color)
            for piece_coord, moves in w_all.items():
                p_x, p_y = piece_coord
                is_king = game.board.board_grid[p_x][p_y].piece.king
                if len(moves) == 0:
                    continue
                for move_coord in moves:
                    if move_coord is None or move_coord == ():
                        continue
                    tmp_board = deepcopy(game)
                    tmp_board.move_piece(
                        piece_coord, move_coord, color, king=is_king
                    )
                    eval, _ = self.minimax(
                        tmp_board, depth - 1, False, alpha, beta
                    )
                    max_eval = max(eval, max_eval)
                    if eval == max_eval:
                        best_move = (piece_coord, move_coord)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        # black
        else:
            color = "DARK"
            min_eval = np.inf
            best_move = None
            b_all = game.all_moves(color)
            for piece_coord, moves in b_all.items():
                p_x, p_y = piece_coord
                is_king = game.board.board_grid[p_x][p_y].piece.king
                if len(moves) == 0:
                    continue
                for move_coord in moves:
                    if move_coord is None or move_coord == ():
                        continue
                    tmp_board = deepcopy(game)
                    tmp_board.move_piece(
                        piece_coord, move_coord, color, king=is_king
                    )
                    eval, _ = self.minimax(
                        tmp_board, depth - 1, True, alpha, beta
                    )
                    min_eval = min(eval, min_eval)
                    if eval == min_eval:
                        best_move = (piece_coord, move_coord)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def random_move(self, game, seed=None):
        """
        finds a random move out of all possible moves in a game

        Input:
        - game(Checkers): current game
        - seed(int): a seed to regularize the bot for testing purposes

        Output:
        - tuple(
            tuple(int,int),
            tuple(int,int,str)
            )
        """
        if seed is not None:
            random.seed(seed)
        poss_moves = game.all_moves(self.color)
        random_idx = random.randint(0, len(poss_moves) - 1)
        random_piece = list(poss_moves.keys())[random_idx]
        random_piece_moves = poss_moves[random_piece]
        random_piece_idx = random.randint(0, len(random_piece_moves) - 1)
        random_move = (random_piece, random_piece_moves[random_piece_idx])
        return random_move

    def get_move(self, new_board_state):
        """
        gets a move recommendation based on board state

        Input:
        - new_board_state(Checkers): the game to get a move from

        Output:
        - tuple(
            tuple(int,int),
            tuple(int,int,str)
            )
        """
        current_board = new_board_state
        if self.random:
            return self.random_move(new_board_state)
        else:
            depth = self.depth
            if self.color == "LIGHT":
                maxing = True
            else:
                maxing = False
            alpha = np.NINF
            beta = np.inf
            _, move = self.minimax(current_board, depth, maxing, alpha, beta)
            return move

    def move(self, new_board_state):
        """
        actively changes the board state on game object in place
        Input:
        - new_board_state(Checkers): the gave to be moved

        Output:
        - Checkers obj: the changed game
        """
        self.game = new_board_state
        if new_board_state.board.winner is not None:
            print("There is a winner")
            return new_board_state
        elif new_board_state.board.turn != self.color:
            print("It is not our turn")
        else:
            piece, move = self.get_move(new_board_state)
            p_x, p_y = piece
            is_king = new_board_state.board.board_grid[p_x][p_y].piece.king
            new_board_state.move_piece(piece, move, self.color, king=is_king)
            return new_board_state

@click.command(name = "checkers-bot")
@click.option ('-n','--num-games', type = click.INT, default = 100)
@click.option('--bot1', type = click.INT, default = 2)
@click.option('--bot2', type = click.INT, default = 0)
@click.option('--play_len', type = click.INT, default = 3)
def bot_v_bot(num_games, bot1 = 2, bot2 = 0, play_len=3):
    """
    Runs a script of n Checkers games of a bot of a given depth against another
    bot of a given depth on a given board size
    Input:
    - n(int): how many iterations or simulation games to be run
    - bot1(int): the depth of first bot
    - bot2(int): the depth of second bot
    - play_len(int): the number of starting rows per player to find the board
        length, given by 2*play_len + 2 (i.e. play_len 3 is a board len of 8)

    Output:
    - tuple(
        float, -> the bot1 win percentage
        float, -> the bot 2 win percentage
        list, -> the list of the results of each game
        float -> the average speed of each gme
        )
    """
    bot1wins = 0
    bot2wins = 0
    win_lst = []
    time_lst = []
    for i in range(num_games):
        start = time.time()
        if i % 2 == 0:
            bot1_col = "LIGHT"
            bot2_col = "DARK"
            win_state = "White Wins"
            loss_state = "Black Wins"
        else:
            bot1_col = "DARK"
            bot2_col = "LIGHT"
            win_state = "Black Wins"
            loss_state = "White Wins"
        game = Checkers(play_len)
        win_bot = Bot(bot1, bot1_col)
        rand_bot = Bot(bot2, bot2_col)
        while game.check_winner() == "No Winner":
            if game.board.turn == bot1_col:
                win_bot.move(game)
            elif game.board.turn == bot2_col:
                rand_bot.move(game)
        end = time.time()
        time_lst.append(end - start)
        if game.check_winner() == win_state:
            bot1wins += 1
            win_lst.append("Bot1")
        elif game.check_winner() == loss_state:
            bot2wins += 1
            win_lst.append("Bot2")
        elif game.check_winner() == "DRAW":
            win_lst.append("Draw")
        else:
            win_lst.append(("something bad happened", game.check_winner()))
    n = num_games
    if bot1 <= 0:
        bot1_int = "Random"
    else:
        bot1_int = f"Smart, Depth of {bot1}"
    if bot2 <= 0:
        bot2_int = "Random"
    else:
        bot2_int = f"Smart, Depth of {bot2}"
    bot1_perc = 100 * bot1wins / n
    bot2_perc = 100 * bot2wins / n
    ties = 100 * (n - bot1wins - bot2wins) / n
    avg_gametime = np.mean(time_lst)
    print(f"Bot1 ({bot1_int}): won {bot1wins}/{n} or {bot1_perc}% of games")
    print(f"Bot2 ({bot2_int}): won {bot2wins}/{n} or {bot2_perc}% of games")
    print(f"Ties: {ties}%")
    print(f"Average Time per Game: {avg_gametime}")
    return bot1_perc, bot2_perc, win_lst, avg_gametime

if __name__ == "__main__":
    bot_v_bot()

def create_test_board(black, white, black_k, white_k):
    """
    creates a test board of side length 8 of a given positions on the board,
    for testing purposes only

    Input:
    - black(list(tuples(int,int))): list of black nonking piece coordinates
    - white(list(tuples(int,int))): list of white nonking piece coordinates
    - black_k(list(tuples(int,int))): list of black king piece coordinates
    - white_k(list(tuples(int,int))): list of white king piece coordinates

    Output:
    - Checkers Object
    """
    game = clear_board()
    for bpiece in black:
        game._place_piece(bpiece, "DARK")
    for wpiece in white:
        game._place_piece(wpiece, "LIGHT")
    for wking in white_k:
        game._place_piece(wking, "LIGHT", king=True)
    for bking in black_k:
        game._place_piece(bking, "DARK", king=True)
    return game


