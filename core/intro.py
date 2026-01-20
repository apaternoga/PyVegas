import pygame
import os
import sys

# --- USTAWIENIA ---
WIDTH, HEIGHT = 1280, 720 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_FRAME = (180, 180, 180) 
DARK_GRAY = (40, 40, 40)
CYAN = (0, 245, 255)

class IntroSequence:
    def __init__(self, screen, sm=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.stage = 1 
        self.timer_start = pygame.time.get_ticks()

        #Dźwięk syczenia
        self.sm = sm
        sm.load_sound('hiss', 'hiss.mp3')
        
        # Logo 
        self.logo = self.load_and_scale_logo(width=700) 
        
        # Zmienne do efektu fade
        self.fade_alpha = 255 
        self.fade_state = "FADE_IN" 
        self.fade_speed = 15 
        self.fade_surface = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surface.fill(BLACK)

        # Czas trwania slajdów (w ms)
        self.durations = {
            1: 4000, 
            2: 7000, 
            3: 3000  
        }

        # Czcionki
        try:
            path = os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf")
            self.font_main = pygame.font.Font(path, 36)
            self.font_small = pygame.font.Font(path, 28)
            self.font_final = pygame.font.Font(path, 70)
        except:
            self.font_main = pygame.font.SysFont("Arial", 32, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 24, bold=True)
            self.font_final = pygame.font.SysFont("Arial", 60, bold=True)

    def load_and_scale_logo(self, width):
        try:
            path = os.path.join("assets", "images", "logo_trans.png") 
            img = pygame.image.load(path).convert_alpha()
            ratio = width / img.get_width()
            new_height = int(img.get_height() * ratio)
            return pygame.transform.smoothscale(img, (width, new_height))
        except: return None

    def load_sound(self, filename):
        try:
            path = os.path.join("assets", "images", filename)
            return pygame.mixer.Sound(path)
        except: return None

    def run(self):
        running = True
        self.timer_start = pygame.time.get_ticks()

        while running:
            # --- 1. OBSŁUGA ZDARZEŃ ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                
                # OBSŁUGA SPACJI (SKIP)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Jeśli nie jesteśmy już w trakcie wygaszania,
                        # wymuś wygaszanie, aby przejść do następnego slajdu
                        if self.fade_state != "FADE_OUT":
                            self.fade_state = "FADE_OUT"
                
            # --- 2. RYSOWANIE TREŚCI ---
            self.screen.fill(BLACK)

            if self.stage == 1:
                # SLAJD 1: Tekst WYŚRODKOWANY
                lines = ["They say", "99% of gamblers quit", "right before their biggest win ..."]
                spacing = 60
                total_height = len(lines) * spacing
                start_y = (HEIGHT - total_height) // 2
                
                for i, line in enumerate(lines):
                    surf = self.font_main.render(line, True, WHITE)
                    rect = surf.get_rect(center=(WIDTH // 2, start_y + i * spacing))
                    self.screen.blit(surf, rect)
                
            elif self.stage == 2:
                # SLAJD 2: Projekt i Autorzy (PO ANGIELSKU)
                header_lines = [
                    "Game created as part of a programming project",
                    "by Computer Science students of the",
                    "University of Wroclaw."
                ]
                authors_list = [
                    "Adrian Paternoga", "Miłosz Kiedrzyński", 
                    "Patryk Iżbicki", "Adam Zalewski", 
                    "Borys Kaczka", "Filip Liskowski"
                ]

                curr_y = 120
                for line in header_lines:
                    surf = self.font_main.render(line, True, WHITE)
                    self.screen.blit(surf, surf.get_rect(center=(WIDTH // 2, curr_y)))
                    curr_y += 50

                curr_y += 40
                label_surf = self.font_main.render("Authors:", True, CYAN)
                self.screen.blit(label_surf, label_surf.get_rect(center=(WIDTH // 2, curr_y)))

                curr_y += 60
                for name in authors_list:
                    name_surf = self.font_small.render(name, True, WHITE)
                    self.screen.blit(name_surf, name_surf.get_rect(center=(WIDTH // 2, curr_y)))
                    curr_y += 40
                
            elif self.stage == 3:
                # SLAJD 3: Logo + GOOD LUCK!
                if self.logo:
                    logo_rect = self.logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
                    self.screen.blit(self.logo, logo_rect)
                
                txt = self.font_final.render("GOOD LUCK!", True, WHITE)
                self.screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 600)))

            # --- 3. OBSŁUGA FADE ---
            if self.fade_state == "FADE_IN":
                self.fade_alpha -= self.fade_speed
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fade_state = "DISPLAY"
                    self.timer_start = pygame.time.get_ticks()

            elif self.fade_state == "DISPLAY":
                duration = self.durations.get(self.stage, 3000)
                if pygame.time.get_ticks() - self.timer_start > duration:
                    self.fade_state = "FADE_OUT"

            elif self.fade_state == "FADE_OUT":
                self.fade_alpha += self.fade_speed
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.stage += 1
                    
                    if self.stage > 3:
                        return "FINISHED"
                    
                    # Jeśli przechodzimy z 2 na 3 slajd, graj syczenie
                    if self.stage == 3:
                        self.sm.play_sound('hiss')
                        
                    self.fade_state = "FADE_IN"

            # Rysowanie czarnej nakładki z odpowiednim alpha
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)
