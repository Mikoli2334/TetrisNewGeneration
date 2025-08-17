import pygame

class HighScoreScreen:
    def __init__(self, screen, on_back, on_click_sound=None, theme=None, fonts=None):
        self.screen = screen
        self.on_back = on_back
        self.on_click_sound = on_click_sound
        self.theme = theme or {}
        f = fonts or {}
        self.title_font = f.get("h1") or pygame.font.SysFont("Comic Sans", 48)
        self.font = f.get("text") or pygame.font.SysFont("Comic Sans", 30)
        self.back = pygame.Rect(50, 650, 200, 50)
        self._hover_back = False

    def draw(self, scores: dict):
        t = self.theme
        self.screen.fill(t["bg"])

        tetris_text = self.title_font.render("HIGH SCORES", True, t["accent"])
        self.screen.blit(tetris_text, (100, 100))

        if not scores:
            no_text = self.title_font.render("No scores", True, t["text"])
            self.screen.blit(no_text, (100, 200))
        else:
            for i, (name, score) in enumerate(sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:10]):
                text = self.font.render(f"{i + 1}. {name} — {score}", True, t["text"])
                self.screen.blit(text, text.get_rect(center=(self.screen.get_width() / 2, 200 + i * 40)))

        bg = t["button_hover"] if self._hover_back else t["button_idle"]
        pygame.draw.rect(self.screen, bg, self.back, border_radius=10)
        pygame.draw.rect(self.screen, t["button_border"], self.back, 2, border_radius=10)
        back_text = self.font.render("BACK", True, t["text"])
        self.screen.blit(back_text, back_text.get_rect(center=self.back.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit(); raise SystemExit
        elif event.type == pygame.MOUSEMOTION:
            self._hover_back = self.back.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back.collidepoint(event.pos):
                if self.on_click_sound: self.on_click_sound()
                self.on_back()
