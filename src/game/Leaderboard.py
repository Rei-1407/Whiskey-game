import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

class Leaderboard(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Leaderboard")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Center the window
        self.center_window()

        # Create text area with scrollbar
        self.leaderboard_area = scrolledtext.ScrolledText(self, font=('Monospace', 12), state='disabled')
        self.leaderboard_area.pack(expand=True, fill='both', padx=10, pady=10)

        # Load and display scores
        self.load_scores()

    def center_window(self):
        """Centers the leaderboard window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        self.geometry(f"400x300+{x}+{y}")

    def load_scores(self):
        """Loads and displays scores from the leaderboard file."""
        scores = []
        file_path = "leaderboard.txt"
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as reader:
                    for line in reader:
                        if " - " in line:  # Ensure valid format
                            scores.append(line.strip())

                # Sort scores in descending order by score value
                scores.sort(key=self.sort_key, reverse=True)

            self.display_leaderboard(scores)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            messagebox.showerror("Error", "Cannot load leaderboard.")

    @staticmethod
    def sort_key(score_line):
        """Extracts the score value for sorting."""
        try:
            return int(score_line.split(" - ")[1].split(":")[1].strip())
        except (IndexError, ValueError):
            return 0

    def display_leaderboard(self, scores):
        """Displays the scores in the leaderboard area."""
        self.leaderboard_area.configure(state='normal')
        self.leaderboard_area.delete('1.0', tk.END)

        if scores:
            for rank, score in enumerate(scores, start=1):
                self.leaderboard_area.insert(tk.END, f"{rank}. {score}\n")
        else:
            self.leaderboard_area.insert(tk.END, "No scores available. Play a game to add your score!\n")

        self.leaderboard_area.configure(state='disabled')

    def save_score(self, score, player_name, player_code):
        """Saves a new score to the leaderboard file."""
        file_path = "leaderboard.txt"
        try:
            with open(file_path, "a") as writer:
                writer.write(f"{player_name} (ID: {player_code}) - Score: {score}\n")
        except Exception as e:
            print(f"Error saving score: {e}")
            messagebox.showerror("Error", "Cannot save the score.")

    def close_window(self):
        """Closes the leaderboard window."""
        self.destroy()

# Example usage (if standalone):
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide root window
    leaderboard = Leaderboard()
    leaderboard.mainloop()
