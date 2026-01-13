import os, pygame, sys
from games.blackjack import Card
from constants import *
from ui_elements import Button, Button2, BlackjackIcon, Slider 
import screens
from core.settings import *

class Menu:
    def __init__(self, screen, sound_manager):

        self.screen=screen
        try:
            self.bg_image = pygame.image.load(os.path.join("assets", "tlo_menu.jpg")).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.bg_image = None

        # Sound Manager
        self.sm = sound_manager
        self.sm.play_music()
        # Suwak
        self.vol_slider = Slider(100, 330, 600, self.sm.volume_music)

        self.font = pygame.font.SysFont("Arial", 38)
        self.font_small = pygame.font.SysFont("Arial", 35)
        self.font_smaller = pygame.font.SysFont("Arial", 30)

        self.is_fullscreen = False

        # Tworzenie przycisków
        self.btns = {
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
            't1': Button(150, 200, 240, 50, "JAZZ MIX"),
            't2': Button(410, 200, 240, 50, "LOFI CHILL"),
            'stop': Button(-1, 400, 360, 50, "WYCISZ/PRZYWRÓĆ MUZYKĘ"),
            'bj': Button2(50, 200, 200, 200, "Blackjack", icon_renderer=BlackjackIcon(Card)),
            'g2': Button2(300, 200, 200, 200, "Gra 2"),
            'g3': Button2(550, 200, 200, 200, "Gra 3"),
            'playlist1' : Button(100, 230, 290, 50, "JAZZ MIX"),
            'playlist2' : Button(410, 230, 290, 50, "LOFI CASINO"),
            'mute' : Button(-1, 440, 360, 50, "WYCISZ / ODDAJ GŁOS")
        }

        self.state = "MENU"


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "EXIT_APP"

            if self.state == "MENU":
                if self.btns['start'].is_clicked(event): self.state = "GRY"
                if self.btns['settings'].is_clicked(event): self.state = "SETTINGS"
                if self.btns['exit'].is_clicked(event): self.state = "EXIT"

            elif self.state == "EXIT":
                if self.btns['yes'].is_clicked(event): return "EXIT_APP"
                if self.btns['no'].is_clicked(event): self.state = "MENU"
            elif self.state == "GRY":
                if self.btns['bj'].is_clicked(event):
                    return "START_BLACKJACK"
                if self.btns['back'].is_clicked(event): self.state = "MENU"
            elif self.state == "SETTINGS":
                if self.btns['music_m'].is_clicked(event): self.state = "SETTINGS_MUSIC"
                if self.btns['full'].is_clicked(event): self.state = "FULLSCREEN"
                if self.btns['back'].is_clicked(event): self.state = "MENU"
            elif self.state == "FULLSCREEN":
                if self.btns['yes'].is_clicked(event):
                    self.is_fullscreen = not self.is_fullscreen
                    f = (pygame.FULLSCREEN | pygame.SCALED) if self.is_fullscreen else pygame.SCALED
                    self.screen = pygame.display.set_mode((800, 600), f)
                    self.state = "SETTINGS"
                if self.btns['no'].is_clicked(event): self.state = "SETTINGS"

            elif self.state == "SETTINGS_MUSIC":
                if self.btns['back'].is_clicked(event): self.state = "SETTINGS"

                if self.vol_slider.handle_event(event):
                    self.sm.set_volume_music(self.vol_slider.value)

                if self.btns['t1'].is_clicked(event):
                    self.sm.play_music("jazz_playlist.mp3")

                if self.btns['t2'].is_clicked(event):
                    self.sm.play_music("lofi_playlist.mp3")

                if self.btns['stop'].is_clicked(event):
                    self.sm.toggle_mute()
                    self.vol_slider.value = self.sm.volume_music
                    self.vol_slider.handle_rect.centerx = self.vol_slider.rect.left + int(self.vol_slider.rect.width * self.vol_slider.value)
        return None

    def draw(self):
        vol_music = self.sm.volume_music
        muted = self.sm.muted
        # RYSOWANIE
        if self.state == "MENU": screens.draw_menu(self.screen, self.bg_image, self.btns, self.font)
        elif self.state == "EXIT": screens.draw_exit(self.screen, self.bg_image, self.btns, self.font, self.font_small)
        elif self.state == "SETTINGS": screens.draw_settings(self.screen, self.bg_image, self.btns, self.font)
        elif self.state == "SETTINGS_MUSIC": screens.draw_settings_music(self.screen, self.bg_image, self.btns, self.font, self.font_smaller, vol_music, self.vol_slider, muted)
        elif self.state == "FULLSCREEN": screens.draw_fullscreen(self.screen, self.btns, self.font_smaller, self.is_fullscreen)
        elif self.state == "GRY": screens.draw_game_placeholder(self.screen, self.bg_image, self.btns, self.font)
