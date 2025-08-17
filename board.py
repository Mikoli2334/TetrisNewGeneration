import pygame

from constants import *

#This class describe game panel and its behaviour
class Board:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.grid=[[None for _ in range(cols)] for _ in range(rows)]

    # Draws every cell of the board (filled or empty) and the outer border onto the given surface.
    def is_valid_position(self,piece):
        for x ,y in piece.get_blocks():
            if x<0 or x>=self.cols:
                return False
            if y<0 or y>=self.rows:
                return False
            if self.grid[y][x] is not None:
                return False
        return True

    # Places the piece on the grid by coloring every block it occupies.
    def place_piece(self,piece):
        for x,y in piece.get_blocks():
            if 0<=x<self.cols and 0<=y<self.rows:
             self.grid[y][x]=piece.color

    # Deletes every full row, shifts the grid down, adds empty rows on top, and returns the number of cleared rows.
    def clear_rows(self):
        new_grid=[]
        for row in self.grid:
            if any(cell is None for cell in row):
                new_grid.append(row)
        deleted_rows=self.rows-len(new_grid)
        for _ in range(deleted_rows):
            new_grid.insert(0,[None for _ in range(self.cols)])
        self.grid=new_grid
        return deleted_rows

    # Draws every cell of the board (filled or empty) and the outer border onto the given surface.
    def draw(self,surface,theme):
        pygame.draw.rect(surface,theme["play_bg"],(PLAY_AREA_X,PLAY_AREA_Y,PLAY_AREA_WIDTH,PlAY_AREA_HEIGHT))
        for y in range(self.rows):
            for x in range(self.cols):
                rect_x=PLAY_AREA_X+x*GRID_SIZE
                rect_y=PLAY_AREA_Y+y*GRID_SIZE
                if self.grid[y][x] is not None:
                   pygame.draw.rect(surface, self.grid[y][x], (rect_x,rect_y,GRID_SIZE,GRID_SIZE))
                pygame.draw.rect(surface, theme["grid"], (rect_x, rect_y, GRID_SIZE, GRID_SIZE),1)

        pygame.draw.rect(surface,theme["border"], (PLAY_AREA_X,PLAY_AREA_Y,PLAY_AREA_WIDTH,PlAY_AREA_HEIGHT),2)