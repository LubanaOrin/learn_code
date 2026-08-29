# Chess Capture Analyzer

## Project Overview

Chess Capture Analyzer is a Python command-line program that evaluates a user-defined chess board and identifies which black pieces can be captured by a selected white piece.

The project demonstrates practical Python fundamentals: functions, dictionaries, lists, input validation, control flow, and modular rule-based logic.

## Files

- `chess_capture_analyzer.py` - final cleaned Python script
- `tests/test_chess_capture_analyzer.py` - focused tests for validation and capture rules

## How It Works

1. The user enters one white chess piece and its position.
2. The user enters one to sixteen black pieces and their positions.
3. The user types `done` after adding at least one black piece.
4. The program returns the black pieces the white piece can capture.

Supported pieces:

- pawn
- knight
- bishop
- rook
- queen
- king

Positions use standard chess coordinates such as `a1`, `e4`, or `h8`.

## Example

Input:

```text
Enter white piece and position: rook e4
Enter black piece and position (or 'done'): pawn h4
Enter black piece and position (or 'done'): bishop e8
Enter black piece and position (or 'done'): done
```

Output:

```text
Capturable black pieces:
e8 bishop
h4 pawn
```

## Key Features

- Validates chess piece names and board coordinates
- Prevents multiple pieces from occupying the same square
- Supports up to sixteen black pieces
- Implements capture logic for all six standard chess pieces
- Includes a Unicode chessboard display helper for visual inspection
- Keeps the command-line workflow simple and beginner-friendly

## How to Run

```bash
python3 chess_capture_analyzer.py
```

## How to Test

From this project folder:

```bash
python3 -m unittest discover -s tests
```
