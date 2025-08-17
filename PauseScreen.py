import pygame

class PauseScreen:
    def __init__(self, screen, on_resume, on_back_to_menu, on_click_sound=None, theme=None, fonts=None):
        self.screen = screen
        self.on_resume = on_resume
        self.on_back_to_menu = on_back_to_menu
        self.on_click_sound = on_click_sound
        self.theme = theme or {}
        f = fonts or {}
        self.title_font = f.get("h1") or pygame.font.SysFont("Comic Sans", 60, bold=True)
        self.btn_font   = f.get("text") or pygame.font.SysFont("Comic Sans", 30)

        w, h = self.screen.get_size()
        self.resume_rect = pygame.Rect(0, 0, 320, 70)
        self.back_rect   = pygame.Rect(0, 0, 320, 70)
        self.resume_rect.center = (w // 2, h // 2 - 50)
        self.back_rect.center   = (w // 2, h // 2 + 50)

        self._hover_resume = False
        self._hover_back   = False

    def draw(self):
        t = self.theme
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # полупрозрачное затемнение
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("PAUSED", True, t["accent"])
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 140)))

        bg = t["button_hover"] if self._hover_resume else t["button_idle"]
        pygame.draw.rect(self.screen, bg, self.resume_rect, border_radius=10)
        pygame.draw.rect(self.screen, t["button_border"], self.resume_rect, 2, border_radius=10)
        label = self.btn_font.render("RESUME", True, t["text"])
        self.screen.blit(label, label.get_rect(center=self.resume_rect.center))

        bg = t["button_hover"] if self._hover_back else t["button_idle"]
        pygame.draw.rect(self.screen, bg, self.back_rect, border_radius=10)
        pygame.draw.rect(self.screen, t["button_border"], self.back_rect, 2, border_radius=10)
        label = self.btn_font.render("BACK TO MENU", True, t["text"])
        self.screen.blit(label, label.get_rect(center=self.back_rect.center))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit(); raise SystemExit
        elif event.type == pygame.MOUSEMOTION:
            self._hover_resume = self.resume_rect.collidepoint(event.pos)
            self._hover_back   = self.back_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.resume_rect.collidepoint(event.pos):
                if self.on_click_sound: self.on_click_sound()
                self.on_resume()
            elif self.back_rect.collidepoint(event.pos):
                if self.on_click_sound: self.on_click_sound()
                self.on_back_to_menu()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if self.on_click_sound: self.on_click_sound()
            self.on_resume()
