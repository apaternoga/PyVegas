import os
import pygame
import sys
from games import blackjack
from games.blackjack import Card

# 1. Inicjalizacja ekranu
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Nasza Gra - Menu")
font = pygame.font.SysFont("Arial", 40)

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)  # Dodatkowy kolor dla efektu najechania

#wczytanie dzwiekow
try:
    sound_hover = pygame.mixer.Sound(os.path.join("assets", "hover.wav"))
    sound_click = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
    sound_hover.set_volume(0.5)
    sound_click.set_volume(0.5)
except FileNotFoundError:
    print("Ostrzeżenie: Nie znaleziono plików dźwiękowych w folderze assets!")

    class DummySound:
        def play(self):
            pass

    sound_hover = DummySound()
    sound_click = DummySound()

bg_image = None # Wczytanie tła menu

try:
    loaded_bg = pygame.image.load(os.path.join("assets", "tlo_menu.jpg"))
    bg_image = pygame.transform.scale(loaded_bg, (800, 600))
except FileNotFoundError:
    print("Ostrzeżenie: Nie znaleziono pliku tlo_menu.jpg w assets")


# --- KLASA PRZYCISKU (Tu pracuje osoba od grafiki i logiki) ---
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY

        self.is_hovered = False

    def draw(self, surface):
        # Pobierz pozycję myszki
        mouse_pos = pygame.mouse.get_pos()

        # LOGIKA GRAFIKA: Zmiana koloru jeśli myszka najeżdża na przycisk
        # zmiana: dodanie logiki dźwiękowej
        if self.rect.collidepoint(mouse_pos):
            current_color = DARK_GRAY
            if not self.is_hovered:
                sound_hover.play()
                self.is_hovered = True
        else:
            current_color = self.color
            self.is_hovered = False

        # Rysowanie prostokąta
        pygame.draw.rect(surface, current_color, self.rect)

        # Rysowanie tekstu (wyśrodkowanego automatycznie!)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # LOGIKA PROGRAMISTY: Sprawdź, czy kliknięto w ten przycisk
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sound_click.play()
                return True
        return False
    
class BlackjackIcon:
    def __init__(self):
        self.card1 = Card("Spades", "Ace")
        self.card2 = Card("Hearts", "Jack")

    def draw(self, surface, center_x, center_y, offset):
        scale = 0.65
        h = 150*scale
        w = 100*scale
        draw_y = center_y - (h / 2) - 30 #ile do gory (15)
        self.card1.draw(surface, center_x - offset -30, draw_y, w, h) #ukryta
        self.card2.draw(surface, center_x + offset -30, draw_y, w, h) #widoczna

class Button2:
    def __init__(self, x, y, width, height, text, icon_renderer=None):
        
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy() 
        self.text = text

        self.icon_renderer = icon_renderer 
        self.anim_offset = 0 
        self.max_offset = 40   # Maksymalny offset dla animacji
        
        # KOLORY
        self.base_color = (52, 152, 219)  # Jasny niebieski
        self.hover_color = (41, 128, 185) # Ciemny niebieski
        self.text_color = (255, 255, 255) # Biały
        
        self.is_hovered = False 
        
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        
        # LOGIKA NAJECHANIA I ANIMACJI
        if self.original_rect.collidepoint(mouse_pos):
            current_color = self.hover_color
            #animacia powiekszenia
            self.rect = self.original_rect.inflate(20, 20)

            #animacja ikon
            if self.anim_offset < self.max_offset:
                self.anim_offset += 2
        
            # Dźwięk 
            if not self.is_hovered:
                sound_hover.play()
                self.is_hovered = True
        else:
            if self.anim_offset > 0:
                self.anim_offset -= 2
            current_color = self.base_color
            self.rect = self.original_rect.copy()
            self.is_hovered = False
        
        # RYSOWANIE - prostokąt z zaokrąglonymi rogami
        pygame.draw.rect(surface, current_color, self.rect, border_radius=15)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=15)

        # Rysowanie ikony, jeśli istnieje
        if self.icon_renderer:
            self.icon_renderer.draw(surface, self.rect.centerx, self.rect.centery, self.anim_offset)
        
        # Rysowanie tekstu
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(midbottom=(self.rect.centerx, self.rect.bottom - 30))
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sound_click.play()
                return True
        return False

# TWORZENIE PRZYCISKÓW
btn_start = Button(300, 250, 200, 50, "START")
btn_exit = Button(300, 350, 200, 50, "EXIT")
btn_autorzy = Button(300, 450, 200, 50, "CREDITS")

btn_bj = Button2(50, 200, 200, 200, "Blackjack", icon_renderer=BlackjackIcon())
btn_g2 = Button2(300, 200, 200, 200, "Gra 2")
btn_g3 = Button2(550, 200, 200, 200, "Gra 3")
btn_back = Button(250, 500, 300, 60, "BACK")

state = "MENU"

active_game = None


def draw_menu():
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(WHITE)
    title_text = font.render("MENU GŁÓWNE", True, WHITE)
    screen.blit(title_text, (275, 100))

    btn_start.draw(screen)
    btn_exit.draw(screen)
    btn_autorzy.draw(screen)


def draw_game_placeholder():
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((0, 255, 0))  # Zielony
    text = font.render("MINIGIERKI", True, WHITE)
    btn_bj.draw(screen)
    btn_g2.draw(screen)
    btn_g3.draw(screen)
    btn_back.draw(screen)
    screen.blit(text, (300, 75))


def draw_credits():
    screen.fill(WHITE)
    title_text = font.render("CREDITS", True, BLACK)
    screen.blit(title_text, (350, 50))

    y_offset = 150
    for line in credits_text:
        line_surf = credits_font.render(line, True, BLACK)
        screen.blit(line_surf, (100, y_offset))
        y_offset += 30

    btn_credits_back.draw(screen)


credits_font = pygame.font.SysFont("Arial", 24)
btn_credits_back = Button(300, 500, 200, 50, "BACK")
credits_text = []


def load_credits():
    lines = []
    try:
        with open("CREDITS.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["CREDITS.txt not found."]

    return [line.strip() for line in lines]


credits_text = load_credits()

# 2. Główna pętla programu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "MENU":

            if btn_start.is_clicked(event):
                state = "GRY"

            if btn_autorzy.is_clicked(event):
                state = "CREDITS"

            if btn_exit.is_clicked(event):
                running = False

        elif state == "GRY":
            if btn_bj.is_clicked(event):
                active_game = blackjack.BlackjackGame(screen)
                state = "GRA"
            if btn_g2.is_clicked(event):
                print("Wybrano Grę 2")
                state = "GRA"
            if btn_g3.is_clicked(event):
                print("Wybrano Grę 3")
                state = "GRA"
            if btn_back.is_clicked(event):
                state = "MENU"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

        elif state == "GRA":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "GRY"
                    active_game = None

                if active_game:
                    active_game.handle_input(event)

        elif state == "CREDITS":
            if btn_credits_back.is_clicked(event):
                state = "MENU"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

    if state == "MENU":
        draw_menu()
    elif state == "GRY":
        draw_game_placeholder()
    elif state == "GRA":
        if active_game:
            active_game.draw()
        else:
            draw_game_placeholder()
    elif state == "CREDITS":
        draw_credits()

    pygame.display.flip()

pygame.quit()
sys.exit()
