"""
algorithms.py
-------------
Implementation of Game Playing Algorithms:
1. Minimax Algorithm (Exhaustive Game-Tree Search)
2. Alpha-Beta Pruning Algorithm (Branch-and-Bound Optimization)

Includes instrumentation to record:
- Nodes evaluated (search tree expansion)
- Pruning cutoffs (branches saved)
- Execution latency in milliseconds
- Selected move and minimax evaluation score
"""

import time
from dataclasses import dataclass
from typing import Tuple, Optional
from game import Board


@dataclass
class SearchMetrics:
    """Stores performance and decision metrics for a single search run."""
    algorithm: str
    best_move: int
    score: int
    nodes_evaluated: int
    pruning_count: int
    time_taken_ms: float

    def __str__(self) -> str:
        return (
            f"[{self.algorithm}] Move: {self.best_move + 1} (idx {self.best_move}) | "
            f"Score: {self.score} | Nodes Evaluated: {self.nodes_evaluated:,} | "
            f"Prunings: {self.pruning_count:,} | Time: {self.time_taken_ms:.2f} ms"
        )


class MinimaxAgent:
    """
    Minimax AI Agent:
    Performs exhaustive depth-first exploration of the complete game tree.
    - Maximizer (Player 'X') aims for highest positive score.
    - Minimizer (Player 'O') aims for lowest negative score.
    - Depth-penalty ensures the agent prefers rapid victories and delays inevitable losses.
    """

    def __init__(self, name: str = "Minimax"):
        self.name = name
        self.nodes_evaluated = 0

    def _utility(self, winner: str, depth: int) -> int:
        """
        Evaluate terminal state with depth factor:
        - Win for X: 10 - depth (faster win has higher utility)
        - Win for O: depth - 10 (faster win for O has lower utility)
        - Draw: 0
        """
        if winner == 'X':
            return 10 - depth
        elif winner == 'O':
            return depth - 10
        return 0

    def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        """Recursive minimax core function."""
        self.nodes_evaluated += 1

        winner = board.check_winner()
        if winner is not None:
            return self._utility(winner, depth)

        if is_maximizing:
            best_value = -1000
            for move in board.get_available_moves():
                board.make_move(move, 'X')
                score = self._minimax(board, depth + 1, is_maximizing=False)
                board.undo_move(move)
                best_value = max(best_value, score)
            return best_value
        else:
            best_value = 1000
            for move in board.get_available_moves():
                board.make_move(move, 'O')
                score = self._minimax(board, depth + 1, is_maximizing=True)
                board.undo_move(move)
                best_value = min(best_value, score)
            return best_value

    def get_move(self, board: Board, player: str) -> Tuple[int, SearchMetrics]:
        """
        Find optimal move for the given player.
        :param board: Current Board state
        :param player: 'X' or 'O'
        :return: (best_move_index, SearchMetrics)
        """
        self.nodes_evaluated = 0
        available_moves = board.get_available_moves()

        if not available_moves:
            return -1, SearchMetrics(self.name, -1, 0, 0, 0, 0.0)

        start_time = time.perf_counter()

        if player == 'X':
            best_score = -1000
            best_move = available_moves[0]
            for move in available_moves:
                board.make_move(move, 'X')
                score = self._minimax(board, depth=1, is_maximizing=False)
                board.undo_move(move)
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = 1000
            best_move = available_moves[0]
            for move in available_moves:
                board.make_move(move, 'O')
                score = self._minimax(board, depth=1, is_maximizing=True)
                board.undo_move(move)
                if score < best_score:
                    best_score = score
                    best_move = move

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        metrics = SearchMetrics(
            algorithm=self.name,
            best_move=best_move,
            score=best_score,
            nodes_evaluated=self.nodes_evaluated,
            pruning_count=0,
            time_taken_ms=elapsed_ms
        )
        return best_move, metrics


class AlphaBetaAgent:
    """
    Alpha-Beta Pruning Agent:
    An adversarial search optimization that prunes game branches that cannot
    influence the final decision.
    - alpha: The highest score guaranteed to the maximizer along current path.
    - beta: The lowest score guaranteed to the minimizer along current path.
    - Cutoff occurs when beta <= alpha.
    """

    def __init__(self, name: str = "Alpha-Beta Pruning"):
        self.name = name
        self.nodes_evaluated = 0
        self.pruning_count = 0

    def _utility(self, winner: str, depth: int) -> int:
        """Evaluate terminal state with depth factor."""
        if winner == 'X':
            return 10 - depth
        elif winner == 'O':
            return depth - 10
        return 0

    def _alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        """Recursive alpha-beta core function."""
        self.nodes_evaluated += 1

        winner = board.check_winner()
        if winner is not None:
            return self._utility(winner, depth)

        if is_maximizing:
            best_value = -1000
            for move in board.get_available_moves():
                board.make_move(move, 'X')
                score = self._alpha_beta(board, depth + 1, alpha, beta, is_maximizing=False)
                board.undo_move(move)

                best_value = max(best_value, score)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  # Beta cutoff: minimizer wouldn't allow this branch
            return best_value
        else:
            best_value = 1000
            for move in board.get_available_moves():
                board.make_move(move, 'O')
                score = self._alpha_beta(board, depth + 1, alpha, beta, is_maximizing=True)
                board.undo_move(move)

                best_value = min(best_value, score)
                beta = min(beta, best_value)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  # Alpha cutoff: maximizer wouldn't allow this branch
            return best_value

    def get_move(self, board: Board, player: str) -> Tuple[int, SearchMetrics]:
        """
        Find optimal move for the given player using Alpha-Beta Pruning.
        :param board: Current Board state
        :param player: 'X' or 'O'
        :return: (best_move_index, SearchMetrics)
        """
        self.nodes_evaluated = 0
        self.pruning_count = 0
        available_moves = board.get_available_moves()

        if not available_moves:
            return -1, SearchMetrics(self.name, -1, 0, 0, 0, 0.0)

        start_time = time.perf_counter()
        alpha = -1000.0
        beta = 1000.0

        if player == 'X':
            best_score = -1000
            best_move = available_moves[0]
            for move in available_moves:
                board.make_move(move, 'X')
                score = self._alpha_beta(board, depth=1, alpha=alpha, beta=beta, is_maximizing=False)
                board.undo_move(move)

                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
        else:
            best_score = 1000
            best_move = available_moves[0]
            for move in available_moves:
                board.make_move(move, 'O')
                score = self._alpha_beta(board, depth=1, alpha=alpha, beta=beta, is_maximizing=True)
                board.undo_move(move)

                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        metrics = SearchMetrics(
            algorithm=self.name,
            best_move=best_move,
            score=best_score,
            nodes_evaluated=self.nodes_evaluated,
            pruning_count=self.pruning_count,
            time_taken_ms=elapsed_ms
        )
        return best_move, metrics
