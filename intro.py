import pygame
import os
import sys

# --- USTAWIENIA ---
WIDTH, HEIGHT = 800, 700 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_FRAME = (180, 180, 180) 
DARK_GRAY = (40, 40, 40)

class IntroSequence:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.stage = 1 
        
        # Logo (600px szerokości)
        self.logo = self.load_and_scale_logo(width=600) 
        
        # Przycisk SKIP
        self.skip_btn_rect = pygame.Rect(WIDTH - 180, HEIGHT - 80, 150, 50)
        
        # Czcionki
        try:
            path = os.path.join("assets", "LuckiestGuy-Regular.ttf")
            self.font_main = pygame.font.Font(path, 30)
            self.font_small = pygame.font.Font(path, 24) # Nieco mniejsza dla listy autorów
            self.font_final = pygame.font.Font(path, 55)
        except:
            self.font_main = pygame.font.SysFont("Arial", 26, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 20, bold=True)
            self.font_final = pygame.font.SysFont("Arial", 48, bold=True)

    def load_and_scale_logo(self, width):
        try:
            path = os.path.join("assets", "logo_trans.png") 
            img = pygame.image.load(path).convert_alpha()
            ratio = width / img.get_width()
            new_height = int(img.get_height() * ratio)
            return pygame.transform.smoothscale(img, (width, new_height))
        except:
            return None

    def handle_advance(self):
        self.stage += 1
        if self.stage > 3:
            return "FINISHED"
        return None

    def run(self):
        running = True
        while running:
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

            # --- RYSOWANIE ---
            self.screen.fill(BLACK)

            if self.stage == 1:
                # SLAJD 1: Tekst w lewym górnym rogu
                lines = ["They say", "99% of gamblers quit", "right before their biggest win..."]
                margin_x, margin_y, spacing = 50, 50, 45
                for i, line in enumerate(lines):
                    text_surf = self.font_main.render(line, True, WHITE)
                    self.screen.blit(text_surf, (margin_x, margin_y + i * spacing))
                
            elif self.stage == 2:
                # --- SLAJD 2: Projekt i Autorzy ---
                header_lines = [
                    "Gra stworzona w ramach projektu",
                    "programistycznego studentów informatyki",
                    "Uniwersytetu Wrocławskiego."
                ]
                
                authors_label = "Autorzy:"
                authors_list = [
                    "Adrian Paternoga", "Miłosz Kiedrzyński", 
                    "Patryk Iżbicki", "Adam Zalewski", 
                    "Borys Kaczka", "Filip Liskowski"
                ]

                # Rysowanie nagłówka (Projekt UWr)
                curr_y = 100
                for line in header_lines:
                    surf = self.font_main.render(line, True, WHITE)
                    self.screen.blit(surf, surf.get_rect(center=(WIDTH // 2, curr_y)))
                    curr_y += 45

                # Rysowanie napisu "Autorzy:"
                curr_y += 40
                label_surf = self.font_main.render(authors_label, True, (0, 245, 255)) # Kolor błękitny dla wyróżnienia
                self.screen.blit(label_surf, label_surf.get_rect(center=(WIDTH // 2, curr_y)))

                # Rysowanie listy autorów
                curr_y += 50
                for name in authors_list:
                    name_surf = self.font_small.render(name, True, WHITE)
                    self.screen.blit(name_surf, name_surf.get_rect(center=(WIDTH // 2, curr_y)))
                    curr_y += 35
                
            elif self.stage == 3:
                # SLAJD 3: Logo + GOOD LUCK!
                if self.logo:
                    logo_rect = self.logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
                    self.screen.blit(self.logo, logo_rect)
                
                txt = self.font_final.render("GOOD LUCK!", True, WHITE)
                self.screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 580)))

            # Przycisk SKIP/START
            pygame.draw.rect(self.screen, DARK_GRAY, self.skip_btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, GRAY_FRAME, self.skip_btn_rect, 2, border_radius=5)
            btn_label = "SKIP" if self.stage < 3 else "START"
            label_surf = self.font_main.render(btn_label, True, WHITE)
            self.screen.blit(label_surf, label_surf.get_rect(center=self.skip_btn_rect.center))

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyVegas Intro")
    intro = IntroSequence(test_screen)
    intro.run()
    pygame.quit()