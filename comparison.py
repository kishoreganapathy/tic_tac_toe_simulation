"""
comparison.py
-------------
Comprehensive comparative analysis suite between:
1. Standard Minimax Algorithm
2. Alpha-Beta Pruning Algorithm

Provides:
- Fixed Scenario Benchmarking (Opening, Midgame, Forks, Defense, Endgame)
- Full Turn-by-Turn Game Analysis (Dual evaluation at every step)
- Head-to-Head AI vs AI Matches
- Statistical Summaries (State space reduction %, Speedup factor, Pruning frequency)
"""

from typing import List, Tuple, Dict, Any
from game import Board
from algorithms import MinimaxAgent, AlphaBetaAgent, SearchMetrics


def print_separator(char: str = "=", length: int = 80) -> None:
    print(char * length)


def run_scenario_benchmarks() -> List[Dict[str, Any]]:
    """
    Evaluates Minimax vs Alpha-Beta Pruning across standard strategic scenarios.
    """
    scenarios: List[Tuple[str, List[str], str]] = [
        (
            "1. Empty Board (Opening Move)",
            [' '] * 9,
            'X'
        ),
        (
            "2. Opponent Center Move (Early)",
            [' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' '],
            'O'
        ),
        (
            "3. Mid-Game Balanced State",
            ['X', 'O', ' ', ' ', 'X', ' ', ' ', ' ', 'O'],
            'X'
        ),
        (
            "4. Fork Setup (Dual Threat)",
            ['X', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'X'],
            'O'
        ),
        (
            "5. Defensive Block Required",
            ['X', 'X', ' ', ' ', 'O', ' ', ' ', ' ', ' '],
            'O'
        ),
        (
            "6. Immediate Winning Strike",
            ['X', 'O', 'X', ' ', 'X', ' ', 'O', ' ', 'O'],
            'X'
        )
    ]

    minimax_agent = MinimaxAgent()
    alphabeta_agent = AlphaBetaAgent()

    print_separator("=")
    print(" SCENARIO BENCHMARK: MINIMAX vs ALPHA-BETA PRUNING")
    print_separator("=")
    print(
        f"{'Scenario':<32} | {'Player':<6} | {'Algorithm':<18} | "
        f"{'Move':<5} | {'Score':<5} | {'Nodes':<10} | {'Prunes':<7} | {'Time (ms)':<9}"
    )
    print_separator("-")

    results = []

    for name, state, player in scenarios:
        board = Board(state)

        # Minimax evaluation
        m_move, m_metric = minimax_agent.get_move(board, player)

        # Alpha-Beta evaluation
        ab_move, ab_metric = alphabeta_agent.get_move(board, player)

        # Calculate reduction %
        reduction_pct = 0.0
        if m_metric.nodes_evaluated > 0:
            reduction_pct = (
                (m_metric.nodes_evaluated - ab_metric.nodes_evaluated)
                / m_metric.nodes_evaluated
            ) * 100.0

        speedup = (
            (m_metric.time_taken_ms / ab_metric.time_taken_ms)
            if ab_metric.time_taken_ms > 0 else 1.0
        )

        results.append({
            "scenario": name,
            "player": player,
            "minimax": m_metric,
            "alphabeta": ab_metric,
            "reduction_pct": reduction_pct,
            "speedup": speedup
        })

        # Print Minimax row
        print(
            f"{name:<32} | {player:<6} | {m_metric.algorithm:<18} | "
            f"{m_move + 1:<5} | {m_metric.score:<5} | {m_metric.nodes_evaluated:<10,d} | "
            f"{'N/A':<7} | {m_metric.time_taken_ms:<9.2f}"
        )
        # Print Alpha-Beta row
        print(
            f"{'':<32} | {'':<6} | {ab_metric.algorithm:<18} | "
            f"{ab_move + 1:<5} | {ab_metric.score:<5} | {ab_metric.nodes_evaluated:<10,d} | "
            f"{ab_metric.pruning_count:<7,d} | {ab_metric.time_taken_ms:<9.2f}"
        )
        print(
            f"   >> Search Space Reduction: {reduction_pct:5.1f}%  |  "
            f"Speedup: {speedup:5.1f}x  |  Decisions Match: {'YES (Optimal)' if m_move == ab_move else 'NO'}"
        )
        print_separator("-")

    return results


def run_turn_by_turn_game_comparison() -> None:
    """
    Simulates a full game from scratch.
    At EVERY single turn, both algorithms independently evaluate the exact same
    board state to demonstrate how search complexity diminishes as the game progresses.
    """
    board = Board()
    minimax_agent = MinimaxAgent()
    alphabeta_agent = AlphaBetaAgent()

    print_separator("=")
    print(" FULL MATCH TURN-BY-TURN ANALYSIS (Both AI evaluate every state)")
    print_separator("=")
    print("At each turn, both algorithms evaluate the board state to compare effort.\n")

    current_player = 'X'
    turn = 1

    total_mm_nodes = 0
    total_ab_nodes = 0
    total_mm_time = 0.0
    total_ab_time = 0.0
    total_prunes = 0

    print(
        f"{'Turn':<5} | {'Player':<6} | {'Chosen Move':<11} | "
        f"{'Minimax Nodes':<14} | {'AlphaBeta Nodes':<16} | {'Reduction %':<12} | {'Prunings':<8}"
    )
    print_separator("-")

    while not board.is_terminal():
        # Evaluate with Minimax
        mm_move, mm_metrics = minimax_agent.get_move(board, current_player)

        # Evaluate with Alpha-Beta
        ab_move, ab_metrics = alphabeta_agent.get_move(board, current_player)

        # Accumulate metrics
        total_mm_nodes += mm_metrics.nodes_evaluated
        total_ab_nodes += ab_metrics.nodes_evaluated
        total_mm_time += mm_metrics.time_taken_ms
        total_ab_time += ab_metrics.time_taken_ms
        total_prunes += ab_metrics.pruning_count

        reduction = (
            ((mm_metrics.nodes_evaluated - ab_metrics.nodes_evaluated) / mm_metrics.nodes_evaluated * 100.0)
            if mm_metrics.nodes_evaluated > 0 else 0.0
        )

        chosen_move = ab_move  # Both choose optimal; use the move to progress board
        print(
            f"{turn:<5} | {current_player:<6} | Cell {chosen_move + 1:<6} | "
            f"{mm_metrics.nodes_evaluated:<14,d} | {ab_metrics.nodes_evaluated:<16,d} | "
            f"{reduction:<11.1f}% | {ab_metrics.pruning_count:<8,d}"
        )

        board.make_move(chosen_move, current_player)
        current_player = 'O' if current_player == 'X' else 'X'
        turn += 1

    winner = board.check_winner()
    print_separator("=")
    print(f" Match Result: {winner.upper() if winner != 'Draw' else 'DRAW (Perfect Play by Both Agents)'}")
    print_separator("-")
    print(" CUMULATIVE TOURNAMENT METRICS:")
    print(f"  * Total Minimax Nodes Evaluated : {total_mm_nodes:,}")
    print(f"  * Total Alpha-Beta Nodes        : {total_ab_nodes:,}")
    overall_reduction = (
        ((total_mm_nodes - total_ab_nodes) / total_mm_nodes * 100.0)
        if total_mm_nodes > 0 else 0.0
    )
    overall_speedup = (total_mm_time / total_ab_time) if total_ab_time > 0 else 1.0
    print(f"  * Total Branch Cutoffs (Prunes) : {total_prunes:,}")
    print(f"  * Overall State Space Reduction : {overall_reduction:.2f}%")
    print(f"  * Total Minimax Computation Time: {total_mm_time:.2f} ms")
    print(f"  * Total Alpha-Beta Time         : {total_ab_time:.2f} ms ({overall_speedup:.2f}x faster)")
    print_separator("=")


def run_head_to_head_matches() -> None:
    """
    Runs two complete AI vs AI matches:
    Game 1: Minimax as 'X', Alpha-Beta as 'O'
    Game 2: Alpha-Beta as 'X', Minimax as 'O'
    """
    print_separator("=")
    print(" HEAD-TO-HEAD MATCHPLAY: MINIMAX vs ALPHA-BETA PRUNING")
    print_separator("=")

    # Game 1
    print("\n--- GAME 1: Minimax (Player X) vs Alpha-Beta Pruning (Player O) ---")
    board1 = Board()
    agent_x1 = MinimaxAgent("Minimax")
    agent_o1 = AlphaBetaAgent("Alpha-Beta")
    run_single_ai_match(board1, agent_x1, agent_o1)

    # Game 2
    print("\n--- GAME 2: Alpha-Beta Pruning (Player X) vs Minimax (Player O) ---")
    board2 = Board()
    agent_x2 = AlphaBetaAgent("Alpha-Beta")
    agent_o2 = MinimaxAgent("Minimax")
    run_single_ai_match(board2, agent_x2, agent_o2)


def run_single_ai_match(board: Board, player_x_agent: Any, player_o_agent: Any) -> None:
    """Helper to run a single match between two specified agents."""
    turn = 1
    current = 'X'
    x_nodes = 0
    o_nodes = 0
    x_time = 0.0
    o_time = 0.0
    prunings = 0

    while not board.is_terminal():
        if current == 'X':
            move, met = player_x_agent.get_move(board, 'X')
            x_nodes += met.nodes_evaluated
            x_time += met.time_taken_ms
            prunings += met.pruning_count
            agent_label = player_x_agent.name
        else:
            move, met = player_o_agent.get_move(board, 'O')
            o_nodes += met.nodes_evaluated
            o_time += met.time_taken_ms
            prunings += met.pruning_count
            agent_label = player_o_agent.name

        board.make_move(move, current)
        print(
            f"  Turn {turn}: {agent_label} ('{current}') chose cell {move + 1} "
            f"| Nodes: {met.nodes_evaluated:,} | Time: {met.time_taken_ms:.2f} ms"
        )
        current = 'O' if current == 'X' else 'X'
        turn += 1

    board.display()
    winner = board.check_winner()
    print(f"  Result: {winner if winner != 'Draw' else 'Draw (Tie)'}")
    print(f"  Player X ({player_x_agent.name}) Total Nodes: {x_nodes:,} ({x_time:.2f} ms)")
    print(f"  Player O ({player_o_agent.name}) Total Nodes: {o_nodes:,} ({o_time:.2f} ms)")
    if prunings > 0:
        print(f"  Total Alpha-Beta Cutoffs: {prunings:,}")


if __name__ == "__main__":
    run_scenario_benchmarks()
    print("\n")
    run_turn_by_turn_game_comparison()
    print("\n")
    run_head_to_head_matches()
