import pygame


class HighScoreScreen:
    def __init__(self, screen, on_back):
        self.screen = screen
        self.on_back = on_back
        self.title_font = pygame.font.SysFont("Comic Sans", 48)
        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.back = pygame.Rect((50, 650, 200, 50))

    def draw(self, scores):
        self.screen.fill((0, 0, 0))
        tetris_text = self.title_font.render("HIGH SCORES", True, (0, 100, 200))
        self.screen.blit(tetris_text, (100, 100))

        if not scores:
            no_text = self.title_font.render("No scores", True, (0, 100, 200))
            self.screen.blit(no_text, (100, 200))
        else:
            for i, score in enumerate(sorted(scores, reverse=True)[:10]):
                color = (255, 255, 255)
                text = self.font.render(f"{i + 1}.  {score}", True, color)
                text_rect = text.get_rect(center=(self.screen.get_width() / 2, 200 + i * 40))
                self.screen.blit(text, text_rect)


        pygame.draw.rect(self.screen, (50, 50, 50), self.back)
        pygame.draw.rect(self.screen, (200, 200, 220), self.back, 2)
        back_text = self.font.render("BACK", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back.center)
        self.screen.blit(back_text, back_rect)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back.collidepoint(event.pos):
                self.on_back()
