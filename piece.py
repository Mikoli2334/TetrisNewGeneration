import pygame
import random

from constants import *
'''This class represents a single tetromino piece, including its shape, color, position, and rotation.'''
class Piece:
    def __init__(self,shape_index,board_width_block,board_height_block):
        self.shape_index=shape_index
        self.shape_data=SHAPES[shape_index]
        self.color=COLORS[shape_index]
        self.rotation=0
        current_shape=self.shape_data[self.rotation]
        max_col_offset=max(block[0] for block in current_shape) if current_shape else 0
        self.x=(board_width_block//2)-(max_col_offset//2)
        self.y=0

    # Returns a list of absolute block positions (x, y) based on the current rotation and position.
    def get_blocks(self):
        blocks=[]
        for r_offset,c_offset in self.shape_data[self.rotation]:
            blocks.append((self.x+c_offset,self.y+r_offset))
        return blocks

    # Rotates the piece to the next available shape variation.
    def rotate(self):
        self.rotation+=1
        self.rotation%=len(self.shape_data)
