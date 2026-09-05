from typing import Optional
# CONSTANTS

VALID_PIECES = ["pawn", "knight", "bishop", "rook", "queen", "king"]
MAX_BLACK_PIECES = 16

# VALIDATION FUNCTIONS

def is_valid_piece(piece: str) -> bool:
    return piece in VALID_PIECES

def is_valid_position(position: str) -> bool:
    return len(position) == 2 and position[0] in "abcdefgh" and position[1] in "12345678"

def parse_piece_input(input_str: str) -> Optional[tuple[str, str]]:
    input_str = input_str.lower()
    parts = input_str.split()
    if len(parts) != 2:
        return None
    piece, position = parts
    if is_valid_piece(piece) and is_valid_position(position):
        return (piece, position)
    return None

# BOARD MANAGEMENT

def add_piece(board: dict[str, str], piece: str, position: str) -> bool:
    if not is_valid_position(position):
        return False
    if position in board:
        return False
    board[position] = piece
    return True

def get_chess_piece_symbol(piece: str, color: str) -> str:
    symbols = {
        "king": {"white": " ♔ ", "black": " ♚ "},
        "queen": {"white": " ♕ ", "black": " ♛ "},
        "rook": {"white": " ♖ ", "black": " ♜ "},
        "bishop": {"white": " ♗ ", "black": " ♝ "},
        "knight": {"white": " ♘ ", "black": " ♞ "},
        "pawn": {"white": " ♙ ", "black": " ♟ "},
    }

    if piece not in symbols:
        raise ValueError(f"Invalid piece name: {piece}")
    if color not in ["white", "black"]:
        raise ValueError(f"Invalid color: {color}")

    return symbols[piece][color]

def print_board(board: dict[str, str], white_position: str) -> None:
    print("    a   b   c   d   e   f   g   h")
    print("  +---+---+---+---+---+---+---+---+")

    for row in range(8, 0, -1):
        line = str(row) + " |"

        for col in "abcdefgh":
            pos = col + str(row)

            if pos in board:
                piece = board[pos]
                if pos == white_position:
                    symbol = get_chess_piece_symbol(piece, "white")
                else:
                    symbol = get_chess_piece_symbol(piece, "black")
            else:
                symbol = "   "

            line += symbol + "|"

        print(line)
        print("  +---+---+---+---+---+---+---+---+")

# CAPTURE LOGIC

def get_pawn_captures(position: str, board: dict[str, str]) -> list[str]:
    if not is_valid_position(position):
        return []
    if position not in board or board[position] != "pawn":
        return []

    col = position[0]
    row = int(position[1])
    # Note: Pawn promotion is not handled. If the pawn is on row 8,
    # forward_row becomes 9, which is outside the board.
    # is_valid_position prevents this from causing errors.

    captures = []

    left_col = chr(ord(col) - 1)
    right_col = chr(ord(col) + 1)
    forward_row = row + 1

    left_pos = left_col + str(forward_row)
    right_pos = right_col + str(forward_row)

    if is_valid_position(left_pos) and left_pos in board:
        captures.append(left_pos)

    if is_valid_position(right_pos) and right_pos in board:
        captures.append(right_pos)

    return captures

def get_rook_captures(position: str, board: dict[str, str]) -> list[str]:
    if not is_valid_position(position):
        return []

    if position not in board or board[position] != "rook":
        return []

    col = position[0]
    row = int(position[1])

    captures = []

    # UP
    for r in range(row + 1, 9):
        pos = col + str(r)
        if pos in board:
            captures.append(pos)
            break

    # DOWN
    for r in range(row - 1, 0, -1):
        pos = col + str(r)
        if pos in board:
            captures.append(pos)
            break

    # RIGHT
    for c in range(ord(col) + 1, ord('h') + 1):
        pos = chr(c) + str(row)
        if pos in board:
            captures.append(pos)
            break

    # LEFT
    for c in range(ord(col) - 1, ord('a') - 1, -1):
        pos = chr(c) + str(row)
        if pos in board:
            captures.append(pos)
            break

    return captures

def get_knight_captures(position: str, board: dict[str, str]) -> list[str]:
    if not is_valid_position(position):
        return []
    if position not in board or board[position] != "knight":
        return []

    col = position[0]
    row = int(position[1])

    moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    captures = []

    for dc, dr in moves:
        new_col = chr(ord(col) + dc)
        new_row = row + dr
        new_pos = new_col + str(new_row)

        if is_valid_position(new_pos) and new_pos in board:
            captures.append(new_pos)

    return captures

def get_bishop_captures(position: str, board: dict[str, str]) -> list[str]:
    if not is_valid_position(position):
        return []

    if position not in board or board[position] != "bishop":
        return []

    col = position[0]
    row = int(position[1])

    captures = []

    directions = [
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1)
    ]

    for dc, dr in directions:
        c = ord(col)
        r = row

        while True:
            c += dc
            r += dr
            new_pos = chr(c) + str(r)

            if not is_valid_position(new_pos):
                break

            if new_pos in board:
                captures.append(new_pos)
                break

    return captures

def get_queen_captures(position: str, board: dict[str, str]) -> list[str]:
    if not is_valid_position(position):
        return []

    if position not in board or board[position] != "queen":
        return []

    col = position[0]
    row = int(position[1])

    captures = []

    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]

    for dc, dr in directions:
        c = ord(col)
        r = row

        while True:
            c += dc
            r += dr
            new_pos = chr(c) + str(r)

            if not is_valid_position(new_pos):
                break

            if new_pos in board:
                captures.append(new_pos)
                break

    return captures

def get_king_captures(position: str, board: dict[str, str]) -> list[str]:
    if not is_valid_position(position):
        return []

    if position not in board or board[position] != "king":
        return []

    col = position[0]
    row = int(position[1])

    captures = []

    moves = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1),  (0, 1),  (1, 1)
    ]

    for dc, dr in moves:
        new_col = chr(ord(col) + dc)
        new_row = row + dr
        new_pos = new_col + str(new_row)

        if is_valid_position(new_pos) and new_pos in board:
            captures.append(new_pos)

    return captures

CAPTURE_FUNCTIONS = {
    "pawn": get_pawn_captures,
    "rook": get_rook_captures,
    "bishop": get_bishop_captures,
    "knight": get_knight_captures,
    "queen": get_queen_captures,
    "king": get_king_captures,
}

def get_capturable_pieces(board: dict[str, str], white_piece: str, white_position: str) -> list[str]:
    if not is_valid_piece(white_piece):
        return []

    if not is_valid_position(white_position):
        return []

    if white_position not in board or board[white_position] != white_piece:
        return []

    capture_function = CAPTURE_FUNCTIONS.get(white_piece)

    if capture_function:
        return capture_function(white_position, board)

    return []

# MAIN PROGRAM

def main() -> None:
    """
    Main function to handle user input, manage the board, and output capturable pieces.
    """
    board = {}

    while True:
        white_input = input("Enter white piece and position: ")
        parsed = parse_piece_input(white_input)

        if parsed is None:
            print("Invalid input. Please use format like 'rook e4'.")
            continue

        white_piece, white_position = parsed

        if add_piece(board, white_piece, white_position):
            print("White piece added successfully.")
            break
        else:
            print("Could not add white piece.")

    black_count = 0

    while black_count < MAX_BLACK_PIECES:
        black_input = input("Enter black piece and position (or 'done'): ")

        if black_input == "done":
            if black_count >= 1:
                break
            else:
                print("You must add at least one black piece before typing 'done'.")
                continue

        parsed = parse_piece_input(black_input)

        if parsed is None:
            print("Invalid input. Please use format like 'bishop d6'.")
            continue

        black_piece, black_position = parsed

        if add_piece(board, black_piece, black_position):
            black_count += 1
            print("Black piece added successfully.")
        else:
            print("Could not add black piece. Position may be invalid or occupied.")

    capturable = get_capturable_pieces(board, white_piece, white_position)

    if capturable:
        print("Capturable black pieces:")
        for pos in capturable:
            print(pos, board[pos])
    else:
        print("No black pieces can be captured.")

if __name__ == "__main__":
    main()