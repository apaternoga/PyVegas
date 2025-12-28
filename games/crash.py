import pygame
import random

# --- 1. KONFIGURACJA I KOLORY (Tymczasowe, docelowo z core/settings.py) ---
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
GRAY = (128, 128, 128)
YELLOW = (255, 215, 0)


class CrashGame :
    def __init__(self, screen) :
        self.screen = screen
        self.font_big = pygame.font.SysFont(None, 120)
        self.font_small = pygame.font.SysFont(None, 40)

        # Stan portfela (Tymczasowy, docelowo pobierany z globalnego gracza)
        self.balance = 1000
        self.current_bet = 0

        # Zmienne gry
        self.state = "BETTING"  # Opcje: BETTING, RUNNING, CRASHED, SUCCESS
        self.current_multiplier = 1.00
        self.target_crash = 1.00
        self.cashout_point = 0.0

        # Szybkość wzrostu (animacja)
        self.growth_speed = 0.01

    def _generate_crash_point(self) :
        """
        Generuje punkt Crash zgodnie z algorytmem Bustabit (Open Source).
        """
        house_edge = 0.01
        r = random.random()

        if r == 0 :
            r = 0.0000001  # Zabezpieczenie przed dzieleniem przez zero

        # Wzór: (1 - zysk) / losowa
        crash_point = (1 - house_edge) / r

        return max(1.00, int(crash_point * 100) / 100.0)

    def start_round(self) :
        """Rozpoczyna nową rundę - pobiera zakład i losuje wynik"""
        if self.balance >= 10 :  # Minimalny zakład 10
            self.balance -= 10
            self.current_bet = 10
            self.target_crash = self._generate_crash_point()
            self.current_multiplier = 1.00
            self.state = "RUNNING"
            print(f"DEBUG: Wynik ustalony na: {self.target_crash}x")  # Do testów w konsoli

    def cash_out(self) :
        """Gracz wypłaca środki w trakcie lotu"""
        if self.state == "RUNNING" :
            self.state = "SUCCESS"
            self.cashout_point = self.current_multiplier
            win_amount = int(self.current_bet * self.cashout_point)
            self.balance += win_amount

    def update(self) :
        """Logika gry wykonywana w każdej klatce (60 razy na sekunde)"""

        if self.state == "RUNNING" :
            # Zwiększamy mnożnik
            self.current_multiplier += self.growth_speed

            # Przyspieszamy animację im wyżej jesteśmy (dla emocji)
            if self.current_multiplier > 2.0 : self.growth_speed = 0.02
            if self.current_multiplier > 5.0 : self.growth_speed = 0.05
            if self.current_multiplier > 10.0 : self.growth_speed = 0.10

            # Sprawdzenie czy nastąpił wybuch
            if self.current_multiplier >= self.target_crash :
                self.current_multiplier = self.target_crash  # Ustawiamy na wynik końcowy
                self.state = "CRASHED"
                self.growth_speed = 0.01  # Reset prędkości na przyszłość

    def handle_input(self, event) :
        """Obsługa klawiszy specyficzna dla Crasha"""
        if event.type == pygame.KEYDOWN :

            # SPACJA obsługuje akcje w zależności od stanu
            if event.key == pygame.K_SPACE :
                if self.state == "BETTING" or self.state == "CRASHED" or self.state == "SUCCESS" :
                    self.start_round()
                elif self.state == "RUNNING" :
                    self.cash_out()

    def draw(self) :
        """Rysowanie wszystkiego na ekranie"""
        self.screen.fill(BLACK)

        # 1. Rysowanie Mnożnika na środku
        color = WHITE
        if self.state == "RUNNING" : color = GREEN
        if self.state == "CRASHED" : color = RED
        if self.state == "SUCCESS" : color = YELLOW

        text_value = f"{self.current_multiplier:.2f}x"
        text_surf = self.font_big.render(text_value, True, color)
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_surf, text_rect)

        # 2. Rysowanie informacji o stanie (UI)
        balance_text = self.font_small.render(f"Portfel: {self.balance} $", True, WHITE)
        self.screen.blit(balance_text, (20, 20))

        # 3. Instrukcje na dole ekranu
        msg = ""
        if self.state == "BETTING" :
            msg = "Nacisnij SPACJE aby postawic 10$ i startowac"
        elif self.state == "RUNNING" :
            msg = f"Nacisnij SPACJE aby wyplacic! (Wygrana: {int(self.current_bet * self.current_multiplier)}$)"
        elif self.state == "CRASHED" :
            msg = f"PRZEGRANA! Przegrales. Wynik to {self.target_crash:.2f}x. Spacja = Nowa gra"
        elif self.state == "SUCCESS" :
            msg = f"WYGRANA! Zgarnales {int(self.current_bet * self.cashout_point)}$. Spacja = Nowa gra"

        instr_surf = self.font_small.render(msg, True, GRAY)
        instr_rect = instr_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(instr_surf, instr_rect)


# --- FUNKCJA STARTOWA ---
def run_crash_game(screen) :
    clock = pygame.time.Clock()
    game = CrashGame(screen)  # Tworzymy instancję klasy
    running = True

    while running :
        # 1. Obsługa zdarzeń
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    running = False

            # Przekazujemy input do gry
            game.handle_input(event)

        # 2. Aktualizacja logiki
        game.update()

        # 3. Rysowanie
        game.draw()

        pygame.display.flip()
        clock.tick(60)


# --- TRYB TESTOWY  ---
if __name__ == "__main__" :
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Crash Game")

    run_crash_game(screen)

    pygame.quit()