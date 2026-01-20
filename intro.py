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
AUTO_SKIP_TIME = 10000 # 10 sekund w milisekundach

class IntroSequence:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.stage = 1 
        self.timer_start = pygame.time.get_ticks()
        
        # Logo 
        self.logo = self.load_and_scale_logo(width=700) 
        
        # Dźwięk syczenia
        self.hiss_sound = self.load_sound("hiss.mp3")
        
        # Przycisk SKIP 
        self.skip_btn_rect = pygame.Rect(WIDTH - 200, HEIGHT - 100, 160, 60)
        
        # Czcionki
        try:
            path = os.path.join("assets", "LuckiestGuy-Regular.ttf")
            self.font_main = pygame.font.Font(path, 36)
            self.font_small = pygame.font.Font(path, 28)
            self.font_final = pygame.font.Font(path, 70)
        except:
            self.font_main = pygame.font.SysFont("Arial", 32, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 24, bold=True)
            self.font_final = pygame.font.SysFont("Arial", 60, bold=True)

    def load_and_scale_logo(self, width):
        try:
            path = os.path.join("assets", "logo_trans.png") 
            img = pygame.image.load(path).convert_alpha()
            ratio = width / img.get_width()
            new_height = int(img.get_height() * ratio)
            return pygame.transform.smoothscale(img, (width, new_height))
        except: return None

    def load_sound(self, filename):
        try:
            path = os.path.join("assets", filename)
            return pygame.mixer.Sound(path)
        except: return None

    def handle_advance(self):
        # Jeśli przechodzimy z 2 na 3 slajd, graj syczenie
        if self.stage == 2 and self.hiss_sound:
            self.hiss_sound.play()
            
        self.stage += 1
        self.timer_start = pygame.time.get_ticks() # Reset timera dla nowego slajdu
        
        if self.stage > 3:
            return "FINISHED"
        return None

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()

            # --- 1. OBSŁUGA ZDARZEŃ ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        res = self.handle_advance()
                        if res: return res
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.skip_btn_rect.collidepoint(event.pos):
                        res = self.handle_advance()
                        if res: return res

            # --- 2. AUTOMATYCZNY SKIP PO 10 SEKUNDACH ---
            if current_time - self.timer_start > AUTO_SKIP_TIME:
                res = self.handle_advance()
                if res: return res

            # --- 3. RYSOWANIE ---
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

            # Przycisk SKIP/START
            pygame.draw.rect(self.screen, DARK_GRAY, self.skip_btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, GRAY_FRAME, self.skip_btn_rect, 3, border_radius=8)
            btn_label = "SKIP" if self.stage < 3 else "START"
            label_surf = self.font_main.render(btn_label, True, WHITE)
            self.screen.blit(label_surf, label_surf.get_rect(center=self.skip_btn_rect.center))

            pygame.display.flip()
            self.clock.tick(60)

