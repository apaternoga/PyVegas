import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.base_path = os.path.join("assets", "sounds")

        self.volume = 0.5           # Domyślna głośność (0.0 do 1.0)
        self.muted = False          # Czy wyciszono
        self.previous_volume = 0.5  # głośności przed wyciszeniem
    
    def load_common_sounds(self): #dzwieki uzywane czesto
        common_sounds = {
            "click": "click.wav",
            "hover": "hover.wav"
        }
        for name, filename in common_sounds.items():
            self.load_sound(name, filename)

    def load_blackjack_sounds(self): #dzwieki do blackjacka
        blackjack_sounds = {
            "card_place1": "card_place1.ogg",
            "card_place2": "card_place2.ogg",
            "card_place3": "card_place3.ogg",
            "card_place4": "card_place4.ogg",

            "chips_stack": "chips_stack.ogg",
            "split": "split.ogg",

            "win": "chip_drop.wav",
        }
        for name, filename in blackjack_sounds.items():
            self.load_sound(name, filename)
    
    def load_sound(self, name, filename): #zaladuj dzwiek
        path = os.path.join(self.base_path, filename)
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0 if self.muted else self.volume)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Blad przy wczytywaniu dźwięku {filename}: {e}")

    def play_sound(self, name): #odtworz dzwiek
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Dźwięk {name} nie został załadowany.")

    def play_music(self, name): #odtworz muzyke
        path = os.path.join(self.base_path, name)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0 if self.muted else self.volume)
            pygame.mixer.music.play(-1)  # Odtwarzaj w pętli
        except pygame.error as e:
            print(f"Blad przy odtwarzaniu muzyki {name}: {e}")
    
    def set_volume(self, value): #ustaw glosnosc
        # Zabezpieczenie wartości między 0.0 a 1.0
        self.volume = max(0.0, min(1.0, value))
        
        # Jeśli ruszasz suwakiem - zdjecie wyciszenia
        if self.muted and self.volume > 0:
            self.muted = False
            
        self._apply_volume()

    def toggle_mute(self):  #przelacz wyciszenie
        self.muted = not self.muted
        
        if self.muted:
            self.previous_volume = self.volume 
            self.volume = 0.0 
        else:
            self.volume = self.previous_volume # Przywróć
            if self.volume == 0: self.volume = 0.5 # jezeli poprzednia byla 0, ustaw na 0.5
            
        self._apply_volume()

    def _apply_volume(self):  #zastosuj glosnosc do wszystkich dzwiekow
        current_vol = 0 if self.muted else self.volume
        
        # Aktualizuj muzykę
        pygame.mixer.music.set_volume(current_vol)
        
        # Aktualizuj wszystkie załadowane dzwieki
        for sound in self.sounds.values():
            sound.set_volume(current_vol)