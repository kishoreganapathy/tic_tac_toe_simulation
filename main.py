"""
main.py
-------
Interactive CLI for Tic-Tac-Toe AI Simulation and Comparison:
- Demonstrates Minimax vs Alpha-Beta Pruning
- Benchmark suite
- Watch AI vs AI with step-by-step visual boards & live search stats
- Human vs Minimax / Alpha-Beta gameplay
"""

import sys
import time
from game import Board
from algorithms import MinimaxAgent, AlphaBetaAgent
from comparison import (
    run_scenario_benchmarks,
    run_turn_by_turn_game_comparison,
    run_head_to_head_matches,
    print_separator
)


def print_banner() -> None:
    print_separator("=")
    print("      TIC-TAC-TOE AI SIMULATION: MINIMAX vs ALPHA-BETA PRUNING")
    print("       A Comparative Study in Adversarial Game-Tree Search")
    print_separator("=")


def print_menu() -> None:
    print("\nSelect an option:")
    print("  [1] Run Full Benchmark & Side-by-Side Comparison")
    print("  [2] Watch AI vs AI Match (Minimax vs Alpha-Beta)")
    print("  [3] Play as Human vs Minimax AI")
    print("  [4] Play as Human vs Alpha-Beta Pruning AI")
    print("  [5] View Theoretical Analysis & Complexity Comparison")
    print("  [6] Exit")


def watch_ai_vs_ai() -> None:
    """Watch an AI vs AI match with step-by-s.000.0.tep display."""
    print_separator("-")
    print("AI vs AI Exhibition Match")
    print("Player X: Minimax Agent (Exhaustive search)")
    print("Player O: Alpha-Beta Pruning Agent (Optimized search)")
    print_separator("-")

    board = Board()
    agent_x = MinimaxAgent("Minimax")
    agent_o = AlphaBetaAgent("Alpha-Beta")

    board.display()
    current = 'X'
    turn = 1

    while not board.is_terminal():
        print(f"\n--- Turn {turn} (Player {current}) ---")
        if current == 'X':
            move, metrics = agent_x.get_move(board, 'X')
            print(f"Minimax ('X') evaluated {metrics.nodes_evaluated:,} nodes in {metrics.time_taken_ms:.2f} ms")
        else:
            move, metrics = agent_o.get_move(board, 'O')
            print(
                f"Alpha-Beta ('O') evaluated {metrics.nodes_evaluated:,} nodes "
                f"({metrics.pruning_count:,} prunings) in {metrics.time_taken_ms:.2f} ms"
            )

        print(f"Action: Placed mark at Cell {move + 1}")
        board.make_move(move, current)
        board.display()

        current = 'O' if current == 'X' else 'X'
        turn += 1
        time.sleep(0.3)  # brief pause for pleasant viewing

    winner = board.check_winner()
    print_separator("=")
    if winner == 'Draw':
        print("Final Result: DRAW! (Both algorithms play theoretically optimal moves)")
    else:
        print(f"Final Result: Player {winner} Wins!")
    print_separator("=")


def play_human_vs_ai(agent_type: str = "alphabeta") -> None:
    """
    Play against the AI and inspect how many nodes it evaluates on each move.
    """
    agent = AlphaBetaAgent() if agent_type == "alphabeta" else MinimaxAgent()
    agent_name = agent.name

    print_separator("-")
    print(f"Human vs {agent_name}")
    print_separator("-")

    # Choose symbol
    while True:
        try:
            choice = input("Do you want to play as X (first) or O (second)? [X/O]: ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print("\nReturning to menu.")
            return
        if choice in ['X', 'O']:
            human_player = choice
            ai_player = 'O' if human_player == 'X' else 'X'
            break
        print("Invalid choice. Please enter 'X' or 'O'.")

    board = Board()
    current = 'X'
    turn = 1

    board.display()

    while not board.is_terminal():
        print(f"\n--- Turn {turn}: Player {current}'s Move ---")
        if current == human_player:
            # Human move
            valid = False
            while not valid:
                try:
                    raw_input = input(f"Enter your move (1-9) for '{human_player}': ").strip()
                    val = int(raw_input) - 1
                    if val in board.get_available_moves():
                        board.make_move(val, human_player)
                        valid = True
                    else:
                        print(f"Cell {val + 1} is already occupied or invalid. Available: {[m+1 for m in board.get_available_moves()]}")
                except ValueError:
                    print("Please enter a valid integer between 1 and 9.")
                except (KeyboardInterrupt, EOFError):
                    print("\nGame aborted. Returning to menu.")
                    return
        else:
            # AI move
            print(f"AI ({agent_name}) is thinking...")
            move, metrics = agent.get_move(board, ai_player)
            board.make_move(move, ai_player)

            if isinstance(agent, AlphaBetaAgent):
                print(
                    f">> AI chose Cell {move + 1} | Nodes Evaluated: {metrics.nodes_evaluated:,} | "
                    f"Cutoffs: {metrics.pruning_count:,} | Time: {metrics.time_taken_ms:.2f} ms"
                )
            else:
                print(
                    f">> AI chose Cell {move + 1} | Nodes Evaluated: {metrics.nodes_evaluated:,} | "
                    f"Time: {metrics.time_taken_ms:.2f} ms"
                )

        board.display()
        current = 'O' if current == 'X' else 'X'
        turn += 1

    winner = board.check_winner()
    print_separator("=")
    if winner == 'Draw':
        print("Game Over: It's a DRAW! (Optimal defense maintained)")
    elif winner == human_player:
        print(f"Game Over: You ({human_player}) WIN! Congratulations!")
    else:
        print(f"Game Over: AI ({ai_player}) WINS! Better luck next time!")
    print_separator("=")


def view_theoretical_summary() -> None:
    """Displays algorithmic theory, complexity, and key takeaways."""
    print_separator("=")
    print(" THEORETICAL ANALYSIS & COMPARISON: MINIMAX vs ALPHA-BETA")
    print_separator("=")
    print("""
1. MINIMAX ALGORITHM:
   - Exhaustive depth-first search for two-player zero-sum games.
   - Alternates between Maximizing player (wants highest utility) and
     Minimizing player (wants lowest utility).
   - Time Complexity: O(b^d)
     where b = branching factor (~9 to 1 in Tic-Tac-Toe), d = max depth (up to 9).
   - In Tic-Tac-Toe, exploring an empty root searches 549,945 game tree nodes!

2. ALPHA-BETA PRUNING ALGORITHM:
   - Adversarial search optimization using branch-and-bound logic.
   - Maintains two bounds:
       * alpha: Best (highest) score guaranteed to Maximizer so far.
       * beta:  Best (lowest) score guaranteed to Minimizer so far.
   - Cutoff Rule: Prunes remaining siblings whenever beta <= alpha.
     (Why? The opponent would never allow this branch, so evaluating it is useless.)
   - Time Complexity:
       * Worst Case:  O(b^d) (if visited in worst order)
       * Best Case:   O(b^(d/2)) (doubles the searchable depth for the same cost!)
   - In Tic-Tac-Toe, evaluating the opening move drops from 549,945 down to ~20,865 nodes!
     (A ~96.2% reduction in computation with ZERO loss in decision quality).

3. KEY COMPARISON TAKEAWAY:
   - Admissibility / Optimality: Both algorithms choose IDENTICAL optimal moves.
   - Alpha-Beta Pruning NEVER alters the outcome; it only discards provably irrelevant nodes.
   - Efficiency: Up to 20x to 25x faster on large branching scenarios.
""")
    print_separator("=")


def main() -> None:
    print_banner()

    while True:
        print_menu()
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if choice == '1':
            run_scenario_benchmarks()
            print("\n")
            run_turn_by_turn_game_comparison()
            print("\n")
            run_head_to_head_matches()
        elif choice == '2':
            watch_ai_vs_ai()
        elif choice == '3':
            play_human_vs_ai(agent_type="minimax")
        elif choice == '4':
            play_human_vs_ai(agent_type="alphabeta")
        elif choice == '5':
            view_theoretical_summary()
        elif choice == '6':
            print("\nExiting Tic-Tac-Toe AI Simulation. Have a great day!\n")
            sys.exit(0)
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
