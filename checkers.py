from copy import deepcopy
import math

EMPTY = 0
WHITE_PAWN = 1
WHITE_KING = 2
BLACK_PAWN = -1
BLACK_KING = -2


def initialize_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = BLACK_PAWN

    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = WHITE_PAWN

    return board


def get_possible_moves(board, player):
    moves = []
    for row in range(8):
        for col in range(8):
            if player == "white":
                if board[row][col] not in [WHITE_PAWN, WHITE_KING]:
                    continue
            elif player == "black":
                if board[row][col] not in [BLACK_PAWN, BLACK_KING]:
                    continue
            moves.extend(get_piece_moves(board, row, col))
    return moves


def get_piece_moves(board, row, col):
    piece = board[row][col]
    if piece in [WHITE_PAWN, BLACK_PAWN]:
        return get_pawn_moves(board, row, col)
    else:
        return get_king_moves(board, row, col)




def get_pawn_moves(board, row, col):
    moves = []
    directions = [(-1, -1), (-1, 1)] if board[row][col] == WHITE_PAWN else [(1, -1), (1, 1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == EMPTY:
            moves.append(((row, col), (new_row, new_col)))
        else:
            jump_row, jump_col = new_row + dr, new_col + dc
            if not (0 <= jump_row < 8 and 0 <= jump_col < 8):
                continue

            if board[new_row][new_col] * board[row][col] > 0:
                continue

            if board[jump_row][jump_col] != EMPTY:
                continue
            moves.append(((row, col), (jump_row, jump_col)))

    return moves


def get_king_moves(board, row, col):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == EMPTY:
            moves.append(((row, col), (new_row, new_col)))
        else:
            jump_row, jump_col = new_row + dr, new_col + dc
            if not (0 <= jump_row < 8 and 0 <= jump_col < 8):
                continue

            if board[new_row][new_col] * board[row][col] > 0:
                continue

            if board[jump_row][jump_col] != EMPTY:
                continue
            moves.append(((row, col), (jump_row, jump_col)))

    return moves




def minimax(board, depth, alpha, beta, maximizing_player):
    board = deepcopy(board)
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)
    game_over = is_game_over(board)
    if game_over != 0:
        return game_over

    if maximizing_player:
        max_eval = -math.inf
        for move in get_possible_moves(board, "white"):
            new_board = make_move(board, move)
            if is_capturing_move(move):
                # Explore all possible further captures
                additional_captures = get_possible_captures(new_board, move[1])  # Move[1] is the end position of the current piece
                if additional_captures:
                    for capture in additional_captures:
                        further_board = make_move(new_board, capture)
                        eval = minimax(further_board, depth, alpha, beta, True)  # Continue with the same depth
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if max_eval >= beta:
                            break
                else:
                    eval = minimax(new_board, depth - 1, alpha, beta, False)
            else:
                eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if max_eval >= beta:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_possible_moves(board, "black"):
            new_board = make_move(board, move)
            if is_capturing_move(move):
                # Explore all possible further captures
                additional_captures = get_possible_captures(new_board, move[1])  # Move[1] is the end position of the current piece
                if additional_captures:
                    for capture in additional_captures:
                        further_board = make_move(new_board, capture)
                        eval = minimax(further_board, depth, alpha, beta, False)  # Continue with the same depth
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if min_eval <= alpha:
                            break
                else:
                    eval = minimax(new_board, depth - 1, alpha, beta, True)
            else:
                eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if min_eval <= alpha:
                break
        return min_eval


def is_capturing_move(move):
    (x0,y0), (x1,y2) = move
    return abs(x1-x0) == 2


def get_possible_captures(board, piece_pos):
    moves = get_piece_moves(board, *piece_pos)
    capturing_moves = []
    for move in moves:
        if is_capturing_move(move):
            capturing_moves.append(move)
    return capturing_moves


def select_best_move(board, depth, player):
    board = deepcopy(board)
    best_move = None
    best_eval = float('-inf') if player == "white" else float('inf')
    for move in get_possible_moves(board, player):
        new_board = make_move(board, move)
        move_value = minimax(new_board, depth - 1, -math.inf, math.inf, player == "white")
        if (player == "white" and move_value > best_eval) or (player == "black" and move_value < best_eval):
            best_eval = move_value
            best_move = move
    return best_move

def select_best_capturing_move(board, depth, player, pos):
    board = deepcopy(board)
    best_move = None
    best_eval = float('-inf') if player == "white" else float('inf')
    for move in get_possible_captures(board, pos):
        new_board = make_move(board, move)
        move_value = minimax(new_board, depth - 1, -math.inf, math.inf, player == "white")
        if (player == "white" and move_value > best_eval) or (player == "black" and move_value < best_eval):
            best_eval = move_value
            best_move = move
    return best_move


def is_game_over(board):
    white_moves = black_moves = 0

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in [WHITE_PAWN, WHITE_KING]:
                white_moves += len(get_piece_moves(board, row, col))
            elif piece in [BLACK_PAWN, BLACK_KING]:
                black_moves += len(get_piece_moves(board, row, col))

    if white_moves == 0:
        return -100  # Black wins
    elif black_moves == 0:
        return 100  # White wins
    else:
        return 0  # Game is not over



def evaluate_board(board):
    score = 0

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            score += piece
            # if piece == WHITE_PAWN:
            #     score += 1
            # elif piece == WHITE_KING:
            #     score += 3
            # elif piece == BLACK_PAWN:
            #     score -= 1
            # elif piece == BLACK_KING:
            #     score -= 3

    return score



def make_move(board, move):
    (start_row, start_col), (end_row, end_col) = move
    piece = board[start_row][start_col]
    board[end_row][end_col] = piece
    board[start_row][start_col] = EMPTY

    if abs(end_row - start_row) == 2:
        capture_row = (start_row + end_row) // 2
        capture_col = (start_col + end_col) // 2
        board[capture_row][capture_col] = EMPTY

    if end_row == 0 and piece == WHITE_PAWN:
        board[end_row][end_col] = WHITE_KING
    elif end_row == 7 and piece == BLACK_PAWN:
        board[end_row][end_col] = BLACK_KING

    return board






def play_checkers():
    board = initialize_board()
    current_player = "white"

    while not is_game_over(board):
        print_board(board)

        if current_player == "white":
            print("White AI is thinking...")
            move = select_best_move(board, 2, "white")
            if move:
                board = make_move(board, move)
            current_player = "black"
        else:
            print("Black player's turn")
            move = get_human_move(board, "black")
            if move:
                board = make_move(board, move)
            current_player = "white"

def get_human_move(board, player):
    while True:
        try:
            start_pos = input("Enter the start position (row,col): ")
            end_pos = input("Enter the end position (row,col): ")
            start_row, start_col = map(int, start_pos.split(','))
            end_row, end_col = map(int, end_pos.split(','))

            move = ((start_row, start_col), (end_row, end_col))
            print(get_possible_moves(board, player))

            if move in get_possible_moves(board, player):
                return move
            else:
                print("Invalid move. Please try again.")
        except ValueError:
            print("Invalid input. Please enter the position like: '2,3'.")


def print_board(board):
    piece_symbols = {
        EMPTY: ".",
        WHITE_PAWN: "w",
        WHITE_KING: "W",
        BLACK_PAWN: "b",
        BLACK_KING: "B"
    }

    for row in range(8):
        print(" ".join(piece_symbols[piece] for piece in board[row]))
    print()

if __name__ == "__main__":
    play_checkers()