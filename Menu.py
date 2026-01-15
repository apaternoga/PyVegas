import os, pygame, sys
from games import blackjack
from games.blackjack import Card
from constants import *
from ui_elements import Button, Button2, BlackjackIcon, Slider 
import screens

class Menu:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # --- SOUND MANAGER ---
        self.sm = sound_manager
        self.sm.play_music("jazz_playlist.mp3")

        self.state = "MENU"
        self.active_game = None
        
        # Suwak inicjujemy głośnością pobraną z Sound Managera
        current_vol = getattr(self.sm, 'volume_music', 0.1) 
        self.vol_slider = Slider(-1, 360, 600, current_vol)
        
        # --- GRAFIKA ---
        try:
            self.bg_image = pygame.image.load(os.path.join("assets", "tlo_menu.jpg")).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        except:
            self.bg_image = None
            
        self.font = pygame.font.Font(os.path.join("assets", "LuckiestGuy-Regular.ttf"), 55)
        self.font_small = pygame.font.Font(os.path.join("assets", "LuckiestGuy-Regular.ttf"), 50)
        self.font_smaller = pygame.font.Font(os.path.join("assets", "LuckiestGuy-Regular.ttf"), 45)

        # --- PRZYCISKI ---
        self.btns = {
            'start':    Button(-1, 320, 380, 90, "START"),
            'settings': Button(-1, 430, 380, 90, "SETTINGS"),
            'exit':     Button(1080, 650, 160, 65, "EXIT"),

            'instr':    Button(-1, 200, 400, 55, "INSTRUCTIONS"),
            'lic':      Button(-1, 300, 400, 55, "LICENSES"),
            'music_m':  Button(-1, 400, 400, 55, "MUSIC"),
            'back':     Button(-1, 580, 300, 60, "BACK"), 
            
            'yes':      Button(490, 420, 140, 50, "YES"),
            'no':       Button(650, 420, 140, 50, "NO"),

            't1':       Button(330, 230, 300, 55, "JAZZ MIX"),
            't2':       Button(650, 230, 300, 55, "LOFI CHILL"),
            'stop':     Button(-1, 450, 400, 50, "SOUND ON / OFF"),

            'bj':       Button2(310, 250, 200, 200, "Blackjack", icon_renderer=BlackjackIcon(Card)),
            'g2':       Button2(540, 250, 200, 200, "Gra 2"),
            'g3':       Button2(770, 250, 200, 200, "Gra 3")
        }

    def update(self):

        event= pygame.event.poll()

        if event.type == pygame.QUIT:
            return "EXIT_APP"

        if self.state == "GRA" and self.active_game:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "GRY"
                self.active_game = None
                
                self.sm.play_music("jazz_playlist.mp3")
            else:
                self.active_game.handle_input(event)
            return True

        if self.state == "MENU":
            if self.btns['start'].is_clicked(event): self.state = "GRY"
            if self.btns['settings'].is_clicked(event): self.state = "SETTINGS"
            if self.btns['exit'].is_clicked(event): self.state = "EXIT"
        
        elif self.state == "EXIT":
            if self.btns['yes'].is_clicked(event): return "EXIT_APP" 
            if self.btns['no'].is_clicked(event): self.state = "MENU"

        elif self.state == "GRY":
            if self.btns['bj'].is_clicked(event):
                return "BLACKJACK"
            if self.btns['back'].is_clicked(event): self.state = "MENU"

        elif self.state == "SETTINGS":
            if self.btns['music_m'].is_clicked(event): self.state = "SETTINGS_MUSIC"
            if self.btns['back'].is_clicked(event): self.state = "MENU"

        elif self.state == "SETTINGS_MUSIC":
            if self.btns['back'].is_clicked(event): self.state = "SETTINGS"
            
            # Obsługa suwaka - przekazujemy wartość do Sound Managera
            if self.vol_slider.handle_event(event):
                self.sm.set_volume_music(self.vol_slider.value)

            # Zmiana playlisty
            if self.btns['t1'].is_clicked(event):
                self.sm.play_music("jazz_playlist.mp3")
            
            if self.btns['t2'].is_clicked(event):
                self.sm.play_music("lofi_playlist.mp3")

            # Mute / Unmute
            if self.btns['stop'].is_clicked(event):
                if hasattr(self.sm, 'toggle_mute'):
                    self.sm.toggle_mute()
                else:
                    # Fallback jeśli nie ma metody toggle_mute
                    current = getattr(self.sm, 'is_muted', False)
                    self.sm.mute(not current)

        return True

    def draw(self):
        if self.state == "GRA" and self.active_game:
            self.active_game.draw()
            return

        # Pobieramy aktualne stany z Managera dla UI
        current_vol = getattr(self.sm, 'volume_music', 0.5)
        is_muted = getattr(self.sm, 'muted', False)

        if self.state == "MENU":
            screens.draw_menu(self.screen, self.bg_image, self.btns, self.font)
        elif self.state == "EXIT":
            screens.draw_exit(self.screen, self.bg_image, self.btns, self.font, self.font_small)
        elif self.state == "SETTINGS":
            screens.draw_settings(self.screen, self.bg_image, self.btns, self.font)
        elif self.state == "SETTINGS_MUSIC":
            # Synchronizujemy wartość suwaka z aktualną głośnością
            self.vol_slider.value = current_vol
            # Przekazujemy volume i mute z sound managera do rysowania
            screens.draw_settings_music(
                self.screen, self.bg_image, self.btns, self.font, self.font_smaller, 
                current_vol, self.vol_slider, is_muted
            )
        elif self.state == "GRY":
            screens.draw_game_placeholder(self.screen, self.bg_image, self.btns, self.font)