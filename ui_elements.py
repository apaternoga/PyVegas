import pygame
import os
import random
from constants import WHITE, BLACK, GRAY, DARK_GRAY, WIDTH
from core.settings import TABLE_COLOR
from games.blackjack import Card


class Manager:
    sm = None

    # Mój przycisk główny do ustawień (Patryk)
class Button:
    def __init__(self, x, y, width, height, text):
        self.text = text
        # Automatyczne centrowanie w poziomie jeśli x == -1
        if x == -1:
            x = (WIDTH - width) // 2
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.is_hovered = False

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = DARK_GRAY
            if not self.is_hovered:
                if Manager.sm: Manager.sm.play_sound('hover')
                self.is_hovered = True
        else:
            current_color = self.color
            self.is_hovered = False
        
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)

        if self.text == "EXIT":
         pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        
        # Centrowanie tekstu wewnątrz przycisku
        text_surf = font.render(self.text, True, BLACK)
        text_x = self.rect.centerx
        text_y = self.rect.centery +7
        text_rect = text_surf.get_rect(center=(text_x, text_y))
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if Manager.sm: Manager.sm.play_sound('click')
                return True
        return False

# Przycisk wewnątrz gierek po kliknięciu start
class Button2:
    def __init__(self, x, y, width, height, text, icon_renderer=None):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy() 
        self.text = text
        self.icon_renderer = icon_renderer 
        self.anim_offset = 0 
        self.max_offset = 50 
        self.base_color = TABLE_COLOR                  #(52, 152, 219)
        self.hover_color = (41, 128, 185)
        self.text_color = (255, 255, 255)
        self.is_hovered = False 
        
    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.original_rect.collidepoint(mouse_pos):
            current_color = self.hover_color
            self.rect = self.original_rect.inflate(20, 20)
            current_color = tuple(max(0, c - 30) for c in current_color)  # Zciemniaj kolor o 30
            inner_border_color = (0, 0, 0)
            if self.anim_offset < self.max_offset: self.anim_offset += 4
            if not self.is_hovered:
                if Manager.sm: Manager.sm.play_sound('hover')
                self.is_hovered = True
        else:
            if self.anim_offset > 0: self.anim_offset -= 4
            current_color = self.base_color
            self.rect = self.original_rect.copy()
            self.is_hovered = False
            inner_border_color = (30, 30, 30)
            
        pygame.draw.rect(surface, current_color, self.rect, border_radius=15)

        inner_rect = self.rect.inflate(-10, -10) 
        pygame.draw.rect(surface, inner_border_color, inner_rect, 2, border_radius=10)

        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=15)
        
        # Rysowanie ikony dokładnie na środku przycisku
        if self.icon_renderer:
            self.icon_renderer.draw(surface, self.rect.centerx, self.rect.centery, self.anim_offset, self.is_hovered)
            
        # Centrowanie tekstu w dolnej części przycisku
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(midbottom=(self.rect.centerx, self.rect.bottom - 10))
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if Manager.sm: Manager.sm.play_sound('click')
                return True
        return False

class BlackjackIcon:
    def __init__(self):
        self.card1 = Card("Spades", "Ace")
        self.card2 = Card("Hearts", "Jack")
        # te wartosci sa nadpisywane w draw
        self.x, self.y = 0, 0
        
    def draw(self, surface, center_x, center_y, offset, is_hovered):
        if is_hovered: scale =75+offset//10
        else: scale = 70+offset//10
        h, w = 150*scale//100, 100*scale//100
        draw_y = center_y - (h / 2) -35
        
        # Centrowanie kart
        # Karta 1 w lewo, Karta 2 w prawo
        
        # Ustawiamy pozycje recznie aby pominac animacje
        target_x1 = center_x - (w / 2) - offset
        self.card1.x = target_x1
        self.card1.y = draw_y
        self.card1.draw(surface, target_x1, draw_y, hidden=False, sc=scale)
        
        target_x2 = center_x - (w / 2) + offset
        self.card2.x = target_x2
        self.card2.y = draw_y
        self.card2.draw(surface, target_x2, draw_y, hidden=False, sc=scale)

#tym razem nowa klasa bo crash zbyt skomplikowany na animacje w Button2
class CrashIcon:
    def __init__(self):
        self.val = 1.00
        self.state = "IDLE"  # IDLE, RISING, CRASHED, WAIT_FOR_RESET
        self.crash_point = 2.00
        try:
            path = os.path.join("assets", "LuckiestGuy-Regular.ttf")
            self.font = pygame.font.Font(path, 160)
        except:
            self.font = pygame.font.SysFont("Arial", 160, bold=True)

    def draw(self, surface, center_x, center_y, offset, is_hovered):
        center_y -= 20
        # LOGIKA
        if is_hovered:
            if self.state == "IDLE" or self.state == "WAIT_FOR_RESET":
                # Reset i start
                self.state = "RISING"
                self.val = 1.00
                self.crash_point = random.uniform(1.2, 5.0) # Losowy punkt wybuchu
            
            elif self.state == "RISING":
                self.val += 0.04  # Prędkość wzrostu
                if self.val >= self.crash_point:
                    self.val = self.crash_point
                    self.state = "CRASHED"
        else:
            if self.state == "RISING":
                self.state = "CRASHED"
            
            elif self.state == "CRASHED":
                self.state = "WAIT_FOR_RESET"

        # RYSOWANIE
        if self.state == "CRASHED" or self.state == "WAIT_FOR_RESET":
            color = (230, 50, 50) # Czerwony
            shadow_color = (139, 0, 0)
        else:
            color = (50, 230, 50) # Zielony
            shadow_color = (0, 100, 0)
            
        text_str = f"{self.val:.2f}x"
        text_surf = self.font.render(text_str, True, color)
        text_surf_shadow = self.font.render(text_str, True, shadow_color)

        scale = (60 + (offset * 0.5)) / 150.0
        new_w = int(text_surf.get_width() * scale)
        new_h = int(text_surf.get_height() * scale)
        if new_w %2==1: new_w+=1
        if new_h %2==1: new_h+=1
        text_surf_shadow =pygame.transform.smoothscale(text_surf_shadow, (new_w, new_h))
        text_surf = pygame.transform.smoothscale(text_surf, (new_w, new_h))

        base_center = (center_x, center_y)
        depth_offset = 5 * scale
        shadow_center = (base_center[0] + depth_offset, base_center[1] + depth_offset)
        rect_shadow = text_surf_shadow.get_rect(center=shadow_center)
        surface.blit(text_surf_shadow, rect_shadow)

        
        rect_main = text_surf.get_rect(center=base_center)
        surface.blit(text_surf, rect_main)

class Slider:
    def __init__(self, x, y, width, initial_val):
        # Jeśli x == -1, suwak wyśrodkuje względem ekranu
        if x == -1:
            x = (WIDTH - width) // 2
        self.rect = pygame.Rect(x, y, width, 10)
        # Uchwyt centruje się na podstawie wartości początkowej
        self.handle_rect = pygame.Rect(x + (width * initial_val) - 10, y - 5, 20, 20)
        self.dragging = False
        self.value = initial_val

    def draw(self, surface):
        # Aktualizuj pozycję uchwytu na podstawie wartości
        self.handle_rect.centerx = self.rect.left + (self.rect.width * self.value)
        
        # Tło suwaka (szary pasek)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, border_radius=5)
        # Aktywny pasek (niebieski)
        active_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width * self.value, 10)
        pygame.draw.rect(surface, (52, 152, 219), active_rect, border_radius=5)
        # Uchwyt (kółko) - rysowanie na środku handle_rect
        pygame.draw.circle(surface, (255, 255, 255), self.handle_rect.center, 12)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Ograniczenie ruchu do szerokości paska
                self.handle_rect.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
                # Przeliczenie pozycji na wartość 0.0 - 1.0
                self.value = (self.handle_rect.centerx - self.rect.left) / self.rect.width
                return True
        return False