

import math
import time


class TicTacToe:

    def __init__(self):
        # Board positions 0-8, mapped like a phone keypad-less 3x3 grid:
        #  0 | 1 | 2
        #  3 | 4 | 5
        #  6 | 7 | 8
        self.board = [" " for _ in range(9)]

    def print_board(self):
        b = self.board
        print()
        print(f"  {b[0]} | {b[1]} | {b[2]} ")
        print(" ---+---+---")
        print(f"  {b[3]} | {b[4]} | {b[5]} ")
        print(" ---+---+---")
        print(f"  {b[6]} | {b[7]} | {b[8]} ")
        print()

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def make_move(self, position, letter):
        if self.board[position] == " ":
            self.board[position] = letter
            return True
        return False

    def undo_move(self, position):
        self.board[position] = " "

    def is_full(self):
        return " " not in self.board

    def winner(self):
        """Returns 'X', 'O', or None if there is no winner yet."""
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],   # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],   # columns
            [0, 4, 8], [2, 4, 6],              # diagonals
        ]
        for combo in win_combinations:
            a, b, c = combo
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def game_over(self):
        return self.winner() is not None or self.is_full()


class AIPlayer:
    """AI agent that uses Minimax (with optional Alpha-Beta pruning)."""

    def __init__(self, letter, opponent_letter, use_alpha_beta=True):
        self.letter = letter
        self.opponent_letter = opponent_letter
        self.use_alpha_beta = use_alpha_beta
        self.nodes_explored = 0

    def get_move(self, game: TicTacToe):
        self.nodes_explored = 0
        best_score = -math.inf
        best_move = None

        for move in game.available_moves():
            game.make_move(move, self.letter)
            if self.use_alpha_beta:
                score = self.minimax(game, 0, False, -math.inf, math.inf)
            else:
                score = self.minimax_plain(game, 0, False)
            game.undo_move(move)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax_plain(self, game, depth, is_maximizing):
        """Plain Minimax without pruning."""
        self.nodes_explored += 1
        winner = game.winner()
        if winner == self.letter:
            return 10 - depth
        elif winner == self.opponent_letter:
            return depth - 10
        elif game.is_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in game.available_moves():
                game.make_move(move, self.letter)
                score = self.minimax_plain(game, depth + 1, False)
                game.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for move in game.available_moves():
                game.make_move(move, self.opponent_letter)
                score = self.minimax_plain(game, depth + 1, True)
                game.undo_move(move)
                best_score = min(best_score, score)
            return best_score

    def minimax(self, game, depth, is_maximizing, alpha, beta):
        """Minimax with Alpha-Beta pruning."""
        self.nodes_explored += 1
        winner = game.winner()
        if winner == self.letter:
            return 10 - depth
        elif winner == self.opponent_letter:
            return depth - 10
        elif game.is_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in game.available_moves():
                game.make_move(move, self.letter)
                score = self.minimax(game, depth + 1, False, alpha, beta)
                game.undo_move(move)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return best_score
        else:
            best_score = math.inf
            for move in game.available_moves():
                game.make_move(move, self.opponent_letter)
                score = self.minimax(game, depth + 1, True, alpha, beta)
                game.undo_move(move)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return best_score


def get_human_move(game: TicTacToe):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move not in range(9):
                print("Please enter a number between 1 and 9.")
                continue
            if move not in game.available_moves():
                print("That spot is already taken. Try again.")
                continue
            return move
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")


def print_position_guide():
    print("Position guide (use these numbers to choose your move):")
    print("  1 | 2 | 3 ")
    print(" ---+---+---")
    print("  4 | 5 | 6 ")
    print(" ---+---+---")
    print("  7 | 8 | 9 ")
    print()


def choose_algorithm():
    print("Choose AI mode:")
    print("  1. Minimax with Alpha-Beta Pruning (faster)")
    print("  2. Plain Minimax (slower, explores more nodes)")
    choice = input("Enter choice (1 or 2), default is 1: ").strip()
    return choice != "2"


def play_game():
    print("=" * 40)
    print("   WELCOME TO UNBEATABLE TIC-TAC-TOE")
    print("=" * 40)
    print_position_guide()

    use_alpha_beta = choose_algorithm()

    first = input("Do you want to go first? (y/n): ").strip().lower()
    human_letter = "X"
    ai_letter = "O"
    human_first = first != "n"

    game = TicTacToe()
    ai = AIPlayer(ai_letter, human_letter, use_alpha_beta=use_alpha_beta)

    current_turn_human = human_first
    game.print_board()

    while not game.game_over():
        if current_turn_human:
            move = get_human_move(game)
            game.make_move(move, human_letter)
        else:
            print("AI is thinking...")
            start = time.time()
            move = ai.get_move(game)
            elapsed = time.time() - start
            game.make_move(move, ai_letter)
            print(f"AI chose position {move + 1} "
                  f"(explored {ai.nodes_explored} nodes in {elapsed:.4f}s)")

        game.print_board()
        current_turn_human = not current_turn_human

    winner = game.winner()
    if winner == human_letter:
        print("Congratulations! You won! (This shouldn't normally happen "
              "against a perfect AI!)")
    elif winner == ai_letter:
        print("The AI wins! Better luck next time.")
    else:
        print("It's a draw!")


def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()
