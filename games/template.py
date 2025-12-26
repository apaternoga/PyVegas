import pygame
from core.settings import *

class GameTemplate:
    def __init__(self,screen):
        self.screen=screen
        # inicjowanie zmiennych dla nowej gry

    def handle_input(self,event):
        pass
        # obsluga klawiszy specficznych dla tej gry
    
    def draw(self):
        self.screen.fill(BLACK) #przykladowe czyszczenie ekranu
        #rysowanie elementow gry
