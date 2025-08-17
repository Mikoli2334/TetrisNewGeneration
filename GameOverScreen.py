import pygame

class GameOverScreen:
    def __init__(self, screen, on_back_to_menu, on_click_sound=None, theme=None, fonts=None):
        self.screen = screen
        self.on_back_to_menu = on_back_to_menu
        self.on_click_sound = on_click_sound
        self.theme = theme or {}
        f = fonts or {}
        self.title_font = f.get("title") or pygame.font.SysFont("Comic Sans", 72)
        self.font = f.get("menu") or pygame.font.SysFont("Comic Sans", 40)
        self.back_btn = pygame.Rect(200, 400, 400, 60)
        self._hover_back = False

    def draw(self, score: int):
        t = self.theme
        self.screen.fill(t["bg"])

        title = self.title_font.render("GAME OVER", True, t["accent"])
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() / 2, 200)))

        score_text = self.font.render(f"Your score: {score}", True, t["text"])
        self.screen.blit(score_text, score_text.get_rect(center=(self.screen.get_width() / 2, 300)))

        bg = t["button_hover"] if self._hover_back else t["button_idle"]
        pygame.draw.rect(self.screen, bg, self.back_btn, border_radius=12)
        pygame.draw.rect(self.screen, t["button_border"], self.back_btn, 3, border_radius=12)

        back_text = self.font.render("BACK TO MENU", True, t["text"])
        self.screen.blit(back_text, back_text.get_rect(center=self.back_btn.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit(); raise SystemExit
        elif event.type == pygame.MOUSEMOTION:
            self._hover_back = self.back_btn.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_btn.collidepoint(event.pos):
                if self.on_click_sound: self.on_click_sound()
                self.on_back_to_menu()
