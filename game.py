"""
game.py
-------
Core Tic-Tac-Toe game mechanics:
- Board representation (3x3 grid using 0-8 indexing)
- Move validation and execution
- Terminal state detection and win/draw evaluation
- Board visualization for console display
"""

from typing import List, Optional, Tuple


class Board:
    """Represents a 3x3 Tic-Tac-Toe board."""

    WINNING_COMBINATIONS: List[Tuple[int, int, int]] = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]

    def __init__(self, state: Optional[List[str]] = None):
        """
        Initialize the board.
        :param state: Optional list of 9 characters ('X', 'O', or ' ').
        """
        if state is not None:
            self.cells = list(state)
        else:
            self.cells = [' '] * 9

    def make_move(self, index: int, player: str) -> bool:
        """
        Execute a move on the board.
        :param index: Cell index (0 to 8).
        :param player: Player mark ('X' or 'O').
        :return: True if move was valid and placed, False otherwise.
        """
        if 0 <= index < 9 and self.cells[index] == ' ':
            self.cells[index] = player
            return True
        return False

    def undo_move(self, index: int) -> None:
        """
        Undo a move by resetting the cell to empty.
        Used for fast in-place game tree exploration.
        """
        if 0 <= index < 9:
            self.cells[index] = ' '

    def get_available_moves(self) -> List[int]:
        """Return list of indices for available empty cells."""
        return [i for i, cell in enumerate(self.cells) if cell == ' ']

    def is_full(self) -> bool:
        """Check if board has no empty cells remaining."""
        return ' ' not in self.cells

    def check_winner(self) -> Optional[str]:
        """
        Check board for game result:
        :return: 'X' if X won, 'O' if O won, 'Draw' if tied, or None if ongoing.
        """
        for a, b, c in self.WINNING_COMBINATIONS:
            if self.cells[a] != ' ' and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]

        if self.is_full():
            return 'Draw'

        return None

    def is_terminal(self) -> bool:
        """Check if game has ended (win or draw)."""
        return self.check_winner() is not None

    def clone(self) -> "Board":
        """Return a copy of the current board."""
        return Board(self.cells)

    def display(self) -> None:
        """Print the current board in a user-friendly format."""
        symbols = [cell if cell != ' ' else '.' for cell in self.cells]
        print("\n Current Board:        Cell Reference (1-9):")
        print(f"  {symbols[0]} | {symbols[1]} | {symbols[2]}               1 | 2 | 3")
        print(" ---+---+---             ---+---+---")
        print(f"  {symbols[3]} | {symbols[4]} | {symbols[5]}               4 | 5 | 6")
        print(" ---+---+---             ---+---+---")
        print(f"  {symbols[6]} | {symbols[7]} | {symbols[8]}               7 | 8 | 9\n")
