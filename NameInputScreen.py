import pygame

class NameInputScreen:
    def __init__(self, screen, on_done, theme=None, fonts=None):
        self.screen = screen
        self.on_done = on_done
        self.theme = theme or {}
        f = fonts or {}
        self.title_font = f.get("h1") or pygame.font.SysFont("Comic Sans", 48, bold=True)
        self.font = f.get("text") or pygame.font.SysFont("Comic Sans", 32)
        self.name = ""
        self.max_len = 12
        self.prompt = "Enter your name:"
        self.tip = "Press Enter to continue"

        w, h = self.screen.get_size()
        self.input_rect = pygame.Rect(0, 0, 420, 56)
        self.input_rect.center = (w // 2, h // 2 + 20)

    def draw(self):
        t = self.theme
        self.screen.fill(t["bg"])

        title = self.title_font.render(self.prompt, True, t["accent"])
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 40)))

        pygame.draw.rect(self.screen, t["button_idle"], self.input_rect, border_radius=8)
        pygame.draw.rect(self.screen, t["button_border"], self.input_rect, 2, border_radius=8)

        text_surface = self.font.render(self.name or "_", True, t["text"])
        self.screen.blit(text_surface, text_surface.get_rect(center=self.input_rect.center))

        tip = self.font.render(self.tip, True, t["text"])
        self.screen.blit(tip, tip.get_rect(center=(self.screen.get_width()//2, self.input_rect.bottom + 40)))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit(); raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.name.strip():
                    self.on_done(self.name.strip())
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                ch = event.unicode
                if ch and ch.isprintable() and len(self.name) < self.max_len:
                    self.name += ch
