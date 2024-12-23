import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import random

class RaffleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raffle App")

        # Label para o título da aplicação / Label for application title
        self.label = tk.Label(root, text="Raffle Application", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Botão para carregar o arquivo CSV / Button to load the CSV file
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=5)

        # Botão para sortear / Button to draw a winner
        self.raffle_button = tk.Button(root, text="Draw Winner", command=self.draw_winner, state=tk.DISABLED)
        self.raffle_button.pack(pady=5)

        # Label para mostrar o resultado / Label to display the result
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

        # Lista para armazenar os dados do arquivo e os sorteados / List to store data from the file and drawn entries
        self.entries = []
        self.drawn_entries = set()

    def load_csv(self):
        # Abrir diálogo para selecionar arquivo CSV / Open dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if not file_path:
            return

        try:
            # Carregar o arquivo CSV usando pandas / Load CSV file using pandas
            df = pd.read_csv(file_path)

            # Verificar se o arquivo tem as colunas necessárias / Check if the file has the required columns
            if "Número" not in df.columns or "Nome" not in df.columns:
                messagebox.showerror("Error", "The file must contain 'Número' and 'Nome' columns!")
                return

            # Filtrar os dados necessários / Extract the necessary data
            self.entries = df[df["Nome"].notna()][["Número", "Nome"]].values.tolist()

            if not self.entries:
                messagebox.showerror("Error", "No valid entries found in the file!")
                return

            self.raffle_button.config(state=tk.NORMAL)
            messagebox.showinfo("Success", "CSV file loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def draw_winner(self):
        if not self.entries:
            messagebox.showerror("Error", "No entries to draw from!")
            return

        # Sortear um vencedor aleatoriamente sem repetir / Randomly draw a winner without repetition
        available_entries = [entry for entry in self.entries if entry[0] not in self.drawn_entries]

        if not available_entries:
            self.result_label.config(text="All entries have been drawn!")
            return

        winner = random.choice(available_entries)
        raffle_number, name = winner

        # Adicionar o número sorteado ao conjunto / Add the drawn number to the set
        self.drawn_entries.add(raffle_number)

        # Mostrar o resultado / Display the result
        if name.strip():
            self.result_label.config(text=f"Winner: {name} (Raffle Number: {raffle_number})")
        else:
            self.result_label.config(text=f"Empty entry drawn (Raffle Number: {raffle_number})")

if __name__ == "__main__":
    root = tk.Tk()
    app = RaffleApp(root)
    root.mainloop()
