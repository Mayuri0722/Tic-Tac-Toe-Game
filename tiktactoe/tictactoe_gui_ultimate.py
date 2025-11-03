import tkinter as tk
from tkinter import messagebox
import json
import os

PLAYER = 'X'
AI = 'O'
EMPTY = ''
SCORE_FILE = 'tictactoe_scores.json'

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.theme = 'light'
        self.init_player_screen()

    def init_player_screen(self):
        self.clear_root()
        self.root.geometry("400x300")
        self.root.configure(bg='#fefefe')

        self.fade_in(self.root)

        tk.Label(self.root, text="Enter Player Name", font=("Arial", 16), bg="#fefefe", fg="#444").pack(pady=20)
        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=10)
        tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 12),
                  bg="#4da6ff", fg="white", padx=10, pady=5).pack(pady=20)

    def start_game(self):
        self.player_name = self.name_entry.get() or "Player"
        self.score = {'X': 0, 'O': 0}
        self.board = [[EMPTY]*3 for _ in range(3)]
        self.turn = PLAYER
        self.build_game_ui()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_game_ui(self):
        self.clear_root()
        self.root.update_idletasks()
        width = min(self.root.winfo_screenwidth() - 100, 700)
        height = min(self.root.winfo_screenheight() - 100, 700)
        self.root.geometry(f"{width}x{height}")

        self.colors = self.get_theme_colors()

        self.root.configure(bg=self.colors["bg"])
        self.board_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.board_frame.pack(expand=True)

        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.board_frame, text='', font=('Arial', 32),
                                width=4, height=2, bg=self.colors["btn_bg"],
                                fg=self.colors["fg"], activebackground=self.colors["btn_hover"],
                                command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                self.buttons[i][j] = btn

        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        self.status = tk.Label(self.root, text=f"{self.player_name}'s Turn (X)",
                               bg=self.colors["bg"], fg=self.colors["fg"], font=("Arial", 14))
        self.status.pack(pady=10)

        self.score_label = tk.Label(self.root, text=self.get_score_text(),
                                    bg=self.colors["bg"], fg=self.colors["fg"], font=("Arial", 12))
        self.score_label.pack()

        control_frame = tk.Frame(self.root, bg=self.colors["bg"])
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Reset", font=("Arial", 12), bg="#81c784", fg="white",
                  padx=10, command=self.reset_game).pack(side=tk.LEFT, padx=10)

        tk.Button(control_frame, text="Quit", font=("Arial", 12), bg="#e57373", fg="white",
                  padx=10, command=self.root.quit).pack(side=tk.LEFT, padx=10)

        tk.Button(control_frame, text="Toggle Theme", font=("Arial", 12), bg="#4fc3f7", fg="white",
                  command=self.toggle_theme).pack(side=tk.LEFT, padx=10)

    def get_theme_colors(self):
        if self.theme == 'light':
            return {
                "bg": "#fdfdfd",
                "fg": "#2c2c2c",
                "btn_bg": "#e8f5e9",
                "btn_hover": "#c8e6c9",
                "x_color": "#1e88e5",
                "o_color": "#d81b60"
            }
        else:
            return {
                "bg": "#2e2e2e",
                "fg": "#f0f0f0",
                "btn_bg": "#424242",
                "btn_hover": "#616161",
                "x_color": "#42a5f5",
                "o_color": "#ef5350"
            }

    def toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.build_game_ui()

    def get_score_text(self):
        return f"Score - {self.player_name} (X): {self.score['X']} | AI (O): {self.score['O']}"

    def on_click(self, row, col):
        if self.board[row][col] == EMPTY and self.turn == PLAYER:
            self.make_move(row, col, PLAYER)
            if not self.check_game_over():
                self.turn = AI
                self.status.config(text="AI's Turn (O)")
                self.root.after(300, self.ai_move)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        btn = self.buttons[row][col]
        btn.config(text=player,
                   fg=self.colors["x_color"] if player == 'X' else self.colors["o_color"])
        btn.config(state='disabled')

    def ai_move(self):
        best_score = float('-inf')
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = AI
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        if move:
            self.make_move(move[0], move[1], AI)
            if not self.check_game_over():
                self.turn = PLAYER
                self.status.config(text=f"{self.player_name}'s Turn (X)")

    def minimax(self, board, depth, is_maximizing):
        result = self.check_winner()
        if result == PLAYER:
            return -10
        elif result == AI:
            return 10
        elif self.is_draw():
            return 0

        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = AI
                        best = max(best, self.minimax(board, depth + 1, False))
                        board[i][j] = EMPTY
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER
                        best = min(best, self.minimax(board, depth + 1, True))
                        board[i][j] = EMPTY
            return best

    def check_winner(self):
        lines = self.get_lines()
        for line in lines:
            values = [self.board[r][c] for r, c in line]
            if values.count(values[0]) == 3 and values[0] != EMPTY:
                return values[0]
        return None

    def is_draw(self):
        return all(self.board[i][j] != EMPTY for i in range(3) for j in range(3))

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            self.score[winner] += 1
            self.show_popup(f"{self.player_name if winner == 'X' else 'AI'} Wins!")
            return True
        elif self.is_draw():
            self.show_popup("It's a Draw!")
            return True
        return False

    def show_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.geometry("300x200")
        popup.configure(bg=self.colors["bg"])
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 150
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - 100
        popup.geometry(f"+{x}+{y}")
        popup.grab_set()

        self.fade_in(popup)

        tk.Label(popup, text=message, font=("Arial", 16), bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=20)
        tk.Label(popup, text=self.get_score_text(), font=("Arial", 12), bg=self.colors["bg"], fg=self.colors["fg"]).pack()

        tk.Button(popup, text="Play Again", font=("Arial", 12),
                  bg="#4caf50", fg="white", command=lambda: [popup.destroy(), self.reset_game()]).pack(pady=10)

    def reset_game(self):
        self.board = [[EMPTY]*3 for _ in range(3)]
        self.turn = PLAYER
        self.build_game_ui()

    def get_lines(self):
        return [[(i, 0), (i, 1), (i, 2)] for i in range(3)] + \
               [[(0, i), (1, i), (2, i)] for i in range(3)] + \
               [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    def fade_in(self, window):
        for i in range(0, 11):
            window.attributes('-alpha', i * 0.1)
            window.update()
            window.after(30)

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()

