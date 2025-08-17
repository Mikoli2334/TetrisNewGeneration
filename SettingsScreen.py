# SettingsScreen.py
import pygame
from themes import ORDERED_THEME_KEYS

class SettingsScreen:
    def __init__(self, screen, settings, on_change, on_back, on_click_sound=None, theme=None, fonts=None):
        self.screen = screen
        self.settings = settings
        self.on_change = on_change
        self.on_back = on_back
        self.on_click_sound = on_click_sound
        self.theme = theme
        f = fonts or {}
        self.title_font = f.get("h1") or pygame.font.SysFont("Comic Sans", 48, bold=True)
        self.font = f.get("text") or pygame.font.SysFont("Comic Sans", 28)

        w, h = self.screen.get_size()
        self.music_slider = pygame.Rect(w//2 - 150, 220, 300, 6)
        self.sfx_slider   = pygame.Rect(w//2 - 150, 300, 300, 6)
        self.knob_radius = 10
        self.dragging = None
        self.music_toggle_rect = pygame.Rect(w//2 + 180, 200, 60, 32)

        self.diff_options = [("easy", "Easy"), ("normal", "Normal"), ("hard", "Hard")]
        self.diff_rects = []
        base_y = 380
        for i, (key, label) in enumerate(self.diff_options):
            r = pygame.Rect(w//2 - 150 + i*140, base_y, 120, 40)
            self.diff_rects.append((key, label, r))

        # === THEME (новый блок) ===
        self.theme_keys = ORDERED_THEME_KEYS  # ["Classic","Neon","Pastel","Dark"]
        self.theme_rects = []
        base_y2 = 460
        for i, key in enumerate(self.theme_keys):
            r = pygame.Rect(w//2 - 300 + i*150, base_y2, 130, 40)
            self.theme_rects.append((key, r))

        self.back_btn = pygame.Rect(0, 0, 240, 56)
        self.back_btn.center = (w//2, h - 100)
        self._hover_back = False

    def _value_to_x(self, rect, val): return rect.x + int(val * rect.w)
    def _x_to_value(self, rect, x):
        rel = (x - rect.x) / rect.w
        return max(0.0, min(1.0, rel))

    def draw(self):
        t = self.theme
        self.screen.fill(t["bg"])
        title = self.title_font.render("SETTINGS", True, t["accent"])
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width()//2, 120)))

        # Music label + toggle
        label = self.font.render("Music:", True, t["text"])
        self.screen.blit(label, (self.music_slider.x - 120, self.music_slider.y - 20))
        toggle_color = (100, 180, 100) if self.settings["music_enabled"] else (120, 120, 120)
        pygame.draw.rect(self.screen, toggle_color, self.music_toggle_rect, border_radius=16)
        circle_x = self.music_toggle_rect.right - 16 if self.settings["music_enabled"] else self.music_toggle_rect.left + 16
        pygame.draw.circle(self.screen, (240, 240, 240), (circle_x, self.music_toggle_rect.centery), 12)

        # Music volume
        pygame.draw.rect(self.screen, t["grid"], self.music_slider)
        knob_x = self._value_to_x(self.music_slider, self.settings["music_volume"])
        pygame.draw.circle(self.screen, t["text"], (knob_x, self.music_slider.centery), self.knob_radius)

        # SFX
        label = self.font.render("SFX:", True, t["text"])
        self.screen.blit(label, (self.sfx_slider.x - 120, self.sfx_slider.y - 20))
        pygame.draw.rect(self.screen, t["grid"], self.sfx_slider)
        knob_x = self._value_to_x(self.sfx_slider, self.settings["sfx_volume"])
        pygame.draw.circle(self.screen, t["text"], (knob_x, self.sfx_slider.centery), self.knob_radius)

        # Difficulty
        label = self.font.render("Difficulty:", True, t["text"])
        self.screen.blit(label, (self.music_slider.x - 120, 340))
        for key, text, rect in self.diff_rects:
            active = (self.settings["difficulty"] == key)
            bg = self._mix(t["button_idle"], t["accent"], 0.60) if active else t["button_idle"]
            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            pygame.draw.rect(self.screen, t["button_border"], rect, 2, border_radius=8)
            self.screen.blit(self.font.render(text, True, t["text"]), self.font.render(text, True, t["text"]).get_rect(center=rect.center))

        # Theme picker (новый)
        label = self.font.render("Theme:", True, t["text"])
        self.screen.blit(label, (self.music_slider.x - 120, 420))
        for key, rect in self.theme_rects:
            active = (self.settings.get("theme") == key)
            bg = self._mix(t["button_idle"], t["accent"], 0.60) if active else t["button_idle"]
            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            pygame.draw.rect(self.screen, t["button_border"], rect, 2, border_radius=8)
            self.screen.blit(self.font.render(key, True, t["text"]), self.font.render(key, True, t["text"]).get_rect(center=rect.center))

        # Back
        mouse_pos = pygame.mouse.get_pos()
        self._hover_back = self.back_btn.collidepoint(mouse_pos)
        bg = t["button_hover"] if self._hover_back else t["button_idle"]
        pygame.draw.rect(self.screen, bg, self.back_btn, border_radius=10)
        pygame.draw.rect(self.screen, t["button_border"], self.back_btn, 2, border_radius=10)
        self.screen.blit(self.font.render("BACK", True, t["text"]), self.font.render("BACK", True, t["text"]).get_rect(center=self.back_btn.center))
        pygame.display.flip()

    def _mix(self, a, b, k):
        return (int(a[0]*(1-k)+b[0]*k), int(a[1]*(1-k)+b[1]*k), int(a[2]*(1-k)+b[2]*k))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit(); raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.music_toggle_rect.collidepoint(event.pos):
                self.settings["music_enabled"] = not self.settings["music_enabled"]
                if self.on_click_sound: self.on_click_sound()
                self.on_change(self.settings)
            elif self.music_slider.collidepoint(event.pos):
                self.dragging = "music"
                self.settings["music_volume"] = self._x_to_value(self.music_slider, event.pos[0])
                if self.on_click_sound: self.on_click_sound()
                self.on_change(self.settings)
            elif self.sfx_slider.collidepoint(event.pos):
                self.dragging = "sfx"
                self.settings["sfx_volume"] = self._x_to_value(self.sfx_slider, event.pos[0])
                if self.on_click_sound: self.on_click_sound()
                self.on_change(self.settings)
            else:
                for key, _, rect in self.diff_rects:
                    if rect.collidepoint(event.pos):
                        self.settings["difficulty"] = key
                        if self.on_click_sound: self.on_click_sound()
                        self.on_change(self.settings)
                        break
                for key, rect in self.theme_rects:
                    if rect.collidepoint(event.pos):
                        self.settings["theme"] = key
                        if self.on_click_sound: self.on_click_sound()
                        self.on_change(self.settings)
                        break
                if self.back_btn.collidepoint(event.pos):
                    if self.on_click_sound: self.on_click_sound()
                    self.on_back()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging == "music":
                self.settings["music_volume"] = self._x_to_value(self.music_slider, event.pos[0])
                self.on_change(self.settings)
            elif self.dragging == "sfx":
                self.settings["sfx_volume"] = self._x_to_value(self.sfx_slider, event.pos[0])
                self.on_change(self.settings)
