import pygame
import sys
import random
import os
from UI import UI
from board import Board
from piece import Piece
from constants import *
from Menu import Menu
from HighScoreScreen import HighScoreScreen
from GameOverScreen import GameOverScreen
from NameInputScreen import NameInputScreen
from PauseScreen import PauseScreen
from SettingsScreen import SettingsScreen
from themes import THEMES


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Play Game')

        self.settings = {
            "music_enabled": True,
            "music_volume": 0.35,
            "sfx_volume": 0.7,
            "difficulty": "normal",
            "theme": "Classic"
        }

        self.theme = self._load_theme(self.settings["theme"])
        self.fonts = self.theme["fonts"]()

        self.state = "menu"
        self.board = Board(BOARD_HEIGHT_BLOCKS, BOARD_WIDTH_BLOCKS)

        self.piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS,self.theme["piece_colors"])
        self.next_piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS,self.theme["piece_colors"])

        snd_dir = os.path.join("assets", "sounds")
        self.music_path = os.path.join(snd_dir, "music_game.mp3")

        self.snd_clear = pygame.mixer.Sound(os.path.join(snd_dir, "break_line.mp3"))
        self.snd_lock = pygame.mixer.Sound(os.path.join(snd_dir, "down_shape.mp3"))
        self.snd_over = pygame.mixer.Sound(os.path.join(snd_dir, "game_over.mp3"))
        self.snd_select = pygame.mixer.Sound(os.path.join(snd_dir, "select.mp3"))


        self.snd_clear.set_volume(0.7)
        self.snd_lock.set_volume(0.6)
        self.snd_over.set_volume(0.9)
        self.snd_select.set_volume(0.8)

        self.panel = UI(x=450, y=100, font=self.fonts.get("text"))
        self.panel.reset_score()


        self.menu = Menu(
            self.screen,
            on_start=self._start_game,
            on_scores=self._show_scores,
            on_quit=self._quit_game,
            on_settings=self._show_settings,
            on_click_sound=self.play_select,
            theme=self.theme,
            fonts=self.fonts,
        )

        self.running = True
        self.fall_interval = 500
        self.last_fall_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.player_name = None
        self._over_sound_played = False

        self.high_score_screen = HighScoreScreen(
            self.screen, on_back=self._back_to_menu, on_click_sound=self.play_select,
            theme=self.theme, fonts=self.fonts
        )

        self.name_input_screen = NameInputScreen(
            self.screen, on_done=self._set_player_name,
            theme=self.theme, fonts=self.fonts
        )

        self.game_over_screen = GameOverScreen(
            self.screen, on_back_to_menu=self._back_to_menu, on_click_sound=self.play_select,
            theme=self.theme, fonts=self.fonts
        )

        self.pause_screen = PauseScreen(
            self.screen, on_resume=self._resume_game, on_back_to_menu=self._back_to_menu,
            on_click_sound=self.play_select, theme=self.theme, fonts=self.fonts
        )

        self.settings_screen = SettingsScreen(
            self.screen,
            settings=self.settings,
            on_change=self._apply_settings,
            on_back=self._back_to_menu,
            on_click_sound=self.play_select,
            theme=self.theme,
            fonts=self.fonts,
        )

        self._apply_difficulty(self.settings["difficulty"])
        self._apply_sfx_volume()


    def _apply_settings(self, settings):
        # Музыка
        if self.state == "playing":
            if settings["music_enabled"]:
                if not pygame.mixer.music.get_busy():
                    try:
                        pygame.mixer.music.load(self.music_path)
                    except pygame.error:
                        print("Ошибка загрузки музыки:", self.music_path)
                    else:
                        pygame.mixer.music.set_volume(settings["music_volume"])
                        pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.set_volume(settings["music_volume"])
            else:
                pygame.mixer.music.stop()

        # SFX
        self._apply_sfx_volume()

        # Сложность
        self._apply_difficulty(settings["difficulty"])

        # ### ТЕМА
        new_theme = self._load_theme(settings.get("theme", "Classic"))
        if new_theme is not self.theme:
            self.theme = new_theme
            self.fonts = self.theme["fonts"]()

            self.high_score_screen.theme = self.theme
            self.high_score_screen.title_font = self.fonts.get("h1", self.high_score_screen.title_font)
            self.high_score_screen.font = self.fonts.get("text", self.high_score_screen.font)

            self.game_over_screen.theme = self.theme
            self.game_over_screen.title_font = self.fonts.get("title", self.game_over_screen.title_font)
            self.game_over_screen.font = self.fonts.get("menu", self.game_over_screen.font)

            self.name_input_screen.theme = self.theme
            self.name_input_screen.title_font = self.fonts.get("h1", self.name_input_screen.title_font)
            self.name_input_screen.font = self.fonts.get("text", self.name_input_screen.font)

            self.pause_screen.theme = self.theme
            self.pause_screen.title_font = self.fonts.get("h1", self.pause_screen.title_font)
            self.pause_screen.btn_font = self.fonts.get("text", self.pause_screen.btn_font)

            # Обновим экраны/шрифты
            self.menu.theme = self.theme
            self.menu.title_font = self.fonts.get("title", self.menu.title_font)
            self.menu.font = self.fonts.get("menu", self.menu.font)

            self.settings_screen.theme = self.theme
            self.settings_screen.title_font = self.fonts.get("h1", self.settings_screen.title_font)
            self.settings_screen.font = self.fonts.get("text", self.settings_screen.font)

            # Панель
            self.panel.font = self.fonts.get("text", self.panel.font)



            # Новые цвета для следующих фигур
            self.piece.color = self.theme["piece_colors"][self.piece.shape_index]
            self.next_piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS,
                                    self.theme["piece_colors"])

    def _apply_difficulty(self, difficulty):
        if difficulty == "easy":
            self.fall_interval = 700
        elif difficulty == "normal":
            self.fall_interval = 500
        elif difficulty == "hard":
            self.fall_interval = 300

    # ---------- GAME LOOP ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.piece.x += 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.x -= 1

                elif event.key == pygame.K_LEFT:
                    self.piece.x -= 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.x += 1

                elif event.key == pygame.K_DOWN:
                    self.piece.y += 1
                    if not self.board.is_valid_position(self.piece):
                        self.piece.y -= 1

                elif event.key == pygame.K_p:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.pause()
                    self.play_select()
                    self.state = "pause"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                old_rotation = self.piece.rotation
                self.piece.rotate()
                if not self.board.is_valid_position(self.piece):
                    self.piece.rotation = old_rotation

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > self.fall_interval:
            self.piece.y += 1
            if not self.board.is_valid_position(self.piece):
                self.piece.y -= 1
                self.board.place_piece(self.piece)
                self.snd_lock.play()

                lines = self.board.clear_rows()
                if lines:
                    self.panel.add_score(lines)
                    self.snd_clear.play()
                else:
                    self.panel.add_score(0)

                self.piece = self.next_piece
                self.next_piece = Piece(random.randint(0, len(SHAPES) - 1),
                                        BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS,self.theme["piece_colors"])

                if not self.board.is_valid_position(self.piece):
                    self.panel.save_scores(self.player_name)
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    self._over_sound_played = False
                    self.state = "game_over"

            self.last_fall_time = current_time

    def draw(self):
        # общий фон
        self.screen.fill(self.theme["bg"])

        # рисуем падающую фигуру поверх поля, поэтому сначала поле:
        self.board.draw(self.screen, self.theme)

        # падающая фигура
        for x, y in self.piece.get_blocks():
            if y >= 0:
                rect_x = PLAY_AREA_X + x * GRID_SIZE
                rect_y = PLAY_AREA_Y + y * GRID_SIZE
                pygame.draw.rect(self.screen, self.piece.color, (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, self.theme["grid"], (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)

        # панель
        self.panel.draw(self.screen, self.next_piece, self.theme)
        pygame.display.flip()

    def run(self):
        while self.running:
            if self.state == "menu":
                for event in pygame.event.get():
                    self.menu.handle_event(event)
                self.menu.draw()
                pygame.display.flip()

            elif self.state == "name_input":
                for event in pygame.event.get():
                    self.name_input_screen.handle_event(event)
                self.name_input_screen.draw()
                pygame.display.flip()

            elif self.state == "playing":
                self.handle_events()
                self.update()
                self.draw()

            elif self.state == "scores":
                for event in pygame.event.get():
                    self.high_score_screen.handle_event(event)
                self.high_score_screen.draw(self.panel.highscores)
                pygame.display.flip()

            elif self.state == "pause":
                for event in pygame.event.get():
                    self.pause_screen.handle_event(event)
                self.pause_screen.draw()

            elif self.state == "settings":
                for event in pygame.event.get():
                    self.settings_screen.handle_event(event)
                self.settings_screen.draw()

            elif self.state == "game_over":
                if not self._over_sound_played:
                    pygame.mixer.music.stop()
                    self.snd_over.play()
                    self._over_sound_played = True

                for event in pygame.event.get():
                    self.game_over_screen.handle_event(event)

                self.game_over_screen.draw(self.panel.score)
                pygame.display.flip()

            self.clock.tick(60)

        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    # ---------- CALLBACKS ----------
    def _start_game(self):
        pygame.time.delay(120)
        self.state = "name_input"

    def _show_scores(self):
        self.state = "scores"

    def _show_settings(self):
        self.state = "settings"

    def _quit_game(self):
        pygame.mixer.music.stop()
        self.running = False

    def _back_to_menu(self):
        self.state = "menu"
        if hasattr(self, "menu"):
            self.menu.selected_index = -1
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def play_select(self):
        self.snd_select.play()

    def _set_player_name(self, name):
        self.player_name = name
        self.board = Board(BOARD_HEIGHT_BLOCKS, BOARD_WIDTH_BLOCKS)
        self.piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS,
                           self.theme["piece_colors"])
        self.next_piece = Piece(random.randint(0, len(SHAPES) - 1), BOARD_WIDTH_BLOCKS, BOARD_HEIGHT_BLOCKS,
                                self.theme["piece_colors"])
        self.panel.reset_score()
        self.last_fall_time = pygame.time.get_ticks()

        if self.settings["music_enabled"]:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(self.settings["music_volume"])
            pygame.mixer.music.play(-1)

        self.state = "playing"

    def _resume_game(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()
        self.state = "playing"


    def _load_theme(self, key):
        return THEMES.get(key, THEMES["Classic"])

    def _apply_sfx_volume(self):
        v = self.settings["sfx_volume"]
        self.snd_clear.set_volume(v)
        self.snd_lock.set_volume(v)
        self.snd_over.set_volume(v)
        self.snd_select.set_volume(v)




