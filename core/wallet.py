import os

class Wallet:
    def __init__(self, starting_money=1000):
        self.start_money = starting_money
        self.file_name = "wallet.txt"
        self.balance = self.load()

    def load(self): 
        """wczytuje stan konta z pliku lub ustawia na STARTING_MONEY jeśli plik nie istnieje lub jest nieprawidłowy."""
        if self.file_name is None:
            return self.start_money
        
        try:
            with open(self.file_name, "r") as f:
                data = f.read().strip()
                amount = float(data)
                
                if amount <= 0:
                    return self.start_money
                return amount
        except:
            return self.start_money

    def save(self):
        """Zapisuje aktualny stan konta do pliku."""
        try:
            with open(self.file_name, "w") as f:
                f.write(str(self.balance))
        except Exception as e:
            print(f"Błąd zapisu: {e}")

    def change(self, amount):
        """Zmienia stan konta i od razu zapisuje."""
        self.balance += amount
        self.save()