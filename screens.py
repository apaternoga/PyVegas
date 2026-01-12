import pygame
from constants import WHITE, BLACK, GRAY

def draw_menu(screen, bg_image, btns, font):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(WHITE)
    btns['start'].draw(screen, font)
    btns['exit'].draw(screen, font)
    btns['settings'].draw(screen, font)

def draw_settings(screen, bg_image, btns, font):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(GRAY)
    title_surf = font.render("USTAWIENIA", True, WHITE)
    screen.blit(title_surf, title_surf.get_rect(center=(400, 70)))
    btns['instr'].draw(screen, font)
    btns['full'].draw(screen, font)
    btns['lic'].draw(screen, font)
    btns['music_m'].draw(screen, font)
    btns['back'].draw(screen, font)

def draw_settings_music(screen, bg_image, btns, font, volume, current_track):
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(GRAY)
    title_surf = font.render("MUZYKA", True, WHITE)
    screen.blit(title_surf, title_surf.get_rect(center=(400, 70)))
    vol_text = font.render(f"Głośność: {int(volume * 100)}%", True, WHITE)
    screen.blit(vol_text, vol_text.get_rect(center=(400, 140)))
    pygame.draw.rect(screen, BLACK, (200, 170, 400, 20))
    pygame.draw.rect(screen, (52, 152, 219), (200, 170, 400 * volume, 20))
    info_text = font.render(f"Aktualnie gra: {current_track}", True, WHITE)
    screen.blit(info_text, info_text.get_rect(center=(400, 270)))
    btns['t1'].draw(screen, font)
    btns['t2'].draw(screen, font)
    btns['stop'].draw(screen, font)
    btns['back'].draw(screen, font)

def draw_exit(screen, bg_image, btns, font, font_small):
    draw_menu(screen, bg_image, btns, font)
    overlay = pygame.Surface((800, 600)); overlay.set_alpha(180); overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, WHITE, (100, 200, 600, 200), border_radius=15)
    pygame.draw.rect(screen, BLACK, (100, 200, 600, 200), 3, border_radius=15)
    text = font_small.render("CZY NA PEWNO CHCESZ WYJŚĆ Z GRY?", True, BLACK)
    screen.blit(text, text.get_rect(center=(400, 250)))
    btns['yes'].draw(screen, font)
    btns['no'].draw(screen, font)

def draw_fullscreen(screen, btns, font_smaller, is_fullscreen):
    overlay = pygame.Surface((800, 600)); overlay.set_alpha(180); overlay.fill(BLACK)
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
    else: screen.fill((0, 255, 0))
    text = font.render("MINIGIERKI", True, (255, 255, 255))
    screen.blit(text, (300, 75))
    btns['bj'].draw(screen, font)
    btns['g2'].draw(screen, font)
    btns['g3'].draw(screen, font)
    btns['back'].draw(screen, font)