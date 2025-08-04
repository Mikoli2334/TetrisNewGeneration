import pygame
import sys
import random
from board import Board
from piece import Piece
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Play Game')
board=Board(BOARD_HEIGHT_BLOCKS,BOARD_WIDTH_BLOCKS)
piece=Piece(random.randint(0,len(SHAPES)-1),BOARD_WIDTH_BLOCKS,BOARD_HEIGHT_BLOCKS)

clock=pygame.time.Clock()
running=True
fall_interval=500
last_fall_time=pygame.time.get_ticks()
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False


    currentTime=pygame.time.get_ticks()
    if currentTime-last_fall_time>fall_interval:
        piece.y+=1
        if not board.is_valid_position(piece):
            piece.y-=1
            board.place_piece(piece)
            piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)
        last_fall_time=currentTime

    for x,y in piece.get_blocks():
        if y>=0:
            rect_x=PLAY_AREA_X+x*GRID_SIZE
            rect_y=PLAY_AREA_Y+y*GRID_SIZE
            pygame.draw.rect(screen,piece.color,(rect_x,rect_y,GRID_SIZE,GRID_SIZE))
            pygame.draw.rect(screen,LIGHT_GRAY,(rect_x,rect_y,GRID_SIZE,GRID_SIZE),1)

    board.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()