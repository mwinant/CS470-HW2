import time
import math
from colorama import Fore, Style, init

init(autoreset=True)

ROWS = 6
COLS = 7
CONNECT_N = 4

def print_board(board):
    print("  " + "   ".join(map(str, range(COLS))))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(format_piece(piece) for piece in row) + " |")
        print("+" + "---+" * COLS)

def format_piece(piece):
    if piece == 'X':
        return Fore.RED + piece + Style.RESET_ALL
    elif piece == 'O':
        return Fore.BLUE + piece + Style.RESET_ALL
    else:
        return piece

def is_winner(board, player):
    # Check horizontal locations for win
    for c in range(COLS - CONNECT_N + 1):
        for r in range(ROWS):
            if all(board[r][c + i] == player for i in range(CONNECT_N)):
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - CONNECT_N + 1):
            if all(board[r + i][c] == player for i in range(CONNECT_N)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS - CONNECT_N + 1):
        for r in range(ROWS - CONNECT_N + 1):
            if all(board[r + i][c + i] == player for i in range(CONNECT_N)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - CONNECT_N + 1):
        for r in range(CONNECT_N - 1, ROWS):
            if all(board[r - i][c + i] == player for i in range(CONNECT_N)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def score_position(board, player):
    score = 0

    # Score horizontal
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLS)]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, player)

    # Score vertical
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    # Score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(CONNECT_N)]
            score += evaluate_window(window, player)

    # Score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+3-i][c+i] for i in range(CONNECT_N)]
            score += evaluate_window(window, player)

    return score

def evaluate_window(window, player):
    score = 0
    opponent = 'O' if player == 'X' else 'X'
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(player) == 2 and window.count(' ') == 2:
        score += 2
    if window.count(opponent) == 3 and window.count(' ') == 1:
        score -= 4
    return score

# def negamax(board, depth, alpha, beta, player):
#     opponent = 'O' if player == 'X' else 'X'
#     valid_locations = [c for c in range(COLS) if board[0][c] == ' ']
#     is_terminal = is_winner(board, player) or is_winner(board, opponent) or is_draw(board)

#     if depth == 0 or is_terminal:
#         if is_terminal:
#             if is_winner(board, player):
#                 return (None, 100000000000000)
#             elif is_winner(board, opponent):
#                 return (None, -10000000000000)
#             else:  # Game is over, no more valid moves
#                 return (None, 0)
#         else:  # Depth is zero
#             return (None, score_position(board, player))

#     value = -math.inf
#     column = valid_locations[0]
#     for col in valid_locations:
#         row = next(r for r in range(ROWS - 1, -1, -1) if board[r][col] == ' ')
#         board[row][col] = player
#         new_score = -negamax(board, depth - 1, -beta, -alpha, opponent)[1]
#         board[row][col] = ' '
#         if new_score > value:
#             value = new_score
#             column = col
#         alpha = max(alpha, value)
#         if alpha >= beta:
#             break

#     return column, value

def negamax(board, depth, alpha, beta, player):
    opponent = 'O' if player == 'X' else 'X'
    valid_locations = [c for c in range(COLS) if board[0][c] == ' ']

    # Reorder valid_locations to prioritize the middle column and alternate outward
    middle = COLS // 2
    reordered_locations = [middle] + [middle + i for i in range(1, middle + 1)] + [middle - i for i in range(1, middle + 1)]
    valid_locations = [col for col in reordered_locations if col in valid_locations]

    is_terminal = is_winner(board, player) or is_winner(board, opponent) or is_draw(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winner(board, player):
                return (None, 100000000000000)
            elif is_winner(board, opponent):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, player))

    value = -math.inf
    column = valid_locations[0]
    for col in valid_locations:
        row = next(r for r in range(ROWS - 1, -1, -1) if board[r][col] == ' ')
        board[row][col] = player
        new_score = -negamax(board, depth - 1, -beta, -alpha, opponent)[1]
        board[row][col] = ' '
        if new_score > value:
            value = new_score
            column = col
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return column, value


def best_move(board, player, depth):
    column, _ = negamax(board, depth, -math.inf, math.inf, player)
    return column

def play_game():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    player = input("Please choose your gamepiece, X to go first, O to go second (X/O): ").upper()
    current_player = 'X'
    max_depth = 5

    while True:
        print_board(board)
        if is_winner(board, 'X'):
            print("X wins!")
            break
        if is_winner(board, 'O'):
            print("O wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        if current_player == player:
            move = int(input("Enter your move (column number): "))
            if board[0][move] == ' ':
                row = next(r for r in range(ROWS - 1, -1, -1) if board[r][move] == ' ')
                board[row][move] = current_player
                current_player = 'O' if current_player == 'X' else 'X'
            else:
                print("Invalid move. Try again.")
        else:
            start_time = time.time()
            move = best_move(board, current_player, max_depth)
            end_time = time.time()
            if move is not None:
                row = next(r for r in range(ROWS - 1, -1, -1) if board[r][move] == ' ')
                board[row][move] = current_player
                current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()

