import os
import json
import pygame
from constants import BLACK, GRID_SIZE, WHITE

class UI:
    def __init__(self, x, y, scores_file="scores.json",font=None):
        self.x = x
        self.y = y
        self.score = 0
        self.level = 1
        self.highscores = {}   # имя → очки
        self.scores_file = scores_file
        self.font = font or pygame.font.SysFont("Comic Sans", 28)
        self.load_scores()

    def reset_score(self):
        self.score = 0
        self.level = 1

    def add_score(self, lines_cleared: int):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared >= 4:
            self.score += 800
        self.level = 1 + self.score // 1000


    def load_scores(self):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.highscores = {f"Player{i+1}": s for i, s in enumerate(data)}
                    elif isinstance(data, dict):
                        self.highscores = data
                    else:
                        self.highscores = {}
                except json.JSONDecodeError:
                    self.highscores = {}
        else:
            self.highscores = {}

    def save_scores(self, player_name):
        if not player_name:
            player_name = "Unknown"

        if not isinstance(self.highscores, dict):
            self.highscores = {}

        best = self.highscores.get(player_name, 0)
        if self.score > best:
            self.highscores[player_name] = self.score

        with open(self.scores_file, "w") as f:
            json.dump(self.highscores, f, indent=4)


    def draw(self, screen, next_piece,theme):
        color=theme["panel_text"]
        score_text = self.font.render(f"Score: {self.score}", True, color)
        screen.blit(score_text, (self.x, self.y))


        level_text = self.font.render(f"Level: {self.level}", True, color)
        screen.blit(level_text, (self.x, self.y + 40))


        next_text = self.font.render("Next:", True, color)
        screen.blit(next_text, (self.x, self.y + 100))


        if next_piece:

            blocks = next_piece.get_blocks()
            min_x = min(x for x, _ in blocks)
            max_x = max(x for x, _ in blocks)
            min_y = min(y for _, y in blocks)
            max_y = max(y for _, y in blocks)

            piece_width = (max_x - min_x + 1) * GRID_SIZE
            piece_height = (max_y - min_y + 1) * GRID_SIZE

            panel_center_x = self.x + 100
            panel_top_y = self.y + 150

            offset_x = panel_center_x - piece_width // 2
            offset_y = panel_top_y

            for x, y in blocks:
                rect_x = offset_x + (x - min_x) * GRID_SIZE
                rect_y = offset_y + (y - min_y) * GRID_SIZE
                pygame.draw.rect(screen, next_piece.color,
                                 (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, color,
                                 (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)
