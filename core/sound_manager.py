import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.base_path = os.path.join("assets", "sounds")
    
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
            pygame.mixer.music.play(-1)  # Odtwarzaj w pętli
        except pygame.error as e:
            print(f"Blad przy odtwarzaniu muzyki {name}: {e}")