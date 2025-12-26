import pygame
import sys

from core.settings import *
#importuje wszystkie wartosci z settings.py
from games.blackjack import BlackjackGame
#importuje Blajacka
def main():
    #inicjalizacja modulow pygame
    pygame.init()

    #tworzenie 'screen', czyli glownego okna gry o rozmiarach podanych w settings.py
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    #ta linijka odpowiada za tytul u gory
    pygame.display.set_caption(CAPTION)
    
    #odpowiada za FPS
    clock=pygame.time.Clock()

    game= BlackjackGame(screen)

    running =True

    #GLOWNA PETLA GRY
    #wykonuje sie ona kilkadziesiat razy na sekunde
    while running:
        
        #pygame.event.get() pobiera liste wszystkiego co gracz zrobil
        for event in pygame.event.get():
            
            #sprawdzenie czy gracz kliknal X w oknie aplikacji
            if event.type == pygame.QUIT:
                running= False

            #przekazujemy kazde zdarzenie (wcisniecie klawisza) do logiki naszej gry
            game.handle_input(event)

        #rysujemy cala gre na ekranie
        game.draw()

        #dzieki temu uzytkownik widzi plynna animacje, w pelni narysowane obrazy, a nie proces ich powstawania
        pygame.display.flip()
        
        clock.tick(FPS)
    
    #sprzatanie po zamknieciu petli
    pygame.quit()
    sys.exit()

#uruchom gre wtedy i tylko wtedy jesli ten plik zostal uruchomiony bezposrednio przez czlowieka
if __name__=="__main__":
    main()