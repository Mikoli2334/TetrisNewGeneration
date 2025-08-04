import os

import pygame
import json
from constants import BLACK, GRID_SIZE, LIGHT_GRAY


class UI:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.score=0
        self.font = pygame.font.SysFont("Comic Sans", 24)
        self.scores="scores.json"
        self.highscores=[]

        if os.path.exists(self.scores):
            with open(self.scores,"r") as f:
                try:
                    self.highscores=json.load(f)
                except json.decoder.JSONDecodeError:
                    self.highscores=[]

    def draw(self,surface,next_piece):
        score_text=self.font.render(f"Points:{self.score}",True,(0,100,200))
        surface.blit(score_text,(self.x,self.y))

        text_shape=self.font.render(f"The next",True,(255,255,255))
        surface.blit(text_shape,(self.x,self.y+60))

        for r,c in next_piece.shape_data[next_piece.rotation]:
            blockX=self.x+c*(GRID_SIZE)
            blockY=self.y+100+r*(GRID_SIZE)
            pygame.draw.rect(surface,next_piece.color,(blockX,blockY,GRID_SIZE,GRID_SIZE))
            pygame.draw.rect(surface,LIGHT_GRAY,(blockX,blockY,GRID_SIZE,GRID_SIZE),1)

        text_scores=self.font.render(f"Records:",True,BLACK)
        surface.blit(text_scores,(self.x,self.y+220))

        for i ,score in enumerate(self.highscores):
            text=self.font.render(f"{i+1}.  {score}",True,BLACK)
            surface.blit(text,(self.x,self.y+240+i*30))



    def add_score(self,line):
        self.score+=line*100

    def save_scores(self):
        self.highscores.append(self.score)
        self.highscores=sorted(self.highscores,reverse=True)[:5]
        with open(self.scores, 'w') as f:
            json.dump(self.highscores, f)

    def reset_score(self):
        self.score=0