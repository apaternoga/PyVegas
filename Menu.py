import os, pygame, sys
from games import blackjack
from games.blackjack import Card
from constants import *
from ui_elements import Button, Button2, BlackjackIcon
import screens

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.SCALED)
pygame.display.set_caption("Nasza Gra - Menu")
font = pygame.font.SysFont("Arial", 38)
font_small = pygame.font.SysFont("Arial", 35)
font_smaller = pygame.font.SysFont("Arial", 30)

# Dźwięki
try:
    s_hover = pygame.mixer.Sound(os.path.join("assets", "hover.wav"))
    s_click = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
except:
    class Dummy:
        def play(self): pass
    s_hover = s_click = Dummy()

bg_image = None
try:
    loaded_bg = pygame.image.load(os.path.join("assets", "tlo_menu.jpg"))
    bg_image = pygame.transform.scale(loaded_bg, (800, 600))
except: pass

# Tworzenie przycisków
btns = {
    'start': Button(-1, 250, 200, 50, "START"),
    'exit': Button(-1, 350, 200, 50, "WYJŚCIE"),
    'settings': Button(-1, 450, 200, 50, "USTAWIENIA"),
    'back': Button(-1, 500, 300, 60, "COFNIJ"),
    'yes': Button(250, 300, 140, 50, "TAK"),
    'no': Button(410, 300, 140, 50, "NIE"),
    'instr': Button(-1, 150, 400, 50, "INSTRUKCJE"),
    'full': Button(-1, 220, 400, 50, "PEŁNY EKRAN/OKNO"),
    'lic': Button(-1, 290, 400, 50, "LICENCJE"),
    'music_m': Button(-1, 360, 400, 50, "MUZYKA"),
    't1': Button(150, 200, 240, 50, "UTWÓR 1"),
    't2': Button(410, 200, 240, 50, "UTWÓR 2"),
    'stop': Button(-1, 420, 340, 50, "WYCISZ MUZYKĘ"),
    'bj': Button2(50, 200, 200, 200, "Blackjack", icon_renderer=BlackjackIcon(Card)),
    'g2': Button2(300, 200, 200, 200, "Gra 2"),
    'g3': Button2(550, 200, 200, 200, "Gra 3")
}

state = "MENU"
volume = 0.5
current_track = "Brak"
is_fullscreen = False
active_game = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if state == "MENU":
            if btns['start'].is_clicked(event, s_click): state = "GRY"
            if btns['settings'].is_clicked(event, s_click): state = "SETTINGS"
            if btns['exit'].is_clicked(event, s_click): state = "EXIT"
        
        elif state == "EXIT":
            if btns['yes'].is_clicked(event, s_click): running = False
            if btns['no'].is_clicked(event, s_click): state = "MENU"

        elif state == "GRY":
            if btns['bj'].is_clicked(event, s_click):
                active_game = blackjack.BlackjackGame(screen)
                state = "GRA"
            if btns['back'].is_clicked(event, s_click): state = "MENU"

        elif state == "SETTINGS":
            if btns['music_m'].is_clicked(event, s_click): state = "SETTINGS_MUSIC"
            if btns['full'].is_clicked(event, s_click): state = "FULLSCREEN"
            if btns['back'].is_clicked(event, s_click): state = "MENU"

        elif state == "FULLSCREEN":
            if btns['yes'].is_clicked(event, s_click):
                is_fullscreen = not is_fullscreen
                f = (pygame.FULLSCREEN | pygame.SCALED) if is_fullscreen else pygame.SCALED
                screen = pygame.display.set_mode((800, 600), f)
                state = "SETTINGS"
            if btns['no'].is_clicked(event, s_click): state = "SETTINGS"

        elif state == "SETTINGS_MUSIC":
            if btns['back'].is_clicked(event, s_click): state = "SETTINGS"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: 
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_LEFT: 
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
            if btns['stop'].is_clicked(event, s_click):
                pygame.mixer.music.stop()
                current_track = "Wyciszono"

        elif state == "GRA":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "GRY"; active_game = None
            if active_game: active_game.handle_input(event)

    # RYSOWANIE
    if state == "MENU": screens.draw_menu(screen, bg_image, btns, font)
    elif state == "EXIT": screens.draw_exit(screen, bg_image, btns, font, font_small)
    elif state == "SETTINGS": screens.draw_settings(screen, bg_image, btns, font)
    elif state == "SETTINGS_MUSIC": screens.draw_settings_music(screen, bg_image, btns, font, volume, current_track)
    elif state == "FULLSCREEN": screens.draw_fullscreen(screen, btns, font_smaller, is_fullscreen)
    elif state == "GRY": screens.draw_game_placeholder(screen, bg_image, btns, font)
    elif state == "GRA":
        if active_game: active_game.draw()
        else: screens.draw_game_placeholder(screen, bg_image, btns, font)

    pygame.display.flip()

pygame.quit()