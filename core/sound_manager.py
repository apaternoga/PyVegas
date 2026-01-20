import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.base_path = os.path.join(base_dir, "assets", "sounds")

        self.volume = 0.5           # Domyślna głośność efektów (0.0 do 1.0)
        self.volume_music = 0.1     # Domyślna głośność muzyki (0.0 do 1.0)
        self.muted = False          # Czy muzyka jest wyciszona (mute dla muzyki)
        self.previous_volume_music = self.volume_music
    
    def load_common_sounds(self): #dzwieki uzywane czesto
        common_sounds = {
            "click": "click.wav",
            "hover": "hover.wav"
        }
        loaded = 0
        for name, filename in common_sounds.items():
            if self.load_sound(name, filename):
                loaded += 1
        print(f"Loaded {loaded}/{len(common_sounds)} common sounds")
        return loaded

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
        loaded = 0
        for name, filename in blackjack_sounds.items():
            if self.load_sound(name, filename):
                loaded += 1
        print(f"Loaded {loaded}/{len(blackjack_sounds)} blackjack sounds")
        return loaded
    
    def _ensure_mixer(self):
        """Ensure the pygame mixer is initialized. Returns True if mixer is ready."""
        if pygame.mixer.get_init():
            return True
        try:
            pygame.mixer.init()
            return True
        except Exception as e:
            print(f"Warning: pygame.mixer not available: {e}")
            return False

    def load_sound(self, name, filename): #zaladuj dzwiek
        if not self._ensure_mixer():
            print(f"Nie można załadować dźwięku '{filename}': mixer niedostępny.")
            return False

        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            print(f"Brak pliku dźwięku: {path}")
            return False
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
            return True
        except Exception as e:
            print(f"Blad przy wczytywaniu dźwięku {filename}: {e}")
            return False

    def play_sound(self, name): #odtworz dzwiek
        if not self._ensure_mixer():
            # If mixer is not available, silently ignore to maintain UX
            print(f"Cannot play sound '{name}': mixer not initialized.")
            return

        if name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception as e:
                print(f"Blad przy odtwarzaniu dźwięku {name}: {e}")
        else:
            print(f"Dźwięk {name} nie został załadowany.")

    def play_music(self, name="jazz_playlist.mp3"): #odtworz muzyke
        if not self._ensure_mixer():
            print(f"Cannot play music '{name}': mixer not initialized.")
            return False

        path = os.path.join(self.base_path, name)
        if not os.path.exists(path):
            print(f"Plik muzyki '{name}' nie istnieje w {self.base_path}.")
            return False
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.0 if self.muted else self.volume_music)
            pygame.mixer.music.play(-1)  # Odtwarzaj w pętli
            return True
        except Exception as e:
            print(f"Blad przy odtwarzaniu muzyki {name}: {e}")
            return False
    
    def set_volume(self, value): #ustaw glosnosc efektow
        self.volume = max(0.0, min(1.0, value))
        self._apply_sound_volume()

    def set_volume_music(self, value): #ustaw glosnosc muzyki
        # Zabezpieczenie wartości między 0.0 a 1.0
        self.volume_music = max(0.0, min(1.0, value))
        
        # Jeśli ruszasz suwakiem - zdjęcie wyciszenia 
        if self.muted and self.volume_music > 0:
            self.muted = False
            
        # Używamy volume_music (nie volume) do ustawienia głośności muzyki
        if self._ensure_mixer():
            pygame.mixer.music.set_volume(0.0 if self.muted else self.volume_music)
        else:
            print("Warning: mixer not initialized; cannot set music volume")

    def toggle_mute(self):  #przelacz wyciszenie muzyki
        self.muted = not self.muted
        if self.muted:
            self.previous_volume_music = self.volume_music
            if self._ensure_mixer():
                pygame.mixer.music.set_volume(0.0)
        else:
            self.volume_music = self.previous_volume_music or 0.1
            if self._ensure_mixer():
                pygame.mixer.music.set_volume(self.volume_music)

    def _apply_sound_volume(self):  #zastosuj glosnosc do dzwiekow (efekty)
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
