# themes.py
import pygame

def make_fonts():
    return {
        "title": pygame.font.SysFont("Comic Sans", 72, bold=True),
        "menu":  pygame.font.SysFont("Comic Sans", 48),
        "h1":    pygame.font.SysFont("Comic Sans", 48, bold=True),
        "text":  pygame.font.SysFont("Comic Sans", 28),
    }

THEMES = {
    "Classic": {
        "bg": (0, 0, 20),
        "play_bg": (255, 255, 255),
        "grid": (100, 100, 100),
        "border": (0, 0, 0),
        "text": (255, 255, 255),
        "accent": (0, 200, 200),
        "panel_text": (255, 255, 255),
        "button_idle": (70, 70, 100),
        "button_hover": (120, 120, 180),
        "button_border": (200, 200, 250),
        "piece_colors": [
            (0,255,255),(255,255,0),(128,0,128),(0,255,0),
            (255,0,0),(0,0,255),(255,165,0)
        ],
        "fonts": make_fonts
    },
    "Neon": {
        "bg": (10, 10, 18),
        "play_bg": (10, 10, 18),
        "grid": (55, 55, 90),
        "border": (200, 255, 255),
        "text": (230, 230, 240),
        "accent": (0, 255, 200),
        "panel_text": (230, 230, 240),
        "button_idle": (40, 40, 70),
        "button_hover": (60, 60, 120),
        "button_border": (120, 240, 240),
        "piece_colors": [
            (0, 255, 200),(255, 255, 120),(180, 0, 255),(0, 255, 120),
            (255, 80, 120),(120, 120, 255),(255, 140, 0)
        ],
        "fonts": make_fonts
    },
    "Pastel": {
        "bg": (245, 245, 250),
        "play_bg": (250, 250, 255),
        "grid": (210, 210, 230),
        "border": (120, 120, 160),
        "text": (60, 60, 80),
        "accent": (140, 170, 230),
        "panel_text": (60, 60, 80),
        "button_idle": (220, 225, 245),
        "button_hover": (200, 210, 240),
        "button_border": (140, 170, 230),
        "piece_colors": [
            (140, 220, 220),(240, 240, 150),(190, 140, 210),(160, 220, 160),
            (240, 150, 150),(150, 160, 230),(255, 190, 120)
        ],
        "fonts": make_fonts
    },
    "Dark": {
        "bg": (18, 18, 18),
        "play_bg": (24, 24, 24),
        "grid": (50, 50, 50),
        "border": (200, 200, 200),
        "text": (230, 230, 230),
        "accent": (255, 140, 0),
        "panel_text": (230, 230, 230),
        "button_idle": (40, 40, 40),
        "button_hover": (70, 70, 70),
        "button_border": (160, 160, 160),
        "piece_colors": [
            (0,200,200),(220,220,60),(160,60,180),(80,200,80),
            (220,60,60),(80,80,220),(255,140,0)
        ],
        "fonts": make_fonts
    }
}

ORDERED_THEME_KEYS = ["Classic", "Neon", "Pastel", "Dark"]
