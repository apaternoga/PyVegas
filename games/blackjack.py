import random
from core.settings import *

# importuje wartosci takie jak BLACK itd. z stworzonego juz pliku settings
import sys
import pygame
#potrzebne do ruchu strzaleczek
import math

# definicje kolorow i rang kart
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # karta sie teraz pojawia poza ekranem
        self.x = -150
        self.y = 300
        # animacja bedzie od self.x itd do target
        self.target_x = -150
        self.target_y = 300
        # predkosc 0.1 to 10% dystansu na klatke
        self.speed = 0.1

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    # nowa funkcja do obliczania ruchu
    def update(self):
        #olbiczam roznice miedzy celem a obecna pozycja
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # jesli jestesmy blisko celu to ustawiamy pozycje idealnie, zeby nie bylo efektu drgania karty
        if abs(dx) < 1 and abs(dy) < 1:
            self.x = self.target_x
            self.y = self.target_y
        else:
            self.x += dx * self.speed
            self.y += dy * self.speed

    # ZMIANA: draw teraz pobiera target zamiast zwyklego x i y
    def draw(self, screen, target_x, target_y, hidden=False):
        # ustawiamy cel i aktualizujemy pozycje
        self.target_x = target_x
        self.target_y = target_y
        self.update()

        # do rysowania uzywamy aktualnej (tej aktualizowanej)
        x = int(self.x)
        y = int(self.y)

        # Rysujemy cień: daje on efekt głębi
        shadow_rect = pygame.Rect(x + 2, y + 2, 100, 150)
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Główny kształt karty
        rect = pygame.Rect(x, y, 100, 150)
        pygame.draw.rect(screen, WHITE, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        # Jeśli ukryta (karta dealera)
        if hidden:
            # Wzór na "plecach" karty
            inner_rect = pygame.Rect(x + 5, y + 5, 90, 140)
            pygame.draw.rect(screen, RED, inner_rect, border_radius=5)
            # Znak zapytania
            font_hidden = pygame.font.SysFont("Times New Roman", 60, bold=True)
            text_surf = font_hidden.render("?", True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            return

        # Konwersja nazw na symbole
        rank_conversion = {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": "J",
            "Queen": "Q",
            "King": "K",
            "Ace": "A",
        }
        suits_symbols = {"Hearts": "♥", "Diamonds": "♦", "Spades": "♠", "Clubs": "♣"}

        suit_icon = suits_symbols[self.suit]
        rank_short = rank_conversion[self.rank]

        # Kolor czcionki
        color = RED if self.suit in ["Hearts", "Diamonds"] else BLACK

        rank_str = str(rank_short) 

        # Czcionki
        font_corner = pygame.font.SysFont("Arial", 18, bold=True)
        font_pip = pygame.font.SysFont("Segoe UI Symbol", 28) # Do małych symboli
        font_face = pygame.font.SysFont("Times New Roman", 60) # Do figur

        # --- RYSOWANIE ROGÓW ---

        # Lewy górny
        screen.blit(font_corner.render(rank_str, True, color), (x + 5, y + 5))
        screen.blit(font_corner.render(suit_icon, True, color), (x + 5, y + 25))
        
        # Prawy dolny
        corner_rank_surf = font_corner.render(rank_str, True, color)
        corner_rank_surf = pygame.transform.rotate(corner_rank_surf, 180)
        corner_suit_surf = font_corner.render(suit_icon, True, color)
        corner_suit_surf = pygame.transform.rotate(corner_suit_surf, 180)

        screen.blit(corner_rank_surf, (x + 95 - corner_rank_surf.get_width(), y + 145 - 20))
        screen.blit(corner_suit_surf, (x + 95 - corner_suit_surf.get_width(), y + 145 - 40))

        # Pozycje
        if isinstance(rank_short, int): # LICZBY 2-10
            # Pozycje X
            col_L = 28
            col_M = 50
            col_R = 72
            
            # Pozycje Y
            row_T = 35
            row_MT = 57
            row_C = 75
            row_MB = 93
            row_B = 115
            
            pips = []
            if rank_short == 2:
                pips = [(col_M, row_T), (col_M, row_B)]
            elif rank_short == 3:
                pips = [(col_M, row_T), (col_M, row_C), (col_M, row_B)]
            elif rank_short == 4:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_B), (col_R, row_B)]
            elif rank_short == 5:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_B), (col_R, row_B), (col_M, row_C)]
            elif rank_short == 6:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_C), (col_R, row_C), (col_L, row_B), (col_R, row_B)]
            elif rank_short == 7:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_C), (col_R, row_C), (col_L, row_B), (col_R, row_B), (col_M, row_MT)]
            elif rank_short == 8:
                pips = [(col_L, row_T), (col_R, row_T), (col_L, row_C), (col_R, row_C), (col_L, row_B), (col_R, row_B), (col_M, row_MT), (col_M, row_MB)]
            elif rank_short == 9:
                 pips = [
                     (col_L, row_T), (col_L, row_MT+3), (col_L,  row_MB-3), (col_L, row_B), # Lewa
                     (col_R, row_T), (col_R, row_MT+3), (col_R,  row_MB-3), (col_R, row_B), # Prawa
                     (col_M, row_C) # Środek
                 ]
            elif rank_short == 10:
                 pips = [
                     (col_L, row_T), (col_L, row_MT+3), (col_L,  row_MB-3), (col_L, row_B), # Lewa
                     (col_R, row_T), (col_R, row_MT+3), (col_R,  row_MB-3), (col_R, row_B), # Prawa
                     (col_M, 48), (col_M, 102) # Dwa w środku
                 ]

            # Rysowanie małych symboli
            for (px, py) in pips:
                pip_surf = font_pip.render(suit_icon, True, color)

                if py > 75:
                    pip_surf = pygame.transform.rotate(pip_surf, 180)

                pip_rect = pip_surf.get_rect(center=(x + px, y + py))
                screen.blit(pip_surf, pip_rect)

        else: 
            # FIGURY (J, Q, K, A)
            if rank_short == "A":
                font_ace = pygame.font.SysFont("Segoe UI Symbol", 80)
                pip_surf = font_ace.render(suit_icon, True, color)
                pip_rect = pip_surf.get_rect(center=(x + 50, y + 75))
                screen.blit(pip_surf, pip_rect)
            else:
                # Dla figur (J, Q, K) ramka i litera
                pygame.draw.rect(screen, color, (x+20, y+30, 60, 90), 1)
                
                face_surf = font_face.render(rank_str, True, color)
                face_rect = face_surf.get_rect(center=(x + 50, y + 75))
                screen.blit(face_surf, face_rect)


class Button:
    def __init__(self, text, x, y, w, h, color=GOLD, text_color=BLACK, sm=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text_color = text_color
        # Kolor po najechaniu
        self.hover_color = (255, 240, 100)
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.is_hovered = False
        self.label_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.sm = sm

    def draw(self, screen):
        # Efekt podswietlenia po najechaniu
        mouse_pos = pygame.mouse.get_pos()
        if (self.is_hovered != self.rect.collidepoint(mouse_pos)):
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            if self.sm:
                self.sm.play_sound("hover")

        current_color = self.hover_color if self.is_hovered else self.color

        # Rysowanie przycisku
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        # Wysrodkowanie tekstu na przycisku
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    # Funkcja ktora zwraca True tylko gdy klikniemy ja lewym przyciskiem myszki
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.sm:
                    self.sm.play_sound("click")
                return True
        return False

class Deck:

    # ZMIANA: obsługa wielu talii
    def __init__(self, num_decks=6):
        self.deck = []
        self.num_decks = num_decks
        self.create_shoe()

    def create_shoe(self):
        self.deck = []
        for _ in range(self.num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit, rank))
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if len(self.deck) == 0:
            self.create_shoe()
        
        card = self.deck.pop()
        # reset pozycji karty, aby wylatywala z lewej strony
        card.x = -150
        card.y = 300
        return card

    def needs_shuffle(self):
        return len(self.deck) < (52 * self.num_decks * 0.25)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.calculate_value()

    def calculate_value(self):
        self.value = 0
        self.aces = 0
        for card in self.cards:
            self.value += values[card.rank]
            if card.rank == "Ace":
                self.aces += 1
        self.adjust_for_ace()

    # As moze przyjmowac rozne wartosci, ta funkcja odpowiada za to zeby dopasowac najkorzystniejsza wartosc
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    # iterujac po decku, rysujemy obok siebie karty w przesunieciu o 10 pixeli od poprzedniej karty, (bo karta ma 100)
    # ZMIANA: Przekazujemy cel (target), a nie sztywna pozycje. Karta sie zanimuje.
    def draw(self, screen, start_x, start_y, hide_first=False):
        for i, card in enumerate(self.cards):
            is_hidden = hide_first and i == 0
            
            # obliczamy gdzie karta POWINNA sie znalezc
            target_x = start_x + (i * 110)
            target_y = start_y
            
            # przekazujemy to do karty, ona sama obsluguje ruch w strone celu
            card.draw(screen, target_x, target_y, hidden=is_hidden)

class BlackjackGame:
    def __init__(self, screen, sound_manager):
        self.screen = (
            screen  # referencja do glownego okna gry, tym sie zajmujemy juz w mainie
        )
        self.sm = sound_manager
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.label_font = pygame.font.SysFont("Arial", 22, bold=True)

        self.logo_font = pygame.font.SysFont("Brush Script MT", 65, italic=True)

        self.deck = Deck(num_decks=6)
        self.player_hands = []
        self.current_hand_index = 0
        self.dealer_hand = Hand()

        self.state = "betting"
        
        self.deal_queue = []
        self.last_timer = 0
        self.deal_interval = 200    #200
        self.dealer_interval = 800  #800
        
        self.text_anim_progress = 0.0

        self.message = "Please place your bet (↑ / ↓), then press DEAL."
        self.chips = STARTING_MONEY
        self.current_bet = 10
        self.insurance_bet = 0
        self.wait_timer = 0
    
        # LOGIKA PRZYCISKÓW
        btn_y = SCREEN_HEIGHT - 75 
        
        
        btn_w_std = 110       
        btn_w_wide = 130      
        spacing = 10 

        #zmiany, aby wysrodkowac przyciski, po przedluzeniu surr
        total_width_buttons = (4 * btn_w_std) + btn_w_wide + (4 * spacing)
        
        
        start_x = (SCREEN_WIDTH - total_width_buttons) // 2
        
        
        current_x = start_x

        # HIT
        self.btn_hit = Button("HIT", current_x, btn_y, btn_w_std, 50, sm=self.sm)
        current_x += btn_w_std + spacing  

        # STAND
        self.btn_stand = Button("STAND", current_x, btn_y, btn_w_std, 50, sm=self.sm)
        current_x += btn_w_std + spacing

        # DOUBLE
        self.btn_double = Button(
            "DOUBLE", current_x, btn_y, btn_w_std, 50, color=(200, 150, 50), sm=self.sm
        )
        current_x += btn_w_std + spacing

        # SPLIT
        self.btn_split = Button(
            "SPLIT", current_x, btn_y, btn_w_std, 50, color=(200, 150, 50), sm=self.sm
        )
        current_x += btn_w_std + spacing

        # SURRENDER - szerszy od reszty
        self.btn_surrender = Button(
            "SURRENDER", 
            current_x, 
            btn_y, 
            btn_w_wide, # Tu używamy większej szerokości
            50,
            color=(150, 50, 50),
            text_color=WHITE,
            sm=self.sm
        )

        # Przycisk DEAL
        self.btn_deal = Button(
            "DEAL",
            SCREEN_WIDTH // 2 - 100,
            btn_y,
            200,
            50,
            color=WHITE,
            text_color=BLACK,
            sm=self.sm
        )

        # UI DLA INSURANCE
        # Środek ekranu
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Przyciski będą wewnątrz okienka
        self.btn_ins_yes = Button("YES", cx - 110, cy + 20, 100, 50, color=(50, 150, 50), text_color=WHITE, sm=self.sm) # Zielony
        self.btn_ins_no = Button("NO", cx + 10, cy + 20, 100, 50, color=(150, 50, 50), text_color=WHITE, sm=self.sm)   # Czerwony


    # NOWA FUNKCJA: obsluguje logike oparta na czasie (zamiast time.wait)
    def update(self):
        current_time = pygame.time.get_ticks()

        # Sprawdź opóźnienie przed przejściem do dealera
        if self.wait_timer > 0 and current_time >= self.wait_timer:
            self.wait_timer = 0
            self.state = "dealer_turn"
            self.message = "Dealer's Turn."
            self.sm.play_sound("card_place3")
            self.last_timer = current_time

        # obsluga animacji
        # tekst sie pojawia dopiero w fazie obstawiania
        if self.state != "betting":
            # jesli pojawiaja sie karty to pojawia sie tekst
            if len(self.player_hands) > 0 and len(self.player_hands[0].cards) > 0:
                if self.text_anim_progress < 1.0:
                    self.text_anim_progress += 0.01 # Prędkość pojawiania się (fade in)
                    if self.text_anim_progress > 1.0:
                        self.text_anim_progress = 1.0

        # rozdawanie kart sekwencjami
        if self.state == "dealing":
            if current_time - self.last_timer > self.deal_interval+300:
                if len(self.deal_queue) > 0:
                    # Pobieramy kto ma dostać kartę
                    target = self.deal_queue.pop(0)
                    card = self.deck.deal()
                    
                    if target == "player":
                        self.player_hands[0].add_card(card)
                    elif target == "dealer":
                        self.dealer_hand.add_card(card)
                    a=random.randint(1,4) 
                    self.sm.play_sound("deal"+str(a))
                    self.last_timer = current_time # Reset stopera
                else:
                    # Koniec rozdawania
                    # INSURANCE CHECK
                    # Sprawdzamy czy krupier ma ASA (karta index 1)
                    if len(self.dealer_hand.cards) >= 2 and self.dealer_hand.cards[1].rank == "Ace":
                        self.state = "insurance"
                        self.message = "Dealer shows Ace."
                    else:
                        # Brak Asa - normalna gra
                        self.state = "player_turn"
                        self.message = "Your Turn." # ZMIANA: Kropka zamiast wykrzyknika (spokojniej)
                        if self.check_initial_blackjack():
                            return

        # LOGIKA KRUPIERA - przeniesiona tutaj, aby nie blokować gry
        elif self.state == "dealer_turn":
            # Czekamy chwilę zanim krupier coś zrobi, żeby gracz widział co się dzieje
            if current_time - self.last_timer > self.dealer_interval:
                self.last_timer = current_time # Reset stopera
                
                # dealer dobiera karty dopoki ma mniej niz 17 pkt
                # NOWA LOGIKA "Soft 17"
                # Soft 17 czyli kiedy dealer ma 17 ale liczony z asem
                if self.dealer_hand.value < 17 or (self.dealer_hand.value == 17 and self.dealer_hand.aces > 0):
                    self.dealer_hand.add_card(self.deck.deal())
                    self.sm.play_sound("card_place1")
                    self.message = "Dealer hits..."
                else:
                    # Krupier skończył, sprawdzamy wyniki
                    self.finish_round()

    def start_round(self):
        self.player_hands = [Hand()]
        self.current_hand_index = 0
        self.dealer_hand = Hand()
        self.player_hands[0].bet = self.current_bet

        # POPRAWKA: Odejmujemy pieniądze na starcie
        self.chips -= self.current_bet

        self.deck = Deck(num_decks=6)
        self.deck.shuffle()

        # zamiast rozdawac od razu w petli (co blokuje), tworzymy kolejkę
        # Rozdajemy po 2 karty (Gracz, Dealer, Gracz, Dealer)
        self.deal_queue = ["player", "dealer", "player", "dealer"]
        
        self.state = "dealing"
        self.message = "Dealing cards..."
        self.last_timer = pygame.time.get_ticks()
        
        # Resetujemy animację tekstu przy nowym rozdaniu
        self.text_anim_progress = 0.0

    def check_initial_blackjack(self, hand_index=0):
        # Sprawdzamy czy gracz ma 21
        player_bj = self.player_hands[hand_index].value == 21
        
        if player_bj:
             if len(self.player_hands) == 1:
                 # Jeśli to jedyna ręka i mamy BJ, przechodzimy do rozstrzygnięcia
                 self.next_hand_or_dealer()
                 return True
        return False

    #NOWA FUNKCJA DO ROZSTRZYGANIA INSURANCE
    def resolve_insurance(self, take_insurance):
        insurance_cost = self.current_bet // 2
        
        if take_insurance:
            if self.chips >= insurance_cost:
                self.chips -= insurance_cost
                self.insurance_bet = insurance_cost
                self.message = "Insurance taken."
            else:
                self.message = "Insufficient funds for insurance."
                take_insurance = False

        # Sprawdzamy zakrytą kartę krupiera (index 0)
        hidden_card_value = values[self.dealer_hand.cards[0].rank]
        dealer_has_bj = (hidden_card_value == 10)
        
        if dealer_has_bj:
            # KRUPIER MA BLACKJACKA
            if take_insurance:
                payout = self.insurance_bet * 3
                self.chips += payout
                self.message = "Insurance Pays! Dealer has Blackjack."
            else:
                self.message = "Dealer has Blackjack."
            
            self.finish_round()
        else:
            # KRUPIER NIE MA BLACKJACKA
            if take_insurance:
                self.message = "Dealer no Blackjack. Insurance lost."
            else:
                self.message = "Dealer no Blackjack. Your Turn."
            
            self.state = "player_turn"
            
            if self.check_initial_blackjack():
                return
            

    # funkcja odpowiadajaca za wcisniecia klawiszy ORAZ myszki
    def handle_input(self, event):
        # system obstawiania
        if self.state == "betting":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.chips >= self.current_bet:
                        self.start_round()
                    else:
                        self.message = "Insufficient funds." 
                elif event.key == pygame.K_UP:
                    if self.chips >= self.current_bet + 10:
                        self.current_bet += 10
                elif event.key == pygame.K_DOWN:
                    if self.chips > 10:
                        self.current_bet -= 10

            # obsluga myszki dla przycisku rozdaj
            if self.btn_deal.is_clicked(event):
                if self.chips >= self.current_bet:
                    self.start_round()
                else:
                    self.message = "Insufficient funds." 

        # OBSŁUGA INSURANCE
        elif self.state == "insurance":
            if self.btn_ins_yes.is_clicked(event):
                self.resolve_insurance(True)
            elif self.btn_ins_no.is_clicked(event):
                self.resolve_insurance(False)

        # ruch gracza dobiera (HIT) lub nie dobiera(STAY)
        elif self.state == "player_turn":
            current_hand = self.player_hands[self.current_hand_index]

            # zmienna pomocnicza zeby nie pisac kodu dwa razy dla klawiatury i myszki
            action = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    action = "hit"
                elif event.key == pygame.K_s:
                    action = "stand"
                elif event.key == pygame.K_d:
                    action = "double"
                elif event.key == pygame.K_p:
                    action = "split"
                elif event.key == pygame.K_u:
                    action = "surrender"

            # sprawdzamy klikniecia myszka
            if self.btn_hit.is_clicked(event):
                action = "hit"
            elif self.btn_stand.is_clicked(event):
                action = "stand"
            elif self.btn_double.is_clicked(event):
                if self.chips >= current_hand.bet and len(current_hand.cards) == 2:
                    action = "double"
            elif self.btn_split.is_clicked(event):
                if (
                    len(current_hand.cards) == 2
                    and values[current_hand.cards[0].rank] == values[current_hand.cards[1].rank]
                    and self.chips >= self.current_bet
                    and len(self.player_hands) < 2
                ):
                    action = "split"
            elif self.btn_surrender.is_clicked(event):
                if len(self.player_hands) == 1 and len(current_hand.cards) == 2:
                    action = "surrender"

            # wykonanie akcji
            if (
                action == "hit"
            ):  # jesli gracz kliknie h dodajemy mu karte do reki i sprawdzamy czy przekroczyl wartosc 21
                current_hand.add_card(self.deck.deal())
                self.sm.play_sound("card_place3")
                if current_hand.value > 21:
                    self.next_hand_or_dealer(wait=True)

            elif action == "stand":  # jesli s dobieramy karte dealerowi
                self.next_hand_or_dealer()

            # NOWA LOGIKA "DOUBLE DOWN"
            elif action == "double":
                # podwajamy tylko dla aktualnej reki
                if self.chips >= current_hand.bet and len(current_hand.cards) == 2:
                    self.chips -= current_hand.bet # Pobieramy stawkę
                    current_hand.bet *= 2 # Podwajamy stawkę ręki
                    
                    # w prawdziwej grze kazda reka po splicie ma wlasny zaklad
                    # dla uproszczenia przyjmujemy ze current bet to stawka na JEDNA reke (tutaj zmodyfikowana)
                    current_hand.add_card(self.deck.deal())
                    self.sm.play_sound("card_place2")
                    self.next_hand_or_dealer(wait=True) # Po double zawsze koniec tury tej ręki
                else:
                    self.message = "Double down unavailable." 

            # NOWA LOGIKA "SPLIT"
            elif action == "split":
                self.perform_split()

            elif action == "surrender":
                refund = current_hand.bet // 2
                self.chips += refund
                self.message = f"Surrendered. Refund: {refund}." 
                self.state = "game_over"

        # to odpowiada za "kliknij spacje zeby zaczac ponownie"
        elif self.state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()
            if self.btn_deal.is_clicked(event):
                self.reset_game()

    def perform_split(self):
        # Pobieramy aktualna reke
        current_hand = self.player_hands[self.current_hand_index]
        self.chips -= self.current_bet
        
        # Zabieramy jedna karte z obecnej reki, by stworzyc nowa
        card_to_move = current_hand.cards.pop()
        current_hand.calculate_value() # Aktualizujemy wartosc obecnej reki
        
        new_hand = Hand()
        new_hand.add_card(card_to_move)
        new_hand.bet = self.current_bet
        
        # Dobieramy po jednej karcie do obu rozdzielonych rąk
        current_hand.add_card(self.deck.deal())
        new_hand.add_card(self.deck.deal())
        self.sm.play_sound("card_place4")

        # wstawiamy nowa reke zaraz po aktualnej rece w liscie,
        # dzieki czemu gra płynnie przejdzie do niej w nastepnym kroku petli
        self.player_hands.insert(self.current_hand_index + 1, new_hand)
        self.message = "Hands Split." 

    def next_hand_or_dealer(self, wait=False):
        if self.current_hand_index < len(self.player_hands) - 1:
            self.current_hand_index += 1
            
            self.message = f"Hand {self.current_hand_index + 1}: Your Turn."
            if self.player_hands[self.current_hand_index].value == 21:
                 # Jeśli kolejna ręka ma 21, przechodzimy dalej (opcjonalnie)
                 self.next_hand_or_dealer()
        else:
            if wait:
                self.wait_timer = pygame.time.get_ticks() + 800
                self.message = "Bust! Waiting for dealer..."
            else:
                self.state = "dealer_turn"
                self.message = "Dealer's Turn." 
                self.sm.play_sound("card_place3")
                self.last_timer = pygame.time.get_ticks() # Resetujemy timer dla dealera

    # funkcja wywolywana gdy krupier konczy (zamiast starego dealer_logic)
    def finish_round(self):
        # Sprawdzamy czy dealer ma Blackjacka
        dealer_is_bj = self.dealer_hand.value == 21 and len(self.dealer_hand.cards) == 2
        
        parts = [] # lista na komunikaty dla kazdej reki
        is_split = len(self.player_hands) > 1

        for i, hand in enumerate(self.player_hands):
            player_is_bj = hand.value == 21 and len(hand.cards) == 2
            
            # Budujemy tekst dla tej konkretnej ręki
            current_part = ""
            if is_split:
                current_part = f"Hand {i+1}: "

            # LOGIKA GRY (FINANSE I TEKST)
            
            if hand.value > 21:
                # Fura (przegrana)
                current_part += "Bust."
                self.sm.play_sound("lose")
            
            elif player_is_bj:
                if dealer_is_bj:
                    # Remis przy blackjackach
                    self.chips += hand.bet
                    current_part += "Push."
                else:
                    # Wygrana Blackjack (3:2)
                    win_amount = hand.bet + int(hand.bet * 1.5)
                    self.chips += win_amount
                    current_part += "Blackjack!"
                    self.sm.play_sound("win")
            
            elif self.dealer_hand.value > 21:
                # Dealer fura (wygrana)
                self.chips += hand.bet * 2
                current_part += "Win!"
                self.sm.play_sound("win")
            
            elif hand.value > self.dealer_hand.value:
                # Wygrana punktowa
                self.chips += hand.bet * 2
                current_part += "Win!"
                self.sm.play_sound("win")
            
            elif hand.value < self.dealer_hand.value:
                # Przegrana punktowa
                current_part += "Loss."
                self.sm.play_sound("lose")
            
            else:
                # Remis
                self.chips += hand.bet
                current_part += "Push."

            # Dodajemy gotowy tekst ręki do listy
            parts.append(current_part)

        # laczymy rece | zeby ladniej wygladalo
        self.message = " | ".join(parts)
        self.state = "game_over"

    def reset_game(self):
        self.state = "betting"
        self.message = "Please place your bet (↑ / ↓), then press DEAL."
        if self.chips < 10:
            self.chips = STARTING_MONEY
            self.message = "Bankroll reset."

    def draw_insurance_popup(self):
        
        dimmer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dimmer.set_alpha(150) #polprzezroczyste tlo
        dimmer.fill((0, 0, 0)) 
        self.screen.blit(dimmer, (0, 0))

        # ramka okienka
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        popup_w, popup_h = 400, 200
        popup_rect = pygame.Rect(cx - popup_w // 2, cy - popup_h // 2, popup_w, popup_h)
        
        pygame.draw.rect(self.screen, DARK_PANEL, popup_rect, border_radius=15)
        pygame.draw.rect(self.screen, GOLD, popup_rect, 3, border_radius=15)

        # tekst
        cost = self.current_bet // 2
        title_surf = self.label_font.render("Insurance?", True, GOLD)
        # informacja o koscie i wyplacie
        info_surf = self.small_font.render(f"Cost: {cost}  |  Pays 2:1", True, WHITE)

        title_rect = title_surf.get_rect(center=(cx, cy - 50))
        info_rect = info_surf.get_rect(center=(cx, cy - 20))

        self.screen.blit(title_surf, title_rect)
        self.screen.blit(info_surf, info_rect)

        # przyciski
        self.btn_ins_yes.draw(self.screen)
        self.btn_ins_no.draw(self.screen)

    # funkcja renderujaca - rysuje ona wszystko na ekranie w kazdej klatce
    def draw(self):
        self.screen.fill(GREEN_FELT)

        # Kolo na srodku
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        pygame.draw.circle(
            self.screen, (30, 120, 30), (center_x, center_y - 50), 120, 5
        )

        # Ozdobny napis
        logo_surf = self.logo_font.render(
            "Blackjack", True, (120, 215, 120)
        )
        logo_rect = logo_surf.get_rect(center=(center_x, center_y - 50))
        self.screen.blit(logo_surf, logo_rect)

        # Panel dolny
        panel_height = 100
        panel_y = SCREEN_HEIGHT - panel_height
        
        panel_rect = pygame.Rect(0, panel_y, SCREEN_WIDTH, panel_height)
        pygame.draw.rect(self.screen, DARK_PANEL, panel_rect)
        
        # Zlota linia
        pygame.draw.line(
            self.screen,
            GOLD,
            (0, panel_y),
            (SCREEN_WIDTH, panel_y),
            3,
        )

        # ZMIANA POZYCJI NAPISOW 
        
        # 1. Wyswietlanie Zetonow
        chips_text = self.font.render(f"Chips: {self.chips}", True, GOLD)
        chips_rect = chips_text.get_rect(midleft=(20, panel_y + (panel_height // 2)))
        self.screen.blit(chips_text, chips_rect)

        # 2. Wyswietlanie Stawki
        bet_info = f"Bet: {self.current_bet}"
        if self.state == "betting":
             bet_info += " ↕"
        
        bet_text = self.font.render(bet_info, True, GOLD)
        bet_rect = bet_text.get_rect(midright=(SCREEN_WIDTH - 20, panel_y + (panel_height // 2)))
        self.screen.blit(bet_text, bet_rect)

        # 3. Wiadomosc glowna 
        
        def draw_centered_msg_with_shadow(text, y_pos):
            # 1. Cień 
            shadow = self.font.render(text, True, BLACK)
            shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, y_pos + 2))
            self.screen.blit(shadow, shadow_rect)
            
            # 2. Właściwy tekst
            msg = self.font.render(text, True, MESSAGE_COLOR)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(msg, msg_rect)

    
        draw_centered_msg_with_shadow(self.message, 40)
        
        # LOGIKA POZYCJI KART I NAPISÓW

        dealer_cards_y = 100
        player_cards_y = 380
        
        current_alpha = int(self.text_anim_progress * 255)

        # Rysujemy elementy stołu (chyba że obstawiamy)
        if self.state != "betting":
            hide_dealer = self.state == "player_turn" or self.state == "insurance" or self.state == "dealing"
            dealer_x = 100

            # 1. RYSOWANIE KART
            self.dealer_hand.draw(self.screen, dealer_x, dealer_cards_y, hide_first=hide_dealer)
            for i, hand in enumerate(self.player_hands):
                start_x = 100
                gap = 600
                x_pos = start_x + (i * gap)
                hand.draw(self.screen, x_pos, player_cards_y)

           # 2. RYSOWANIE NAPISÓW (z fadem i CIENIEM)
            
            def draw_label_with_shadow(text, x, y, alpha):
                # 1. Cień
                shadow = self.label_font.render(text, True, BLACK)
                shadow.set_alpha(alpha)
                shadow_rect = shadow.get_rect(bottomleft=(x + 9, y - 5)) 
                self.screen.blit(shadow, shadow_rect)
                
                # 2. Właściwy tekst
                label = self.label_font.render(text, True, WHITE)
                label.set_alpha(alpha)
                label_rect = label.get_rect(bottomleft=(x + 7, y - 7))
                self.screen.blit(label, label_rect)

            # Napis Krupiera
            dealer_text = "Dealer"
            
            # Dodajemy licznik (z obsluga ukrytej karty)
            if len(self.dealer_hand.cards) > 0:
                if hide_dealer:
                    # JESLI KARTA JEST UKRYTA:
                    # Wyswietlamy wynik TYLKO jesli mamy juz druga karte (te odkryta).
                    # Jesli krupier ma tylko 1 karte (zakryta), nie dopisujemy nic.
                    if len(self.dealer_hand.cards) >= 2:
                        visible_card = self.dealer_hand.cards[1]
                        # Pobieramy wartosc tylko tej widocznej karty
                        visible_val = values[visible_card.rank]
                        dealer_text += f": {visible_val}"
                    else:
                        dealer_text += ": ?"
                else:
                    # JESLI KARTY SA ODKRYTE (Dealer Turn / Game Over):
                    # Pokazujemy pelna wartosc reki (suma wszystkich kart)
                    dealer_text += f": {self.dealer_hand.value}"

            draw_label_with_shadow(dealer_text, dealer_x, dealer_cards_y, current_alpha)

            # Napisy Gracza
            for i in range(len(self.player_hands)):
                start_x = 100
                gap = 600
                x_pos = start_x + (i * gap)
                
                # pobieramy obiekt reki zeby znac jej wartosc
                current_hand_obj = self.player_hands[i]

                if len(self.player_hands) > 1:
                    label_text = f"Hand {i + 1}"
                else:
                    label_text = "Player"
                
                # dodajemy wynik do labela po dwukropku
                label_text += f": {current_hand_obj.value}"

                draw_label_with_shadow(label_text, x_pos, player_cards_y, current_alpha)

        # Rysowanie przyciskow
        if self.state == "betting":
            self.btn_deal.draw(self.screen)
        elif self.state == "player_turn":
            current_hand = self.player_hands[self.current_hand_index]
            self.btn_hit.draw(self.screen)
            self.btn_stand.draw(self.screen)

            if len(current_hand.cards) == 2 and self.chips >= current_hand.bet:
                self.btn_double.draw(self.screen)

            if (
                len(current_hand.cards) == 2
                and values[current_hand.cards[0].rank] == values[current_hand.cards[1].rank]
                and self.chips >= self.current_bet
                and len(self.player_hands) < 2
            ):
                self.btn_split.draw(self.screen)

            if len(self.player_hands) == 1 and len(current_hand.cards) == 2:
                self.btn_surrender.draw(self.screen)
        elif self.state == "game_over":
             self.btn_deal.draw(self.screen)
        
        if self.state == "insurance":
            self.draw_insurance_popup()