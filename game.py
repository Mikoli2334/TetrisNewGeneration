import pygame
import sys
import random
from UI import UI
from board import Board
from piece import Piece
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Play Game')

        self.board = Board(BOARD_HEIGHT_BLOCKS, BOARD_WIDTH_BLOCKS)
        self.piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)
        self.next_piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)

        self.panel = UI(x=450, y=100)
        self.panel.reset_score()

        self.running = True
        self.fall_interval = 500
        self.last_fall_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.piece.x += 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.x -= 1

                elif event.key == pygame.K_LEFT:
                    self.piece.x -= 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.x += 1

                elif event.key == pygame.K_DOWN:
                    self.piece.y += 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.y -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                old_rotation = self.piece.rotation
                self.piece.rotate()
                if not self.board.is_valid_position(self.piece):
                    self.piece.rotation = old_rotation

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > self.fall_interval:
            self.piece.y += 1
            if not self.board.is_valid_position(self.piece):
                self.piece.y -= 1
                self.board.place_piece(self.piece)


                lines = self.board.clear_rows()
                self.panel.add_score(lines)


                self.piece = self.next_piece
                self.next_piece = Piece(random.randint(0, len(SHAPES) - 1),
                                        BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)


                if not self.board.is_valid_position(self.piece):
                    self.running = False

            self.last_fall_time = current_time

    def draw(self):
        self.screen.fill(WHITE)
        for x, y in self.piece.get_blocks():
            if y >= 0:
                rect_x = PLAY_AREA_X + x * GRID_SIZE
                rect_y = PLAY_AREA_Y + y * GRID_SIZE
                pygame.draw.rect(self.screen, self.piece.color, (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, LIGHT_GRAY, (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)

        self.board.draw(self.screen)
        self.panel.draw(self.screen, self.next_piece)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        self.panel.save_scores()
        pygame.quit()
        sys.exit()
import pygame
import sys
import random
from UI import UI
from board import Board
from piece import Piece
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Play Game')

        self.board = Board(BOARD_HEIGHT_BLOCKS, BOARD_WIDTH_BLOCKS)
        self.piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)
        self.next_piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)

        self.panel = UI(x=450, y=100)
        self.panel.reset_score()

        self.running = True
        self.fall_interval = 500
        self.last_fall_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.piece.x += 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.x -= 1

                elif event.key == pygame.K_LEFT:
                    self.piece.x -= 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.x += 1

                elif event.key == pygame.K_DOWN:
                    self.piece.y += 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.y -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                old_rotation = self.piece.rotation
                self.piece.rotate()
                if not self.board.is_valid_position(self.piece):
                    self.piece.rotation = old_rotation

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > self.fall_interval:
            self.piece.y += 1
            if not self.board.is_valid_position(self.piece):
                self.piece.y -= 1
                self.board.place_piece(self.piece)

                # Clear rows first
                lines = self.board.clear_rows()
                self.panel.add_score(lines)

                # Spawn next piece
                self.piece = self.next_piece
                self.next_piece = Piece(random.randint(0, len(SHAPES) - 1),
                                        BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS)

                # Game over check
                if not self.board.is_valid_position(self.piece):
                    self.running = False

            self.last_fall_time = current_time

    def draw(self):
        self.screen.fill(WHITE)
        for x, y in self.piece.get_blocks():
            if y >= 0:
                rect_x = PLAY_AREA_X + x * GRID_SIZE
                rect_y = PLAY_AREA_Y + y * GRID_SIZE
                pygame.draw.rect(self.screen, self.piece.color, (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, LIGHT_GRAY, (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)

        self.board.draw(self.screen)
        self.panel.draw(self.screen, self.next_piece)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        self.panel.save_scores()
        pygame.quit()
        sys.exit()
