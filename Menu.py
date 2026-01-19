import os, pygame, sys
from games import blackjack
from games.blackjack import Card
from constants import *
from ui_elements import Button, Button2, BlackjackIcon, Slider 
import screens

# Zmienne muzyczne
is_muted = False
saved_volume = 0.05
current_playlist = "Brak"

# Ustawienie Suwaka
vol_slider = Slider(-1, 360, 600, saved_volume)

# Ustawienia ekranu i czcionki
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Nasza Gra - Menu")
font = pygame.font.Font(os.path.join("assets", "LuckiestGuy-Regular.ttf"), 55)
font_small = pygame.font.Font(os.path.join("assets", "LuckiestGuy-Regular.ttf"), 50)
font_smaller = pygame.font.Font(os.path.join("assets", "LuckiestGuy-Regular.ttf"), 45)

# Dźwięki
try:
    s_hover = pygame.mixer.Sound(os.path.join("assets", "hover.wav"))
    s_click = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
except:
    class Dummy:
        def play(self): pass
    s_hover = s_click = Dummy()

# Ładowanie tła i innych plików
bg_image = None
try:
    loaded_bg = pygame.image.load(os.path.join("assets", "tlo_menu.jpg"))
    bg_image = pygame.transform.scale(loaded_bg, (WIDTH, HEIGHT))
except: pass

btns = {
    # Menu Główne
    'start':    Button(-1, 250, 200, 50, "START"),
    'exit':     Button(1080, 650, 160, 65, "EXIT"),
    'settings': Button(-1, 450, 200, 50, "SETTINGS"),
    
    # Ustawienia 
    'instr':    Button(-1, 200, 400, 55, "INSTRUKCJE"),
    'lic':      Button(-1, 300, 400, 55, "LICENCJE"),
    'music_m':  Button(-1, 400, 400, 55, "MUZYKA"),
    'back':     Button(-1, 580, 300, 60, "COFNIJ"), 
    
    # Wyjście
    'yes':      Button(490, 420, 140, 50, "YES"),
    'no':       Button(650, 420, 140, 50, "NO"),

    # Muzyka
    't1':       Button(390, 230, 240, 50, "JAZZ MIX"),
    't2':       Button(650, 230, 240, 50, "LOFI CHILL"),
    'stop':     Button(-1, 450, 400, 50, "WYCISZ / PRZYWRÓĆ MUZYKĘ"),

    # Minigierki
    'bj':       Button2(310, 250, 200, 200, "Blackjack", icon_renderer=BlackjackIcon(Card)),
    'g2':       Button2(540, 250, 200, 200, "Gra 2"),
    'g3':       Button2(770, 250, 200, 200, "Gra 3")
}

# Jakieś zmienne (niektóre niepotrzebne!)
state = "MENU"
volume = 0.05
current_track = "Brak"
is_fullscreen = False
active_game = None
running = True

# --- AUTOSTART MUZYKI ---
try:
    pygame.mixer.music.load(os.path.join("assets", "jazz_playlist.mp3"))
    pygame.mixer.music.set_volume(volume) 
    pygame.mixer.music.play(-1)           
except:
    print("Ostrzeżenie: Nie udało się włączyć muzyki na starcie (brak pliku?)")

# Główna pętla z różnymi stanami gry 
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
            if btns['back'].is_clicked(event, s_click): state = "MENU"

        elif state == "FULLSCREEN":
            if btns['yes'].is_clicked(event, s_click):
                is_fullscreen = not is_fullscreen
                f = (pygame.FULLSCREEN | pygame.SCALED) if is_fullscreen else pygame.SCALED
                screen = pygame.display.set_mode((WIDTH, HEIGHT), f)
                state = "SETTINGS"
            if btns['no'].is_clicked(event, s_click): state = "SETTINGS"

        elif state == "SETTINGS_MUSIC":
            if btns['back'].is_clicked(event, s_click): state = "SETTINGS"
            
            if vol_slider.handle_event(event):
                volume = vol_slider.value
                if not is_muted:
                    pygame.mixer.music.set_volume(volume)

            # Ładowanie plików
            if btns['t1'].is_clicked(event, s_click):
                try:
                    pygame.mixer.music.load(os.path.join("assets", "jazz_playlist.mp3"))
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(volume)
                    is_muted = False
                except: print("Brak pliku jazz_playlist.mp3")

            if btns['t2'].is_clicked(event, s_click):
                try:
                    pygame.mixer.music.load(os.path.join("assets", "lofi_playlist.mp3"))
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(volume)
                    is_muted = False
                except: print("Brak pliku lofi_playlist.mp3")

            if btns['stop'].is_clicked(event, s_click):
                is_muted = not is_muted
                pygame.mixer.music.set_volume(0 if is_muted else volume)

        elif state == "GRA":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "GRY"; active_game = None
            if active_game: active_game.handle_input(event)

    # RYSOWANIE
    if state == "MENU": screens.draw_menu(screen, bg_image, btns, font)
    elif state == "EXIT": screens.draw_exit(screen, bg_image, btns, font, font_small)
    elif state == "SETTINGS": screens.draw_settings(screen, bg_image, btns, font)
    elif state == "SETTINGS_MUSIC": screens.draw_settings_music(screen, bg_image, btns, font, font_smaller, volume, vol_slider, is_muted)
    elif state == "FULLSCREEN": screens.draw_fullscreen(screen, btns, font_smaller, is_fullscreen)
    elif state == "GRY": screens.draw_game_placeholder(screen, bg_image, btns, font)
    elif state == "GRA":
        if active_game: active_game.draw()
        else: screens.draw_game_placeholder(screen, bg_image, btns, font)

    pygame.display.flip()

pygame.quit()