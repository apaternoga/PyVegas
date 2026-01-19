import pygame
import sys

#importy z innych plikow
from core.settings import *
from core.sound_manager import SoundManager
from Menu import Menu
from games.blackjack import BlackjackGame, Card, Button, Deck, Hand
from ui_elements import Manager

def main():
    #inicjalizacja modulow pygame
    pygame.init()

    #inicjalizacja miksera dzwiekow
    pygame.mixer.init()
    sm = SoundManager()
    sm.load_common_sounds()
    sm.load_blackjack_sounds() #przeniesc potem

    Manager.sm = sm

    #tworzenie 'screen', czyli glownego okna gry o rozmiarach podanych w settings.py
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    #ta linijka odpowiada za tytul u gory
    pygame.display.set_caption(CAPTION)
    
    #odpowiada za FPS
    clock=pygame.time.Clock()

    #tu bedzie intro
    menu = Menu(screen, sm)
    game= None

    app_state ="MENU"

    running =True

    #GLOWNA PETLA
    #wykonuje sie ona kilkadziesiat razy na sekunde
    while running:
        
        if app_state == "MENU":
            action = menu.update() 
            menu.draw()

            if action == "EXIT_APP":
                running = False
            elif action == "BLACKJACK":
                game = BlackjackGame(screen, sm)
                app_state = "GAME"

        elif app_state == "GAME":
            if game:
                game.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        app_state = "MENU"
                        game = None # Usuwamy grę z pamięci
                    
                    if game: game.handle_input(event)
                
                if game: game.draw()

        #rysujemy cala gre na ekranie
        #dzieki temu uzytkownik widzi plynna animacje, w pelni narysowane obrazy, a nie proces ich powstawania
        pygame.display.flip()
        
        clock.tick(FPS)
    
    #sprzatanie po zamknieciu petli
    pygame.quit()
    sys.exit()

#uruchom gre wtedy i tylko wtedy jesli ten plik zostal uruchomiony bezposrednio przez czlowieka
if __name__=="__main__":
    main()