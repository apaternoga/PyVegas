import os
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
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.music_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "crash", "crash_low_to_high.mp3")
        )
        self.crash_sfx_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "crash", "crash_explosion.mp3")
        )
        self.cashout_sfx_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "crash", "cashout.mp3")
        )
        try:
            pygame.mixer.music.load(self.music_path)
        except pygame.error:
            self.music_path = None
        try:
            self.crash_sfx = pygame.mixer.Sound(self.crash_sfx_path)
        except pygame.error:
            self.crash_sfx = None
        try:
            self.cashout_sfx = pygame.mixer.Sound(self.cashout_sfx_path)
        except pygame.error:
            self.cashout_sfx = None

        # Stan portfela (Tymczasowy, docelowo pobierany z globalnego gracza)
        self.balance = 1000
        self.current_bet = 0
      
        # Historia wynikow
        self.game_history = []
  
        #Przyciski bet i cashout
        self.btn_bet_rect = pygame.Rect(430, 500, 150, 50)
        self.btn_cash_rect = pygame.Rect(670, 500, 150, 50)

        #Ustalanie przez gracza wysokosci zakladu
        self.bet_input_text = "10" #to jest domyslna wysokosc zakladu
        self.bet_input_rect = pygame.Rect(540, 600, 150, 40) #pozycja okienka gdzie mozna wpisac wysokosc zaklad

        # Autocashout
        self.auto_cashout_text = "1.00"
        self.auto_cashout_rect = pygame.Rect(690, 600, 150, 40)
        self.auto_cashout_on = False
        self.auto_cashout_toggle_rect = pygame.Rect(850, 600, 70, 40) # Kwadracik do odznaczenia czy ma byc autocashout czy nie

        self.active_input = "BET" # BET lub AUTO - ktore okienko edytujemy
       
        #Komunikaty bledu zwiazane z wysokoscia zakladu
        self.error_msg = ""
        self.error_timer = 0    

        # Zmienne gry
        self.state = "BETTING"  # Opcje: BETTING, RUNNING, CRASHED, SUCCESS
        self.current_multiplier = 1.00
        self.target_crash = 1.00
        self.cashout_point = 0.0

        # Szybkość wzrostu (animacja)
        self.growth_speed = 0.01
        

        # Wykres
        self.history = [1.0] # Lista przechowujaca historie mnoznika
        self.graph_rect = pygame.Rect(340, 150, 600, 300) # Obszar wykresu
    
    
        
        
    def show_error(self, msg):
        self.error_msg = msg
        self.error_timer = 120

 
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

        # Jesli runda juz trwa, to nie mozna postawic znowu przed jej koncem
        if self.state == "RUNNING":
            return

        # Walidacja stawki zakladu:
        try:
            amount = int(self.bet_input_text)
        except ValueError:
            amount = 0

        #podawana jest wysokosc zakladu przez gracza
        amount = int(self.bet_input_text) if self.bet_input_text != "" else 0
        
        #zaklad musi byc liczba dodatnia i nie moze byc wiekszy od stanu konta gracza
     

        if amount <= 0:
            self.show_error("Minimalna stawka zakladu to $1")
            return
   
        if amount > self.balance:
            self.show_error("Niewystarczajace srodki na koncie!")
            return


        # Walidacja autocashout
        if self.auto_cashout_on:
            try:
                ac_val = float(self.auto_cashout_text)
                if ac_val < 1.01:
                    self.auto_cashout_text = "1.01"  # Automatyczna korekta
                    self.show_error("Min. autocashout to 1.01x")
                    return
            except ValueError:
                self.auto_cashout_text = "1.01"
                self.show_error("Nieprawidlowy format mnoznika!")
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.current_bet = amount
        
            #self.current_bet = 10
            self.target_crash = self._generate_crash_point()
            self.current_multiplier = 1.00
            self.history = [1.0] # Reset wykresu; zaczynamy od 1.0x
            self.state = "RUNNING"
            print(f"DEBUG: Wynik ustalony na: {self.target_crash}x")  # Do testów w konsoli

        
            
    def cash_out(self) :
        """Gracz wypłaca środki w trakcie lotu"""
        if self.state == "RUNNING":

            # Dodanie do historii obecnego wyniku przy sukcesie
            if self.cashout_sfx:
                self.cashout_sfx.play()

            self.game_history.append((self.current_multiplier, True))
            if len(self.game_history) > 10: self.game_history.pop(0)
            self.state = "SUCCESS"
            self.cashout_point = self.current_multiplier
            win_amount = int(self.current_bet * self.cashout_point)
            self.balance += win_amount
            #self.growth_speed = 0.01 # Reset predkosci takze przy sukcesie

    def update(self) :
        """Logika gry wykonywana w każdej klatce (60 razy na sekunde)"""
 
      # dodanie timera bledu
        if self.error_timer > 0:
            self.error_timer -= 1
        else:
            self.error_msg = "" #ukryj blad gdy timer minie        

        if self.state == "RUNNING" :
            # Zwiększamy mnożnik
            self.current_multiplier += self.growth_speed
            self.history.append(self.current_multiplier) # Dodanie obecnego mnoznika do historii wykresu
            if self.music_path and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            # Logika autocashout
            if self.auto_cashout_on and self.state == "RUNNING":
                try:
                    limit = float(self.auto_cashout_text)
                    if self.current_multiplier >= limit:
                        self.cash_out()
                except ValueError: 
                    pass

            # Przyspieszamy animację im wyżej jesteśmy (dla emocji)
            if self.current_multiplier > 2.0 : self.growth_speed = 0.02
            if self.current_multiplier > 5.0 : self.growth_speed = 0.05
            if self.current_multiplier > 10.0 : self.growth_speed = 0.10

            # Sprawdzenie czy nastąpił wybuch
            if self.current_multiplier >= self.target_crash :
                self.current_multiplier = self.target_crash  # Ustawiamy na wynik końcowy
                if self.crash_sfx:
                    self.crash_sfx.play()
                self.game_history.append((self.target_crash, False))  # Dodanie do historii wyniku przy crashu
                if len(self.game_history) > 10: self.game_history.pop(0) # Tylko 10 ostatnich wynikow naraz
                self.state = "CRASHED"
                self.growth_speed = 0.01  # Reset prędkości na przyszłość
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

        if self.state == "SUCCESS": self.growth_speed = 0.01 

    def handle_input(self, event) :
        """Obsługa klawiszy specyficzna dla Crasha"""
        if event.type == pygame.KEYDOWN :
            #target_attr = "bet_input_text" if self.active_input == "BET" else "auto_cashout_text"
            #current_val = getattr(self, target_attr)

            if self.state != "RUNNING":
                if self.active_input == "BET":
                    
                    if event.key == pygame.K_BACKSPACE:                  #mozna usunac tekst z okienka
                        self.bet_input_text = self.bet_input_text[:-1]
                    elif event.unicode.isdigit():
                        if len(self.bet_input_text) < 8:                  #limit dlugosci wartosci zakladu
                            self.bet_input_text += event.unicode

                elif self.active_input == "AUTO":
                    if event.key == pygame.K_BACKSPACE: 
                        self.auto_cashout_text = self.auto_cashout_text[:-1]
                     # Pozwalamy na cyfry i kropke dla mnoznika
                    elif event.unicode.isdigit():
                        if len(self.auto_cashout_text) < 4:
                            self.auto_cashout_text += event.unicode
                    elif event.unicode == ".":
                        if "." not in self.auto_cashout_text: 
                            if len(self.auto_cashout_text) < 4:
                                self.auto_cashout_text += event.unicode

            # SPACJA obsługuje akcje w zależności od stanu
            if event.key == pygame.K_SPACE :
                if self.state == "RUNNING":
                    self.cash_out()
                else:
                    self.start_round()

        if event.type == pygame.MOUSEBUTTONDOWN:
             # Przyciski akcji
            if event.button == 1:
                if self.btn_bet_rect.collidepoint(event.pos):
                    self.start_round()
                if self.btn_cash_rect.collidepoint(event.pos):
                    self.cash_out()
           # Wybor okienka do pisania 
                if self.bet_input_rect.collidepoint(event.pos):
                    self.active_input = "BET"
                if self.auto_cashout_rect.collidepoint(event.pos):
                    self.active_input = "AUTO"
             
           # Wlacznik On/Off
                if self.auto_cashout_toggle_rect.collidepoint(event.pos):
                    self.auto_cashout_on = not self.auto_cashout_on

    def draw_button(self, rect, text, color, active):
        mouse_pos = pygame.mouse.get_pos()
        draw_color = color
        if not active:          # Przyciski maja inne kolory kiedy user najedzie na nie kursorem 
            draw_color = GRAY
        elif rect.collidepoint(mouse_pos):
            draw_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255))

        pygame.draw.rect(self.screen, draw_color, rect, border_radius = 10)
        btn_text = self.font_small.render(text, True, WHITE)
        btn_rect = btn_text.get_rect(center=rect.center)
        self.screen.blit(btn_text, btn_rect)


    def draw(self) :
        """Rysowanie wszystkiego na ekranie"""
        self.screen.fill(BLACK)


        # Rysowanie historii
        history_x = 340
        for val, is_success in self.game_history:
            # Kolor zalezny od tego, czy gracz zdazyl wyplacic
            color = GREEN if is_success else RED

            txt = self.font_small.render(f"{val:.2f}x", True, color)
            self.screen.blit(txt, (history_x, 110))
            history_x += txt.get_width() + 20

        # Rysowanie wykresu
        line_color = WHITE
        if self.state == "RUNNING" : line_color = GREEN
        if self.state == "CRASHED" : line_color = RED
        if self.state == "SUCCESS" : line_color = YELLOW


        if len(self.history) > 1:
            points = []
            max_val = max(self.history) if max(self.history) > 2.0 else 2.0

            for i, val in enumerate(self.history):
                # X: rozkladamy punkty rownomiernie na szerokosc okna 
                x = self.graph_rect.x + (i / len(self.history)) * self.graph_rect.width
                # Y: skalujemy wartosc wzgledem max_val (w pygame igreki rosna w dol)
                y = self.graph_rect.y + self.graph_rect.height - ((val - 1) / (max_val - 1)) * self.graph_rect.height
                points.append((x, y))


            pygame.draw.lines(self.screen, line_color, False, points, 4)
 
                # Rysowanie ramki wykresu    
        #pygame.draw.rect(self.screen, (40, 40, 40), self.graph_rect, 2, border_radius = 5)




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
            msg = "Nacisnij SPACJE aby postawic"
        elif self.state == "RUNNING" :
            msg = f"Nacisnij SPACJE aby wyplacic! (Wygrana: {int(self.current_bet * self.current_multiplier)}$)"
        elif self.state == "CRASHED" :
            msg = f"PRZEGRANA! Przegrales. Wynik to {self.target_crash:.2f}x. Spacja = Nowa gra"
        elif self.state == "SUCCESS" :
            msg = f"WYGRANA! Zgarnales {int(self.current_bet * self.cashout_point)}$. Spacja = Nowa gra"

        instr_surf = self.font_small.render(msg, True, GRAY)
        instr_rect = instr_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
        self.screen.blit(instr_surf, instr_rect)
     

        self.draw_button(self.btn_bet_rect, "POSTAW", GREEN, self.state != "RUNNING")
        self.draw_button(self.btn_cash_rect, "WYPLAC", YELLOW, self.state == "RUNNING")


        # Komunikaty bledu
        if self.error_msg:
            err_surf = self.font_small.render(self.error_msg, True, RED)
           
            err_pos_x = self.bet_input_rect.x + self.bet_input_rect.width - 625
            err_pos_y = self.bet_input_rect.y + 5

            self.screen.blit(err_surf, (err_pos_x, err_pos_y))



        box_color = GRAY if self.state == "RUNNING" else YELLOW # Jesli gra dalej trwa to okienko jest szare

        # Tlo i ramka okienka
        pygame.draw.rect(self.screen, (30, 30, 30), self.bet_input_rect)
        pygame.draw.rect(self.screen, box_color, self.bet_input_rect, 2)

        # Napis pomocniczy
        label = self.font_small.render("STAWKA: ", True, WHITE)
        self.screen.blit(label, (self.bet_input_rect.x, self.bet_input_rect.y - 35))

        #Tekst w okineku ze znakiem dolara
        val_surf = self.font_small.render(self.bet_input_text + " $", True, WHITE)
        self.screen.blit(val_surf, (self.bet_input_rect.x + 10, self.bet_input_rect.y + 5))


        # Okienko autocashout
        auto_cashout_box_color = (50, 150, 255) if self.active_input == "AUTO" else (100, 100, 100)
        pygame.draw.rect(self.screen, (30, 30, 30), self.auto_cashout_rect)
        pygame.draw.rect(self.screen, auto_cashout_box_color, self.auto_cashout_rect, 2)

        auto_cashout_label = self.font_small.render("AUTO-CASHOUT:", True, WHITE)
        self.screen.blit(auto_cashout_label, (self.auto_cashout_rect.x, self.auto_cashout_rect.y - 35))

        auto_cashout_val_surf = self.font_small.render(self.auto_cashout_text + " x", True, WHITE)
        self.screen.blit(auto_cashout_val_surf, (self.auto_cashout_rect.x + 10, self.auto_cashout_rect.y + 5))


        # Przycisk On/Off
        toggle_color = (50, 220, 50) if self.auto_cashout_on else (220, 50, 50)
        pygame.draw.rect(self.screen, toggle_color, self.auto_cashout_toggle_rect, border_radius = 5)

        status_text = "ON" if self.auto_cashout_on else "OFF"
        status_surf = self.font_small.render(status_text, True, WHITE)
        self.screen.blit(status_surf, (self.auto_cashout_toggle_rect.x + 5, self.auto_cashout_toggle_rect.y+5)) 
 

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


