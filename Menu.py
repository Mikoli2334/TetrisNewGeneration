import sys

import pygame


class Menu:
    def __init__(self,screen,on_start,on_scores,on_quit):
        self.screen = screen
        self.on_start = on_start
        self.on_scores = on_scores
        self.on_quit = on_quit
        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.start = pygame.Rect((300,300,200,50))
        self.highscores = pygame.Rect((300,370,200,50))
        self.quit=pygame.Rect((300,440,200,50))
        self.menu_items=["START","HIGHSCORES","QUIT"]
        self.selected_index=0

    def draw(self):
        self.screen.fill((0, 0, 0))
        tetris_text = self.font.render("TETRIS", True, (0, 100, 200))
        self.screen.blit(tetris_text, (300, 200))

        buttons = [self.start, self.highscores, self.quit]
        labels = ["START", "HIGHSCORES", "QUIT"]

        for i, rect in enumerate(buttons):
            color = (255, 255, 0) if i == self.selected_index else (50, 50, 50)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (200, 200, 220), rect, 2)
            text = self.font.render(labels[i], True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            buttons = [self.start, self.highscores, self.quit]
            self.selected_index = -1
            for i, rect in enumerate(buttons):
                if rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            buttons = [self.start, self.highscores, self.quit]
            for i, rect in enumerate(buttons):
                if rect.collidepoint(event.pos):
                    self.activate_selected(i)
                    break

    def activate_selected(self, index):
        if index == 0:
            self.on_start()
        elif index == 1:
            self.on_scores()
        elif index == 2:
            self.on_quit()


