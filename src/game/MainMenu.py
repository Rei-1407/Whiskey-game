import tkinter as tk
from tkinter import messagebox
from Leaderboard import Leaderboard
from GamePanel import GamePanel


class MainMenu(tk.Tk):
    player_name = None
    player_code = None

    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("400x300")
        self.eval('tk::PlaceWindow . center')

        panel = tk.Frame(self)
        panel.pack(expand=True)

        # Buttons for Play, Leaderboard, and Exit
        self.play_button = tk.Button(panel, text="Play", command=self.play_game)
        self.leaderboard_button = tk.Button(panel, text="Leaderboard", command=self.show_leaderboard)
        self.exit_button = tk.Button(panel, text="Exit", command=self.exit_program)

        self.play_button.pack(side=tk.LEFT, padx=5)
        self.leaderboard_button.pack(side=tk.LEFT, padx=5)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def play_game(self):
        self.withdraw()  # Hide the main menu
        game_panel = GamePanel(self)  # Pass MainMenu instance to GamePanel
        game_panel.start_game()

    def show_leaderboard(self):
        # Create and display the leaderboard window
        leaderboard = Leaderboard()
        leaderboard.deiconify()

    def exit_program(self):
        # Exit the program
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

    @staticmethod
    def check_name(name):
        return all(c.isalpha() or c.isspace() for c in name)


def main():
    def validate_and_create():
        name = name_field.get().strip()
        code = code_field.get().strip()

        if MainMenu.check_name(name) and name and code:
            dialog.destroy()
            MainMenu.player_name = name
            MainMenu.player_code = code

            # Create and display MainMenu
            main_menu = MainMenu()
            main_menu.mainloop()
        else:
            messagebox.showwarning("Error", "Please enter valid and complete information.")

    # Dialog for player input
    dialog = tk.Tk()
    dialog.title("Enter Player Information")
    dialog.geometry("300x150")
    dialog.eval('tk::PlaceWindow . center')

    frame = tk.Frame(dialog)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Player Name:").grid(row=0, column=0, sticky='e', pady=5)
    name_field = tk.Entry(frame)
    name_field.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Player ID:").grid(row=1, column=0, sticky='e', pady=5)
    code_field = tk.Entry(frame)
    code_field.grid(row=1, column=1, pady=5)

    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="OK", command=validate_and_create).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    dialog.mainloop()


if __name__ == "__main__":
    main()
