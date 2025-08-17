import pygame

class Menu:
    def __init__(self, screen, on_start, on_scores, on_quit, on_settings, on_click_sound=None,theme=None,fonts=None):
        self.screen = screen
        self.on_start = on_start
        self.on_scores = on_scores
        self.on_quit = on_quit
        self.on_settings = on_settings
        self.on_click_sound = on_click_sound
        self.theme = theme
        f = fonts or {}

        self.title_font = f.get("title") or pygame.font.SysFont("Comic Sans", 72, bold=True)
        self.font =f.get("menu") or pygame.font.SysFont("Comic Sans", 48)

        self.options = ["Start Game", "High Scores", "Settings", "Quit"]
        self.actions = [self.on_start, self.on_scores, self.on_settings, self.on_quit]

        self.selected_index = -1

    def draw(self):
        t=self.theme
        self.screen.fill(t["bg"])

        title = self.title_font.render("TETRIS", True, t["accent"])
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title, title_rect)



        for i, option in enumerate(self.options):
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = (self.screen.get_width() // 2, 280 + i * 90)
            bg_color = t["button_hover"] if i == self.selected_index else t["button_idle"]
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=12)
            pygame.draw.rect(self.screen, t["button_border"], rect, 2, border_radius=12)
            text = self.font.render(option, True, t["text"])
            self.screen.blit(text, text.get_rect(center=rect.center))
        pygame.display.flip()



    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.MOUSEMOTION:
            self.selected_index = -1
            for i, option in enumerate(self.options):
                rect = pygame.Rect(0, 0, 300, 60)
                rect.center = (self.screen.get_width() // 2, 280 + i * 90)
                if rect.collidepoint(event.pos):
                    self.selected_index = i

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.selected_index >= 0:
                if self.on_click_sound:
                    self.on_click_sound()
                self.actions[self.selected_index]()
