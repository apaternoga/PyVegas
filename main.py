import pygame
import sys
import os
import ctypes  # Potrzebne do naprawy ikonki na pasku zadań

#importy z innych plikow
from core.settings import *
from core.sound_manager import SoundManager
from Menu import Menu
from games.blackjack import BlackjackGame, Card, Button, Deck, Hand
from games.crash import CrashGame
from ui_elements import Manager
from intro import IntroSequence
from core.wallet import Wallet

def main():
    # --- NAPRAWA IKONKI NA PASKU ZADAŃ (WINDOWS) ---
    # Ta sekcja informuje Windows, że to jest oddzielna aplikacja, a nie skrypt Pythona.
    # Dzięki temu ikonka na pasku zadań nie będzie domyślnym logo Pythona.
    try:
        myappid = 'mycompany.pyvegas.casino.1.0' # Dowolny unikalny ciąg znaków
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass 

    #inicjalizacja modulow pygame
    pygame.init()

    #inicjalizacja miksera dzwiekow
    pygame.mixer.init()
    sm = SoundManager()
    sm.load_common_sounds()
    sm.load_blackjack_sounds()
    sm.load_crash_sounds()
    Manager.sm = sm

    #tworzenie 'screen', czyli glownego okna gry
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    # --- TYTUŁ I IKONKA ---
    pygame.display.set_caption("PyVegas")
    
    icon_path = os.path.join("assets", "pyvegas.png")
    if os.path.exists(icon_path):
        icon = pygame.image.load(icon_path)
    
        pygame.display.set_icon(icon)
    
    #odpowiada za FPS
    clock=pygame.time.Clock()

    #tu jest intro
    intro = IntroSequence(screen, sm)
    intro.run()

    menu = Menu(screen, sm, wallet=Wallet(STARTING_MONEY))
    game = None
    
    app_state ="MENU"

    running = True

    #GLOWNA PETLA
    while running:
        
        if app_state == "MENU":
            action = menu.update() 
            menu.draw()

            if action == "EXIT_APP":
                running = False
            elif action == "BLACKJACK":
                game = BlackjackGame(screen, sm, wallet=menu.wallet)
                game_curr = 'BLACKJACK' 
                app_state = "GAME"
            elif action == "CRASH":
                game = CrashGame(screen, sm, wallet=menu.wallet)
                game_curr = 'CRASH' 
                app_state = "GAME"

        elif app_state == "GAME":
            if game:
                game.update()
                menu.wallet.save()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    
                    # Obsługa ESC - sprawdzamy czy gra pozwala na wyjście
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if hasattr(game, 'can_exit') and game.can_exit():
                            app_state = "MENU"
                            if game_curr == 'CRASH': sm.play_music()
                            game = None
                    
                    if game: game.handle_input(event)

                # Sprawdzanie czy gra sama poprosiła o wyjście
                if game and game.exit_requested:
                    app_state = "MENU"
                    if game_curr == "CRASH": sm.play_music()
                    game = None
                
                if game: game.draw()

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()