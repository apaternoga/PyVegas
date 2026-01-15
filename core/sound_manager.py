import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        bpath = os.path.dirname(os.path.dirname(__file__))
        self.base_path = os.path.join(bpath, "assets", "sounds")

        self.volume = 0.5           # Domyślna głośność (0.0 do 1.0)
        self.volume_music = 0.5    # Domyślna głośność muzyki (0.0 do 1.0)
        self.muted = False          # Czy wyciszono
        self.previous_volume = 0.5  # głośności przed wyciszeniem
    
    def load_common_sounds(self): #dzwieki uzywane czesto
        common_sounds = {
            "click": "click.wav",
            "hover": "hover.wav",
            "win": "chip_drop.wav",
            "lose": "chip_drop.wav",
        }
        for name, filename in common_sounds.items():
            self.load_sound(name, filename)

    def load_blackjack_sounds(self): #dzwieki do blackjacka
        blackjack_sounds = {
            "card_place1": "card_place1.ogg",
            "card_place2": "card_place2.ogg",
            "card_place3": "card_place3.ogg",
            "card_place4": "card_place4.ogg",
            "deal1": "deal1.ogg",
            "deal2": "deal2.ogg",
            "deal3": "deal3.ogg",
            "deal4": "deal4.ogg",

            "chips_stack": "chips_stack.ogg",
            "split": "split.ogg",
        }
        for name, filename in blackjack_sounds.items():
            self.load_sound(name, filename)
    
    def load_sound(self, name, filename): #zaladuj dzwiek
        path = os.path.join(self.base_path, filename)
        if not os.path.isfile(path):
            print(f"Plik dźwiękowy nie istnieje: {path}")
            sound=None
            self.sounds[name]=sound
            return
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.volume)
        self.sounds[name] = sound

    def play_sound(self, name): #odtworz dzwiek
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Dźwięk {name} nie został załadowany.")

    def play_music(self, name="jazz_playlist.mp3"): #odtworz muzyke
        path = os.path.join(self.base_path, name)
        if not os.path.isfile(path):
            print(f"Plik muzyczny nie istnieje: {path}")
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0 if self.muted else self.volume_music)
        pygame.mixer.music.play(-1)  # Odtwarzaj w pętli
    
    def set_volume(self, value): #ustaw glosnosc
        # Zabezpieczenie wartości między 0.0 a 1.0
        self.volume = max(0.0, min(1.0, value))
        self._apply_volume()

    def set_volume_music(self, value): #ustaw glosnosc muzyki
        # Zabezpieczenie wartości między 0.0 a 1.0
        self.volume_music = max(0.0, min(1.0, value))
        
        # Jeśli ruszasz suwakiem - zdjęcie wyciszenia 
        if self.muted and self.volume_music > 0:
            self.muted = False
            
        # Używamy volume_music (nie volume) do ustawienia głośności muzyki
        current_vol = 0.0 if self.muted else self.volume_music
        pygame.mixer.music.set_volume(current_vol)

    def toggle_mute(self):  #przelacz wyciszenie
        self.muted = not self.muted
        
        if self.muted:
            self.previous_volume = self.volume_music 
            self.volume_music = 0.0 
        else:
            self.volume_music = self.previous_volume # Przywróć
            if self.volume_music == 0: self.volume_music = 0.5 # jezeli poprzednia byla 0, ustaw na 0.5
            
        pygame.mixer.music.set_volume(self.volume_music)

    def _apply_volume(self):  #zastosuj glosnosc do wszystkich dzwiekow

        for sound in self.sounds.values():
            sound.set_volume(self.volume)
