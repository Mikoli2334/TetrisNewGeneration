import pygame

from constants import BLACK


class UI:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.score=0
        self.font = pygame.font.SysFont("Comic Sans", 24)

    def draw(self,surface):
        score_text=self.font.render(f"Points:{self.score}",True,(0,100,200))
        surface.blit(score_text,(self.x,self.y))

    def add_score(self,line):
        self.score+=line*100