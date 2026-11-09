"""
================================================================================
ASSIGNMENT No. 2 - Tic-Tac-Toe 
================================================================================
Name:     SHREEYA S TAPASWI
Roll No:  31474
Batch:    N4
--------------------------------------------------------------------------------
Problem Statement: Design an intelligent agent to play a game (e.g. Tic-Tac-Toe)
using MINMAX with Alpha-Beta Pruning to make optimal decisions.
================================================================================
"""
import math
import tkinter as tk
from tkinter import messagebox

# Global game state array
board = [' ' for _ in range(9)]

# --- Core AI Logic Block ---

def check_winner(player):
    """Checks if the specified player has won the game."""
    wins = [(0,1,2),(3,4,5),(6,7,8), # Rows
            (0,3,6),(1,4,7),(2,5,8), # Columns
            (0,4,8),(2,4,6)]         # Diagonals
    return any(board[a] == board[b] == board[c] == player for a, b, c in wins)

def is_full():
    """Returns True if there are no empty spaces left on the board."""
    return ' ' not in board

def minimax(is_max, alpha, beta):
    """Core Minimax algorithm combined with Alpha-Beta Pruning."""
    if check_winner('X'):  # AI wins
        return 1
    if check_winner('O'):  # Human wins
        return -1
    if is_full():          # Draw state
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(False, alpha, beta)
                board[i] = ' '
                best = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(True, alpha, beta)
                board[i] = ' '
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

def find_best_move():
    """Finds the ultimate optimal index for the AI move."""
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(False, -math.inf, math.inf)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# --- Modern Cyberpunk Color Palette ---
BG_MAIN      = "#0B0813"  # Deep black with a dark purple tint
BG_CARD      = "#141026"  # Rich purple-infused container background
BORDER_CARD  = "#31255C"  # Neon purple thin accent framing boundary
COLOR_TILE   = "#1D1836"  # Unclicked game tile base color
COLOR_HOVER  = "#2C2452"  # Hover state color highlight
COLOR_X      = "#38BDF8"  # Electric Ocean Blue for AI (X)
COLOR_O      = "#F87171"  # Vibrant Coral Red for Human (O)
TEXT_WHITE   = "#F3F4F6"  # Clean title white
TEXT_MUTED   = "#A78BFA"  # Soft pastel purple for secondary metadata

# --- Modern UI Dynamic Custom Components ---

class RoundedTile(tk.Canvas):
    """Custom canvas component mimicking a rounded card tile to look modern on Linux."""
    def __init__(self, master, index, **kwargs):
        super().__init__(master, width=90, height=90, bg=BG_MAIN, highlightthickness=0, cursor="hand2", **kwargs)
        self.index = index
        self.state = "normal"
        self.draw_tile(COLOR_TILE)
        
        # UI Event triggers
        self.bind("<Button-1>", lambda e: self.on_click())
        self.bind("<Enter>", lambda e: self.on_hover(True))
        self.bind("<Leave>", lambda e: self.on_hover(False))

    def draw_tile(self, color):
        """Draws the clean round-corner box structure inside canvas."""
        self.delete("all")
        r = 16  # Corner rounding diameter radius pixel strength
        w, h = 90, 90
        # Multi-point coordinate tracking vector generating smooth rounded edges
        points = [r, 0, w-r, 0, w, 0, w, r, w, h-r, w, h, w-r, h, r, h, 0, h, 0, h-r, 0, r, 0, 0]
        self.create_polygon(points, smooth=True, fill=color, outline=BORDER_CARD, width=1)

    def on_hover(self, entering):
        """Applies smooth backdrop transition upon user pointer intersection."""
        if self.state == "normal":
            self.draw_tile(COLOR_HOVER if entering else COLOR_TILE)

    def on_click(self):
        """Processes execution phase maps following direct user grid interaction."""
        global board
        if self.state == "normal" and board[self.index] == ' ' and not check_winner('X') and not check_winner('O'):
            # 1. Player Turn ('O')
            self.state = "disabled"
            board[self.index] = 'O'
            self.draw_tile(BG_MAIN)
            self.create_text(45, 45, text="O", font=('Segoe UI', 32, 'bold'), fill=COLOR_O)
            
            if game_over_check():
                return
                
            # 2. AI Computational State Engine Activation
            status_label.config(text="AI Thinking...", fg=COLOR_X)
            root.update()
            
            ai_idx = find_best_move()
            if ai_idx != -1:
                board[ai_idx] = 'X'
                tiles[ai_idx].state = "disabled"
                tiles[ai_idx].draw_tile(BG_MAIN)
                tiles[ai_idx].create_text(45, 45, text="X", font=('Segoe UI', 32, 'bold'), fill=COLOR_X)
                
            status_label.config(text="Your Turn (O)", fg=COLOR_O)
            game_over_check()


def game_over_check():
    """Checks game end status, modifies indicators, and spawns message alerts."""
    if check_winner('O'):
        status_label.config(text="Victory! You Won!", fg="#34D399") 
        messagebox.showinfo("Match Result", "Congratulations! You won.")
        disable_all_tiles()
        return True
    elif check_winner('X'):
        status_label.config(text="AI Won (Optimal Decision)", fg=COLOR_X)
        messagebox.showerror("Match Result", "AI Wins! The Minimax Agent made perfect strategic choices.")
        disable_all_tiles()
        return True
    elif is_full():
        status_label.config(text="Draw! Perfect Tactics.", fg=TEXT_MUTED)
        messagebox.showinfo("Match Result", "It's a tie game! Strategic stand-off.")
        disable_all_tiles()
        return True
    return False

def disable_all_tiles():
    """Locks up remaining interactive nodes upon session close."""
    for tile in tiles:
        tile.state = "disabled"

def reset_game():
    """Flushes active arrays, resets counters, and draws fresh canvas sheets."""
    global board
    board = [' ' for _ in range(9)]
    status_label.config(text="Your Turn (O)", fg=COLOR_O)
    for tile in tiles:
        tile.state = "normal"
        tile.draw_tile(COLOR_TILE)


# --- UI Window Framework Setup Geometry ---

root = tk.Tk()
root.title("Assignment 2: AI Tic-Tac-Toe Agent")
root.geometry("420x590")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# Clean, Card-Style Header Area with Purple Accent
header_frame = tk.Frame(root, bg=BG_CARD, pady=14, highlightbackground=BORDER_CARD, highlightthickness=1)
header_frame.pack(fill='x', padx=20, pady=(20, 5))

# Primary Required Header Refactoring 
main_title = tk.Label(header_frame, text="AI Tic-Tac-Toe Agent", font=('Segoe UI', 16, 'bold'), fg=TEXT_WHITE, bg=BG_CARD)
main_title.pack()

# Clean structural hierarchy matching requirement lines
info_subheader = "Shreeya Tapaswi  •  Roll No: 31474  •  Batch: N4"
sub_title = tk.Label(header_frame, text=info_subheader, font=('Segoe UI', 9, 'bold'), fg=TEXT_MUTED, bg=BG_CARD)
sub_title.pack(pady=(6, 0))

# Dynamic Interactive State Progress Monitor Strip
status_label = tk.Label(root, text="Your Turn (O)", font=('Segoe UI', 12, 'bold'), fg=COLOR_O, bg=BG_MAIN, pady=12)
status_label.pack()

# Embedded layout grid container housing modern tile structures
grid_frame = tk.Frame(root, bg=BG_MAIN)
grid_frame.pack(pady=5)

tiles = []
for r in range(3):
    for c in range(3):
        idx = r * 3 + c
        tile = RoundedTile(grid_frame, index=idx)
        tile.grid(row=r, column=c, padx=6, pady=6)
        tiles.append(tile)

# Custom stylized action button layout block
footer_frame = tk.Frame(root, bg=BG_MAIN, pady=18)
footer_frame.pack()

reset_btn = tk.Button(footer_frame, text="RESTART ENCOUNTER", font=('Segoe UI', 10, 'bold'), bg="#6D28D9", fg=TEXT_WHITE, 
                      activebackground="#5B21B6", activeforeground=TEXT_WHITE, padx=30, pady=9, bd=0, relief='flat', cursor='hand2')
reset_btn.config(command=reset_game)
reset_btn.pack()

# Execute application tree structure runtime instance lifecycle
if __name__ == "__main__":
    root.mainloop()
