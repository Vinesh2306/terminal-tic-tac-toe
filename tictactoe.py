import os
import sys

HUMAN    = "X"
COMPUTER = "O"
EMPTY    = " "

WINNING_PATTERNS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


def create_board():
    return [EMPTY] * 9


def display_board(board):
    def cell(i):
        return board[i] if board[i] != EMPTY else " "

    print()
    print("  " + cell(0) + " | " + cell(1) + " | " + cell(2))
    print("  ---------")
    print("  " + cell(3) + " | " + cell(4) + " | " + cell(5))
    print("  ---------")
    print("  " + cell(6) + " | " + cell(7) + " | " + cell(8))
    print()


def get_available_moves(board):
    return [i for i, c in enumerate(board) if c == EMPTY]


def is_board_full(board):
    return EMPTY not in board


def check_winner(board, player):
    for a, b, c in WINNING_PATTERNS:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def get_winning_line(board, player):
    for pattern in WINNING_PATTERNS:
        a, b, c = pattern
        if board[a] == board[b] == board[c] == player:
            return pattern
    return None


def get_player_move(board):
    while True:
        try:
            raw = input("  Your move (1-9): ").strip()
            if not raw:
                print("  Invalid! Enter a number from 1-9.")
                continue
            position = int(raw)
            if position < 1 or position > 9:
                print("  Invalid! Choose a position from 1-9.")
                continue
            index = position - 1
            if board[index] != EMPTY:
                print("  Position " + str(position) + " is taken! Choose another.")
                continue
            return index
        except ValueError:
            print("  Invalid input! Enter a number from 1-9.")


def minimax(board, depth, is_maximizing):
    if check_winner(board, COMPUTER):
        return 10 - depth
    if check_winner(board, HUMAN):
        return depth - 10
    if is_board_full(board):
        return 0

    available = get_available_moves(board)

    if is_maximizing:
        best = -1000
        for move in available:
            board[move] = COMPUTER
            score = minimax(board, depth + 1, False)
            board[move] = EMPTY
            if score > best:
                best = score
        return best
    else:
        best = 1000
        for move in available:
            board[move] = HUMAN
            score = minimax(board, depth + 1, True)
            board[move] = EMPTY
            if score < best:
                best = score
        return best


def get_computer_move(board):
    available = get_available_moves(board)
    if len(available) == 1:
        return available[0]

    PREFERENCE = [4, 0, 2, 6, 8, 1, 3, 5, 7]  # center > corners > edges
    best_score, best_move, best_priority = -1000, available[0], len(PREFERENCE)

    for move in available:
        board[move] = COMPUTER
        score = minimax(board, 0, False)
        board[move] = EMPTY
        priority = PREFERENCE.index(move) if move in PREFERENCE else len(PREFERENCE)
        if score > best_score or (score == best_score and priority < best_priority):
            best_score, best_move, best_priority = score, move, priority

    return best_move


def clear_screen():
    os.system("cls" if sys.platform == "win32" else "clear")


def print_header():
    print()
    print("================================")
    print("        TIC-TAC-TOE")
    print("   Human (X) vs Computer (O)")
    print("================================")
    print("  You: X    Computer: O")
    print()


def print_instructions():
    print("  Enter 1-9 to place your X.")
    print()
    print("    1 | 2 | 3")
    print("    ---------")
    print("    4 | 5 | 6")
    print("    ---------")
    print("    7 | 8 | 9")
    print()


def play_game():
    board = create_board()
    print_header()
    print_instructions()
    display_board(board)

    turn = HUMAN

    while True:
        if turn == HUMAN:
            print("  Your turn (X):")
            move = get_player_move(board)
            board[move] = HUMAN
            display_board(board)

            if check_winner(board, HUMAN):
                print("  You Win!\n")
                return
            if is_board_full(board):
                print("  It's a Draw!\n")
                return

            turn = COMPUTER

        else:
            print("  Computer is thinking...")
            move = get_computer_move(board)
            board[move] = COMPUTER
            print("  Computer placed O at position " + str(move + 1) + ".")
            display_board(board)

            if check_winner(board, COMPUTER):
                print("  Computer Wins!\n")
                return
            if is_board_full(board):
                print("  It's a Draw!\n")
                return

            turn = HUMAN


def main():
    clear_screen()
    while True:
        play_game()
        while True:
            again = input("  Play again? (y/n): ").strip().lower()
            if again in ("y", "yes"):
                clear_screen()
                break
            elif again in ("n", "no"):
                print("\n  Thanks for playing! Goodbye.\n")
                sys.exit(0)
            else:
                print("  Enter y or n.")


if __name__ == "__main__":
    main()
