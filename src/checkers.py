"""
File for creating Checkers/Checkers-adjacent games

Examples for Checkers:
x = Checkers()
#Creates a new checkers board with n = 3
x.move_piece((2,1),(3,2,'NC'), "LIGHT")
# Moves the piece at (2,1) to (3,2). Returns None and prints an error if 
# the move is illegal
x.piece_all_moves((3,2), "LIGHT")
# Returns a list with all the moves of the piece at (3,2)
x.all_moves("LIGHT")
# Returns a dictionary with all the moves white can make.
x.check_winner()
# Returns a string that states the winner color or no winner.

"""
from colorama import Fore


class Square:
    """
    Used to represent each square on the board in the Board class.

    Attributes:
    color (str): color of the square
    row (int): row of the square
    column (int): column of the square
    piece (None or Checkers): The piece inside the square (or None if no piece)
    north (None or square): The piece north of the square
    east (None or square): The piece east of the square
    south (None or square): The piece south of the square
    west (None or square): The piece west of the square
    """

    def __init__(self, color_sq, row, column):
        """
        Constructor

        Parameters:
            color_sq : color(str)
            row : int
            column : int

        Initializes an empty square with no neighbors.
        """
        self.color = color_sq
        self.row = row
        self.column = column
        self.piece = None
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def __str__(self):
        """
        str method, returns str
        """
        if self.color == "DARK":
            sq = Fore.BLACK + "X" + Fore.RESET
        else:
            sq = " "

        if self.piece is None:
            p = " "
        else:
            p = str(self.piece)
        s_or_h = " "
        return f"{sq} {p}{s_or_h}"

    def up_diagonals(self):
        """
        Returns a list of the coords of the square's upwards diagonals.

        Returns list[tuples(int, int)]
        """
        diag = []
        if self.north is not None and self.east is not None:
            diag.append((self.row - 1, self.column + 1))
        if self.north is not None and self.west is not None:
            diag.append((self.row - 1, self.column - 1))
        return diag

    def down_diagonals(self):
        """
        Returns a list of the coords of the square's downwards diagonals.

        Returns list[tuples(int, int)]
        """
        diag = []
        if self.south is not None and self.east is not None:
            diag.append((self.row + 1, self.column + 1))
        if self.south is not None and self.west is not None:
            diag.append((self.row + 1, self.column - 1))
        return diag

    def all_diagonals(self):
        """
        Returns a list of the coords of all the square's diagonals.

        Returns list[tuples(int, int)]
        """
        return self.up_diagonals() + self.down_diagonals()


class Board:
    """
    Used to create a representation of a generalized board.

    Attributes:
    board_grid (lst[lst[squares]]): list of a list of squares on the board.
    pieces_white_set (set): set of the coordinates all white pieces
    pieces_black_set (set): set of the coordinates all black pieces
    rows (int): number of rows on the board
    columns (int): number of columns on the board
    turn (str): Color of the current turn's player
    winner (None or str): color of winner (str), "DRAW" if draw, None if no winner
    white_draw_offer (bool): whether or not white offers a draw
    black_draw_offer (bool): whether or not black offers a draw
    """

    def __init__(self, row, column, turn="LIGHT"):
        """
        Constructor

        Parameters:
            rows (int): number of rows on the board
            columns (int): number of columns on the board
            turn (str): color of current player's turn

        Initializes board with set side length.
        """
        self.pieces_white_set = set([])
        self.pieces_black_set = set([])
        self.board_grid = self.board_creator(row, column)
        self.rows = row
        self.columns = column
        self.turn = turn
        self.white_draw_offer = False
        self.black_draw_offer = False
        self.winner = None

    def __str__(self):
        """
        str method of Board class.
        """
        return self._board_str()

    def _board_str(self):
        """
        Returns string format of board.

        Parameters: (None)

        Returns: str
        """
        brd_str = ""
        brd_str += " ____" * self.rows
        brd_str += "\n"
        for sq_lst in self.board_grid:
            brd_str += "|"
            for sq in sq_lst:
                brd_str += str(sq) + "|"
            brd_str += "\n"
            brd_str += "|"
            brd_str += "____|" * self.rows
            brd_str += "\n"
        return brd_str

    def board_creator(self, row, column):
        """
        Takes a side length(int) and returns a board with
        each square connected to the squares above, below, and to its sides.

        Parameters:
            rows (int): number of rows on the board
            columns (int): number of columns on the board

        Returns: board(list[list[squares]])
        """
        board_lst = []
        for row_num in range(row):
            board_lst.append([])
            for col_num in range(column):
                if (row_num + col_num) % 2 == 0:
                    board_lst[row_num].append(
                        Square("LIGHT", row_num, col_num)
                    )
                else:
                    board_lst[row_num].append(Square("DARK", row_num, col_num))
        for i, sq_lst in enumerate(board_lst):
            for j, _ in enumerate(sq_lst):
                if i != 0:
                    board_lst[i][j].north = board_lst[i - 1][j]
                if i != len(board_lst) - 1:
                    board_lst[i][j].south = board_lst[i + 1][j]
                if j != 0:
                    board_lst[i][j].west = board_lst[i][j - 1]
                if j != len(sq_lst) - 1:
                    board_lst[i][j].east = board_lst[i][j + 1]
        return board_lst


class Checkers:
    """
    Used to create the game logic of checkers. Is played on the board made from
    the Board class.
    """

    def __init__(self, n=3):
        """
        Constructor

        Args:
        board (Board): board used for the game
        num_light (int): number of light pieces on the board
        num_dark (int): number of dark pieces on the board
        side_len (int): length of board
        moves_since_capture (int): moves since capture

        Parameters:
            n: int (number of starting rows with pieces for each player)

        Initializes empty checkers board.
        """
        self.num_light = 0
        self.num_dark = 0
        self.side_len = 2 * n + 2
        self.moves_since_capture = 0
        self.board = self._place_pieces(Board(self.side_len, self.side_len))
        for i, sq_lst in enumerate(self.board.board_grid):
            for j, sq in enumerate(sq_lst):
                if sq.piece is not None:
                    if sq.piece.color == "LIGHT":
                        self.board.pieces_white_set.add((i, j))
                    elif sq.piece.color == "DARK":
                        self.board.pieces_black_set.add((i, j))

    def _place_pieces(self, board):
        """
        Given a board, places checkers pieces on the board according to the
        checkers ruleset.

        Parameters:
            board : Board

        Returns: None
        """
        n = (board.columns - 2) / 2
        for i, sq_lst in enumerate(board.board_grid):
            for j, sq in enumerate(sq_lst):
                if sq.color == "DARK":
                    if i < n:
                        board.board_grid[i][j].piece = Checkers_Piece("LIGHT")
                        self.num_light += 1
                    elif (
                        len(board.board_grid) - n - 1
                        < i
                        < len(board.board_grid)
                    ):
                        board.board_grid[i][j].piece = Checkers_Piece("DARK")
                        self.num_dark += 1
        return board

    def __str__(self):
        """
        str method, returns str
        """
        return Board._board_str(self.board)

    def check_winner(self):
        """
        Checks the current board to see if there is a winner.

        Parameters: (None)

        Returns: str ("Black Wins" or "White Wins" or "No Winner")
        """
        if self.num_light == 0 or len(self.all_moves("LIGHT")) == 0:
            self.board.winner = "DARK"
            return "Black Wins"
        elif self.num_dark == 0 or len(self.all_moves("DARK")) == 0:
            self.board.winner = "LIGHT"
            return "White Wins"
        elif self.moves_since_capture == 40:
            self.board.winner = "DRAW"
            return "DRAW"
        return "No Winner"

    def resign(self, color_player):
        """
        Player color resigns, setting board.winner to the color of the opposite
        player. Returns color of the winner.
        """
        if color_player == "LIGHT":
            self.board.winner = "DARK"
            return "Black Wins"
        else:
            self.board.winner = "LIGHT"
            return "White Wins"

    def draw_offer(self, color_player):
        """
        Player color offers/accepts a draw. Returns "DRAW" and sets
        board.winner state to draw if both players accept.
        """
        if color_player == "LIGHT":
            self.board.white_draw_offer = True
        elif color_player == "DARK":
            self.board.black_draw_offer = True
        if self.board.white_draw_offer and self.board.black_draw_offer:
            self.board.winner = "DRAW"
            return "DRAW"

    def undo_draw_offer(self):
        """
        Sets the draw offer for both players to False.
        """
        self.board.white_draw_offer = False
        self.board.black_draw_offer = False

    def move_piece(
        self, piece_loc, board_loc, color_p, king=False, capture=False
    ):
        """
        Given the coordinates of a piece and the coordinates of a square on the
        board, moves the piece to the square. Returns a message about the move.

        Parameters:
        piece (tuple(int, int)): coordinates of the piece to be moved
        board_loc (tuple(int, int, str)): coordinates of the square to be moved
        to and status of capture ('N' or "C")
        color_p (str): color of the player
        king (bool): if selected piece is a king
        capture (bool): can only make capture moves

        Returns: str
        """
        # Need to input (row, column)
        if color_p != self.board.turn:
            print("Move Not Legal")
            return "Move Not Legal"
        if not self._check_sq(piece_loc, color_p):
            print("Move Not Legal")
            return "Move Not Legal"
        row1 = piece_loc[0]
        col1 = piece_loc[1]
        row2 = board_loc[0]
        col2 = board_loc[1]
        lst_moves = self.piece_all_moves(piece_loc, color_p, king, capture)
        if board_loc not in lst_moves:
            print("Move Not Legal")
            return "Move Not Legal"
        if color_p == "LIGHT":
            opp_color = "DARK"
        else:
            opp_color = "LIGHT"
        self._remove_piece((row1, col1))
        to_king = king
        if board_loc[0] == 0 or board_loc[0] == self.board.rows - 1:
            to_king = True
        self._place_piece((row2, col2), color_p, to_king)
        self.moves_since_capture += 1
        if board_loc[2] == "C":
            self._remove_piece(((row1 + row2) // 2, (col1 + col2) // 2))
            self.moves_since_capture = 0
        print(self)
        if (
            board_loc[2] == "C"
            and len(self.piece_all_moves((row2, col2), color_p, king, True))
            != 0
        ):
            print("Move Piece Again")
            self.board.turn = color_p
            return "Move Piece Again"
        else:
            print("End Turn")
            self.board.turn = opp_color
            return "End Turn"

    def _check_sq(self, piece_loc, color_p):
        """
        Given a piece, determines if the piece is in a legal starting square.

        Parameters:
        piece_loc (tuple(int, int)): coordinates of the piece to be checked

        Returns: bool (True if the square is legal, False if not)
        """
        # for piece and board loc, need to input as (row, column)
        x1 = piece_loc[0]
        y1 = piece_loc[1]
        if piece_loc not in self.all_moves(color_p).keys():
            return False
        if not 0 <= x1 <= self.board.rows or not 0 <= y1 <= self.board.columns:
            return False
        start_sq = self.board.board_grid[x1][y1]
        piece = start_sq.piece
        if piece is None:
            return False
        if piece.color != color_p:
            return False
        return True

    def piece_all_moves(
        self,
        piece_loc,
        p_color,
        king=False,
        capture=False,
    ) -> list:
        """
        Given a piece location, returns a list of coords of possible moves.
        Assumes starting position is on the board and contains a piece.

        Parameters:
        piece (tuple(int, int)): coordinates of the piece to be moved
        color_p (str): color of the player
        king (bool): if selected piece is a king
        capture (bool): display only capture moves
        lst_moves (lst[tuple(int, int, str)]): a list of given moves with a str
        designating the status of capture.

        Returns: list[tuple(int, int)]
        """
        # input coords as (row, column)
        lst_moves = []
        row1 = piece_loc[0]
        col1 = piece_loc[1]
        bg = self.board.board_grid
        start_sq = bg[row1][col1]
        if p_color == "LIGHT":
            opp_color = "DARK"
            if not king:
                diag = Square.down_diagonals
            else:
                diag = Square.up_diagonals
        elif p_color == "DARK":
            opp_color = "LIGHT"
            if not king:
                diag = Square.up_diagonals
            else:
                diag = Square.down_diagonals
        for row2, col2 in diag(start_sq):
            if p_color == "LIGHT":
                if not king:
                    next_row = row2 + 1
                else:
                    next_row = row2 - 1
            else:
                if not king:
                    next_row = row2 - 1
                else:
                    next_row = row2 + 1
            if bg[row2][col2].piece is None:
                if not capture:
                    lst_moves.append((row2, col2, "NC"))
                continue
            if (
                self.board.board_grid[row2][col2].piece.color == opp_color
                and 0 <= next_row < self.board.rows
            ):
                if col2 > col1 and col2 + 1 < self.board.columns:
                    next_col = col2 + 1
                elif col2 < col1 and col2 - 1 >= 0:
                    next_col = col2 - 1
                else:
                    continue
                if bg[next_row][next_col] is not None:
                    if bg[next_row][next_col].piece is None:
                        lst_moves.append((next_row, next_col, "C"))
        for coords in lst_moves:
            if coords[2] == "C":
                for coords2 in lst_moves:
                    if coords2[2] == "NC":
                        lst_moves.remove(coords2)
        if king:
            return list(set(lst_moves)) + self.piece_all_moves(
                piece_loc,
                p_color,
                False,
            )
        return list(set(lst_moves))

    def all_moves(self, color_move):
        """
        Returns a list of all possible moves on the board.

        Parameters:
        color_move (str): color of the player

        Returns: dict{'tuple(int, int)': list[tuple(int, int, str)]}
        """
        all_moves_dict = {}
        if color_move == "DARK":
            pieces_loc = self.board.pieces_black_set
        elif color_move == "LIGHT":
            pieces_loc = self.board.pieces_white_set
        capture = False
        for coords in list(pieces_loc):
            move_lst1 = self.piece_all_moves(
                coords,
                color_move,
                self.board.board_grid[coords[0]][coords[1]].piece.king,
            )
            for coords2 in move_lst1:
                if coords2[2] == "C":
                    capture = True
            all_moves_dict[(coords[0], coords[1])] = move_lst1
        all_moves_dict = {k: v for k, v in all_moves_dict.items() if v}
        if capture:
            for key in all_moves_dict.keys():
                for i, coords2 in enumerate(all_moves_dict[key]):
                    if coords2[2] == "NC":
                        all_moves_dict[key][i] = ()
        for keys, lsts in all_moves_dict.items():
            lsts = [v for v in lsts if v != ()]
            all_moves_dict[keys] = lsts
        all_moves_dict = {k: v for k, v in all_moves_dict.items() if v}
        return all_moves_dict

    def calculate_boardstate(self):
        """
        Calculates the boardstate used for bot implementation
        """
        boardstate = 0
        for row, col in self.board.pieces_white_set:
            if self.board.board_grid[row][col].piece.king:
                boardstate += 2
            else:
                boardstate += 1
        for row, col in self.board.pieces_black_set:
            if self.board.board_grid[row][col].piece.king:
                boardstate -= 2
            else:
                boardstate -= 1
        if self.board.winner == "LIGHT":
            boardstate += 1000
        elif self.board.winner == "DARK":
            boardstate -= 1000
        return boardstate

    def _place_piece(self, loc, color, king=False):
        """
        Places a piece in the location given its coords, color, and king state.
        """
        # input location as (row, column)
        self.board.board_grid[loc[0]][loc[1]].piece = Checkers_Piece(
            color, king
        )
        if color == "LIGHT":
            self.board.pieces_white_set.add((loc))
        else:
            self.board.pieces_black_set.add((loc))
        print(self)

    def _remove_piece(self, loc):
        """
        Removes a piece in the location. Make sure there is a piece in the
        location before using.
        """
        # input location as (row, column)
        if self.board.board_grid[loc[0]][loc[1]].piece.color == "LIGHT":
            self.board.pieces_white_set.remove((loc))
        else:
            self.board.pieces_black_set.remove((loc))
        self.board.board_grid[loc[0]][loc[1]].piece = None
        print(self)


def make_test_board():
    """
    Test for king movement
    """
    x = Checkers()
    x._remove_piece((6, 5))
    x._remove_piece((6, 1))
    x._place_piece((3, 2), "DARK")
    x._place_piece((6, 5), "LIGHT", True)
    return x


def clear_board():
    """
    Creates clear board
    """
    x = Checkers()
    for i in range(x.board.rows):
        for j in range(x.board.columns):
            x.board.board_grid[i][j].piece = None
    x.board.pieces_white_set = set()
    x.board.pieces_black_set = set()
    return x


def winner_check():
    """
    Creates a winning situation for black
    """
    x = clear_board()
    x._place_piece((0, 0), "LIGHT")
    x._place_piece((1, 1), "DARK")
    x._place_piece((2, 2), "DARK")
    return x


class Checkers_Piece:
    """
    Class for representing checkers pieces.

    Attriubutes:
    color (str): color of the piece
    king (bool): determines whether the piece is a king
    """

    def __init__(self, color_p, king=False):
        """
        Constructor

        Parameters:
            color_p (str): color of the piece
            king (bool): if the piece is a king or not

        Initializes a regular or king piece.
        """
        self.color = color_p
        self.king = king

    def __str__(self) -> str:
        """
        str method, returns str
        """
        ret_str = "o"
        if not self.king:
            if self.color == "DARK":
                ret_str = Fore.RED + "R" + Fore.RESET
            elif self.color == "LIGHT":
                ret_str = Fore.WHITE + "W" + Fore.RESET
        elif self.color == "DARK":
            ret_str = Fore.RED + "\033[4mR\033[0m" + Fore.RESET
        elif self.color == "LIGHT":
            ret_str = Fore.WHITE + "\033[4mW\033[0m" + Fore.RESET
        return ret_str
