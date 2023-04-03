"""
Ethan Jiang
GUI for Checkers
"""

import os
import sys
from typing import Union, Dict

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import click

from checkers import Square, Board, Checkers, Checkers_Piece

from bot import Bot
from colorama import Fore, Style

WIDTH = 800
HEIGHT = 800
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (122, 122, 122)
BLUE = (0, 0, 255)


class GUIPlayer:
    """
    Simple class to store information about a GUI player
    A GUI player can either a human player using the keyboard,
    or a bot.
    """

    def __init__(
        self, n: int, player_type: str, checkers: Checkers, color: str
    ):
        """Constructor
        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            checkers: The checkers game
            color: The player's color
        """

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = Bot(0, color)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = Bot(2, color)
        self.checkers = checkers
        self.selected = None


def draw_board(surface: pygame.surface.Surface, board_grid, all_moves) -> None:
    """Draws the current state of the board in the window
    Args:
        surface: Pygame surface to draw the board on
        board_grid: List of lists containing squares on board
        all_moves: List of possible moves for individual pieces
    """
    grid = board_grid
    nrows = len(grid)
    ncols = len(grid[0])

    surface.fill((0, 0, 255))

    # Compute the row height and column width
    rh = HEIGHT // nrows + 1
    cw = WIDTH // ncols + 1

    for row in range(nrows):
        for col in range(ncols):
            # Draw squares in the board
            rect = (col * cw, row * rh, cw, rh)
            square_col = (0, 255, 0)
            if grid[row][col].color == "DARK":
                square_col = BLACK
            elif grid[row][col].color == "LIGHT":
                square_col = RED
            pygame.draw.rect(surface, color=square_col, rect=rect)

            # Draw the circles for pieces
            if grid[row][col].piece is None:
                if grid[row][col].color == "LIGHT":
                    circ_col = RED
                elif grid[row][col].color == "DARK":
                    circ_col = BLACK
            elif grid[row][col].piece.color == "DARK":
                circ_col = GRAY
            elif grid[row][col].piece.color == "LIGHT":
                circ_col = WHITE

            center = (col * cw + cw // 2, row * rh + rh // 2)
            radius = rh // 2 - 8
            pygame.draw.circle(
                surface, color=circ_col, center=center, radius=radius
            )
            if grid[row][col].piece is not None and grid[row][col].piece.king:
                pygame.draw.circle(
                    surface, color=BLACK, center=center, radius=radius / 2
                )
    # Draw dots for possible moves
    if all_moves is not None:
        for loc in all_moves:
            center = (loc[1] * cw + cw // 2, loc[0] * rh + rh // 2)
            pygame.draw.circle(
                surface, color=BLUE, center=center, radius=radius / 2
            )


def process_click(pos, checkers, players, current_col):
    """
    Proccesses mouse click event
    Args:
        pos: Tuple(int, int)
        checkers: Checkers game
        players: dict[str, GUIPlayer]
        current_col: str, the current player turn
    Returns:
    """
    x, y = pos
    grid = checkers.board.board_grid
    length = len(grid)
    col = x // (WIDTH // length)
    row = y // (HEIGHT // length)
    player = players[current_col]
    # If piece is clicked, highlight possible moves
    if (
        grid[row][col].piece is not None
        and grid[row][col].piece.color == current_col
    ):
        king = grid[row][col].piece.king
        all_moves = checkers.piece_all_moves((row, col), current_col, king)
        player.selected = (row, col)
        return (False, all_moves)

    # Move a piece to a possible square
    elif player.selected is not None:
        selected_row, selected_col = player.selected
        king = grid[selected_row][selected_col].piece.king
        possible_moves = checkers.piece_all_moves(
            player.selected,
            current_col,
            king,
        )
        move_permit = False
        # Check is possible moves includes a capture
        if (row, col, "NC") in possible_moves:
            capture = "NC"
            p_capture = False
            move_permit = True
        elif (row, col, "C") in possible_moves:
            capture = "C"
            p_capture = True
            move_permit = True

        # Actually move the piece
        if move_permit:
            result = checkers.move_piece(
                player.selected, (row, col, capture), current_col, king
            )
            if result == "Move Not Legal":
                player.selected = None
                return (False, None)
            elif result == "Move Piece Again":
                player.selected = (row, col)
                p_capture = True
                return (False, None)
            p_capture = False
            player.selected = None
            return (True, None)
        player.selected = None
        return (False, None)
    return (False, None)


def play_checkers(
    checkers: Checkers, bot_delay: float, players: Dict[str, GUIPlayer]
) -> None:
    """
    Plays a game of Checkers on a Pygame window
    Args:
        checkers: A Checkers object
        players: A dictionary mapping piece colors to
          GUIPlayer objects.
        bot_delay: When playing as a bot, an artificial delay
          (in seconds) to wait before making a move.
    Returns: None
    """
    board = checkers.board.board_grid

    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Checkers")
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    all_moves = []
    no_winner = True
    current_col = "LIGHT"

    while no_winner:
        events = pygame.event.get()
        column = None
        moved = False
        if checkers.check_winner() != "No Winner":
            no_winner = False
        # Check for pygame events
        for event in events:
            # If user closes window, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Process mouse input
            if (
                players[current_col].bot is None
                and event.type == pygame.MOUSEBUTTONDOWN
            ):
                moved, all_moves = process_click(
                    pygame.mouse.get_pos(), checkers, players, current_col
                )

        # Make a move through the bot
        if players[current_col].bot is not None:
            pygame.time.wait(int(bot_delay * 1000))
            players[current_col].bot.move(checkers)
            moved = True

        # Change the turn if a move was made
        if moved:
            if current_col == "DARK":
                current_col = "LIGHT"
            elif current_col == "LIGHT":
                current_col = "DARK"

        # Update the display
        draw_board(surface, board, all_moves)
        pygame.display.update()
        clock.tick(24)

    # Display winner on the terminal
    winner = checkers.check_winner()
    if winner != "DRAW" and winner != "No Winner":
        print(winner)
    else:
        print("It's a tie!")


#
# Command-line interface
#

# Allow customization of player types, board size, and bot delay
@click.command(name="checkers-gui")
@click.option(
    "--player1",
    type=click.Choice(
        ["human", "random-bot", "smart-bot"], case_sensitive=False
    ),
    default="human",
)
@click.option(
    "--player2",
    type=click.Choice(
        ["human", "random-bot", "smart-bot"], case_sensitive=False
    ),
    default="human",
)
@click.option("-n", "--board-size", type=click.INT, default=3)
@click.option("--bot-delay", type=click.FLOAT, default=0.5)

# Run the GUI for checkers
def cmd(player1, player2, board_size, bot_delay):
    new_checkers = Checkers(board_size)
    p1 = GUIPlayer(1, player1, new_checkers, "LIGHT")
    p2 = GUIPlayer(2, player2, new_checkers, "DARK")
    players = {"LIGHT": p1, "DARK": p2}
    play_checkers(new_checkers, bot_delay, players)


if __name__ == "__main__":
    cmd()
