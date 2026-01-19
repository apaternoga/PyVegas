import pygame
from constants import WHITE, BLACK, GRAY, WIDTH, HEIGHT

def draw_menu(screen, bg_image, btns, font):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(WHITE)
    btns['start'].draw(screen, font)
    btns['exit'].draw(screen, font)
    btns['settings'].draw(screen, font)

def draw_settings(screen, bg_image, btns, font):
    if bg_image: 
        screen.blit(bg_image, (0, 0))
    else: 
        screen.fill(GRAY)
        
    # Tytuł sekcji
    title_surf = font.render("USTAWIENIA", True, WHITE)
    screen.blit(title_surf, title_surf.get_rect(center=(1280 // 2, 80)))
    
    # Rysujemy tylko istniejące przyciski
    btns['instr'].draw(screen, font)
    btns['lic'].draw(screen, font)
    btns['music_m'].draw(screen, font)
    btns['back'].draw(screen, font)

def draw_settings_music(screen, bg_image, btns, font, font_smaller, volume, vol_slider, is_muted):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(BLACK)
    
    # Tytuł na środku
    title = font.render("MUZYKA", True, WHITE)
    screen.blit(title, title.get_rect(center=(1280 // 2, 80)))
    
    # 1. Przygotowanie tekstu głośności
    vol_label = f"Głośność: {int(volume * 100)}%"
    vol_surf = font_smaller.render(vol_label, True, WHITE)
    
    # 2. Obliczamy całkowitą szerokość bloku [Tekst + Odstęp + Ikonka]
    # Szerokość ikonki to ok. 30px, odstęp 20px
    total_width = vol_surf.get_width() + 20 + 30
    start_x = (1280 - total_width) // 2
    
    # 3. Rysujemy tekst
    screen.blit(vol_surf, (start_x, 150))
    
    # 4. Rysujemy ikonkę obok tekstu
    draw_speaker_icon(screen, start_x + vol_surf.get_width() + 20, 150, is_muted)

    # Reszta elementów (suwak i przyciski)
    vol_slider.draw(screen)
    btns['t1'].draw(screen, font)
    btns['t2'].draw(screen, font)
    btns['stop'].draw(screen, font_smaller)
    btns['back'].draw(screen, font)
    
def draw_exit(screen, bg_image, btns, font, font_small):
    # Overlay przyciemniający
    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Białe okno komunikatu na środku
    rect_w, rect_h = 800, 300
    rect_x = (1280 - rect_w) // 2
    rect_y = (720 - rect_h) // 2
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_w, rect_h), border_radius=15)
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_w, rect_h), 3, border_radius=15)
    
    # Napis wyśrodkowany w oknie
    text = font_small.render("CZY NA PEWNO CHCESZ WYJŚĆ Z GRY?", True, BLACK)
    screen.blit(text, text.get_rect(center=(1280 // 2, rect_y + 80)))
    
    btns['yes'].draw(screen, font)
    btns['no'].draw(screen, font)
def draw_fullscreen(screen, btns, font_smaller, is_fullscreen):
    overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(180); overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, WHITE, (100, 200, 600, 200), border_radius=15)
    pygame.draw.rect(screen, BLACK, (100, 200, 600, 200), 3, border_radius=15)
    mode_text = "PEŁNY EKRAN" if not is_fullscreen else "TRYB OKNA"
    text = font_smaller.render(f"CZY CHCESZ PRZEŁĄCZYĆ NA {mode_text}?", True, BLACK)
    screen.blit(text, text.get_rect(center=(400, 250)))
    btns['yes'].draw(screen, font_smaller)
    btns['no'].draw(screen, font_smaller)

def draw_game_placeholder(screen, bg_image, btns, font):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill((20, 20, 20))
    
    # Tytuł sekcji gier na środku
    title = font.render("MINIGIERKI", True, WHITE)
    screen.blit(title, title.get_rect(center=(1280 // 2, 80)))
    
    btns['bj'].draw(screen, font)
    btns['g2'].draw(screen, font)
    btns['g3'].draw(screen, font)
    btns['back'].draw(screen, font)

def draw_speaker_icon(screen, x, y, muted):
    # Korpus głośnika (prostokąt)
    pygame.draw.rect(screen, WHITE, (x, y + 5, 10, 10))
    # Front głośnika (trapez/trójkąt)
    pygame.draw.polygon(screen, WHITE, [
        (x + 10, y + 5), (x + 25, y - 5), 
        (x + 25, y + 25), (x + 10, y + 15)
    ])
    
    if muted:
        # Czerwony X, gdy wyciszone
        pygame.draw.line(screen, (255, 50, 50), (x - 5, y - 5), (x + 30, y + 25), 4)
        pygame.draw.line(screen, (255, 50, 50), (x + 30, y - 5), (x - 5, y + 25), 4)
    else:
        # Fale dźwiękowe, gdy gra (łuki)
        pygame.draw.arc(screen, WHITE, (x + 15, y - 5, 20, 30), -1.5, 1.5, 3)
        pygame.draw.arc(screen, WHITE, (x + 22, y - 10, 25, 40), -1.5, 1.5, 2)