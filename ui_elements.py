import pygame
import os
from constants import WHITE, BLACK, GRAY, DARK_GRAY

class Button:
    def __init__(self, x, y, width, height, text):
        if x == -1:
            x = (800 - width) // 2
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.is_hovered = False

    def draw(self, surface, font, s_hover=None):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = DARK_GRAY
            if not self.is_hovered:
                if s_hover: s_hover.play()
                self.is_hovered = True
        else:
            current_color = self.color
            self.is_hovered = False
        pygame.draw.rect(surface, current_color, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event, s_click=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if s_click: s_click.play()
                return True
        return False

class Button2:
    def __init__(self, x, y, width, height, text, icon_renderer=None):
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy() 
        self.text = text
        self.icon_renderer = icon_renderer 
        self.anim_offset = 0 
        self.max_offset = 40 
        self.base_color = (52, 152, 219)
        self.hover_color = (41, 128, 185)
        self.text_color = (255, 255, 255)
        self.is_hovered = False 
        
    def draw(self, surface, font, s_hover=None):
        mouse_pos = pygame.mouse.get_pos()
        if self.original_rect.collidepoint(mouse_pos):
            current_color = self.hover_color
            self.rect = self.original_rect.inflate(20, 20)
            if self.anim_offset < self.max_offset: self.anim_offset += 2
            if not self.is_hovered:
                if s_hover: s_hover.play()
                self.is_hovered = True
        else:
            if self.anim_offset > 0: self.anim_offset -= 2
            current_color = self.base_color
            self.rect = self.original_rect.copy()
            self.is_hovered = False
        pygame.draw.rect(surface, current_color, self.rect, border_radius=15)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=15)
        if self.icon_renderer:
            self.icon_renderer.draw(surface, self.rect.centerx, self.rect.centery, self.anim_offset)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(midbottom=(self.rect.centerx, self.rect.bottom - 30))
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event, s_click=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if s_click: s_click.play()
                return True
        return False

class BlackjackIcon:
    def __init__(self, card_class):
        self.card1 = card_class("Spades", "Ace")
        self.card2 = card_class("Hearts", "Jack")
    def draw(self, surface, center_x, center_y, offset):
        scale = 0.65
        h, w = 150*scale, 100*scale
        draw_y = center_y - (h / 2) - 30
        self.card1.draw(surface, center_x - offset -30, draw_y, w, h)
        self.card2.draw(surface, center_x + offset -30, draw_y, w, h)