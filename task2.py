# TIC-TAC-TOE AI



#!/usr/bin/env python3
"""
tictactoe_ai.py
A console Tic-Tac-Toe game where a human plays against an
unbeatable AI (Minimax + Alpha-Beta pruning).

Run:
    python tictactoe_ai.py
"""

import math
from typing import List, Tuple, Optional

# ------------------------------------------------------------
# Board representation
# ------------------------------------------------------------
Board = List[List[str]]
HUMAN, AI = "X", "O"
EMPTY = " "

def create_board() -> Board:
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def print_board(board: Board) -> None:
    print("\n")
    for row in board:
        print(" | ".join(cell if cell != EMPTY else " " for cell in row))
        print("-" * 9)

# ------------------------------------------------------------
# Game rules
# ------------------------------------------------------------
def winner(board: Board) -> Optional[str]:
    """Return 'X' or 'O' if someone has won, else None."""
    lines = (
        board[:] +  # rows
        [list(col) for col in zip(*board)] +  # columns
        [[board[i][i] for i in range(3)],     # main diag
         [board[i][2 - i] for i in range(3)]] # anti-diag
    )
    for line in lines:
        if line[0] == line[1] == line[2] != EMPTY:
            return line[0]
    return None

def is_full(board: Board) -> bool:
    return all(cell != EMPTY for row in board for cell in row)

def available_moves(board: Board) -> List[Tuple[int, int]]:
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

# ------------------------------------------------------------
# Minimax with Alpha-Beta
# ------------------------------------------------------------
def minimax(board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
    win = winner(board)
    if win == AI:
        return 10 - depth, None
    if win == HUMAN:
        return depth - 10, None
    if is_full(board):
        return 0, None

    best_move = None

    if maximizing:  # AI turn
        max_eval = -math.inf
        for move in available_moves(board):
            r, c = move
            board[r][c] = AI
            eval_score, _ = minimax(board, depth + 1, alpha, beta, False)
            board[r][c] = EMPTY
            if eval_score > max_eval:
                max_eval, best_move = eval_score, move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:  # Human turn
        min_eval = math.inf
        for move in available_moves(board):
            r, c = move
            board[r][c] = HUMAN
            eval_score, _ = minimax(board, depth + 1, alpha, beta, True)
            board[r][c] = EMPTY
            if eval_score < min_eval:
                min_eval, best_move = eval_score, move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def best_move(board: Board) -> Tuple[int, int]:
    _, move = minimax(board, 0, -math.inf, math.inf, True)
    if move is None:
        raise ValueError("Board already finished")
    return move

# ------------------------------------------------------------
# Human input
# ------------------------------------------------------------
def ask_human_move(board: Board) -> Tuple[int, int]:
    while True:
        try:
            raw = input("Your move (row col): ")
            r, c = map(int, raw.strip().split())
            if r not in (0, 1, 2) or c not in (0, 1, 2):
                raise ValueError
            if board[r][c] != EMPTY:
                print("Cell already taken. Try again.")
                continue
            return r, c
        except ValueError:
            print("Please enter two integers 0-2 separated by space, e.g. 1 2")

# ------------------------------------------------------------
# Main game loop
# ------------------------------------------------------------
def play():
    board = create_board()
    print("\n=== Tic-Tac-Toe ===")
    print("You are X, AI is O.")
    print("Enter moves as row col, e.g. 0 2 for top-right.\n")

    current_player = HUMAN  # Human starts; change to AI if desired
    while True:
        print_board(board)
        win = winner(board)
        if win:
            print(f"{win} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        if current_player == HUMAN:
            r, c = ask_human_move(board)
            board[r][c] = HUMAN
            current_player = AI
        else:
            print("AI is thinking...")
            r, c = best_move(board)
            board[r][c] = AI
            print(f"AI plays {r} {c}")
            current_player = HUMAN

if __name__ == "__main__":
    play()