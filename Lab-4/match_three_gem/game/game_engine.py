import math
import pygame
from game.board import Board, GRID_SIZE, TILE_SIZE


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        offset_x = (width - (GRID_SIZE * TILE_SIZE)) // 2
        offset_y = (height - (GRID_SIZE * TILE_SIZE)) // 2 + 30

        self.board = Board(offset_x, offset_y, target_score=500, max_moves=20)

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 24)

        self.combo_text = None
        self.combo_until = 0

        self.hint = None
        self.last_input_time = pygame.time.get_ticks()

    def find_hint(self):
        """Return an adjacent pair of cells whose swap would make a match, or None."""
        board = self.board
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                for r2, c2 in ((r, c + 1), (r + 1, c)):
                    if r2 >= GRID_SIZE or c2 >= GRID_SIZE:
                        continue
                    board.swap_gems((r, c), (r2, c2))
                    matched = board.find_matches()
                    board.swap_gems((r, c), (r2, c2))
                    if matched:
                        return (r, c), (r2, c2)
        return None

    def handle_click(self, mouse_pos):
        self.hint = None
        self.last_input_time = pygame.time.get_ticks()

        if self.board.is_game_over() or self.board.is_animating():
            return

        mx, my = mouse_pos
        bx = mx - self.board.offset_x
        by = my - self.board.offset_y

        if 0 <= bx < GRID_SIZE * TILE_SIZE and 0 <= by < GRID_SIZE * TILE_SIZE:
            col = int(bx // TILE_SIZE)
            row = int(by // TILE_SIZE)

            if self.board.selected is None:
                self.board.selected = (row, col)
            else:
                prev_selected = self.board.selected
                if prev_selected == (row, col):
                    self.board.selected = None
                else:
                    if self.board.process_swap(prev_selected, (row, col)) and self.board.last_combo > 1:
                        self.combo_text = f"COMBO x{self.board.last_combo}!"
                        self.combo_until = pygame.time.get_ticks() + 1200
                    self.board.selected = None

    def reset(self):
        self.board.reset()
        self.combo_text = None
        self.hint = None
        self.last_input_time = pygame.time.get_ticks()

    def update(self):
        self.board.update()

        idle_ms = pygame.time.get_ticks() - self.last_input_time
        if (
            self.hint is None
            and idle_ms >= 5000
            and not self.board.is_animating()
            and not self.board.is_game_over()
        ):
            self.hint = self.find_hint()

    def render(self, screen):
        screen.fill((32, 34, 40))

        title_surf = self.font_big.render("MATCH-3 GEM SWAP", True, (240, 240, 240))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 10))
        hud_text = (
            f"SCORE: {self.board.score} / {self.board.target_score}   |   "
            f"MOVES LEFT: {self.board.moves_remaining}"
        )
        hud_surf = self.font_small.render(hud_text, True, (80, 220, 180))
        screen.blit(hud_surf, (self.width // 2 - hud_surf.get_width() // 2, 55))

        self.board.render(screen)

        if self.hint:
            pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
            glow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(
                glow, (255, 240, 120, int(80 + 175 * pulse)), glow.get_rect(),
                width=3 + int(3 * pulse), border_radius=12,
            )
            for r, c in self.hint:
                screen.blit(glow, (self.board.offset_x + c * TILE_SIZE, self.board.offset_y + r * TILE_SIZE))

        if self.combo_text and pygame.time.get_ticks() >= self.combo_until:
            self.combo_text = None
        if self.combo_text:
            combo_surf = self.font_big.render(self.combo_text, True, (255, 215, 70))
            screen.blit(
                combo_surf,
                (self.width // 2 - combo_surf.get_width() // 2, self.height // 2 - combo_surf.get_height() // 2),
            )

        inst_surf = self.font_small.render(
            "Swap gems to match 3+. Press [R] to Restart.",
            True,
            (180, 180, 180),
        )
        screen.blit(
            inst_surf, (self.width // 2 - inst_surf.get_width() // 2, self.height - 25)
        )

        result = self.board.check_result()
        if result:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            if result == "WIN":
                msg = "STAGE CLEARED!"
                color = (80, 220, 80)
            else:
                msg = "OUT OF MOVES!"
                color = (240, 80, 80)

            res_surf = self.font_big.render(msg, True, color)
            screen.blit(
                res_surf,
                (self.width // 2 - res_surf.get_width() // 2, self.height // 2 - 40),
            )

            sub_text = f"Final Score: {self.board.score}  |  Press [R] to Play Again"
            sub_surf = self.font_small.render(sub_text, True, (220, 220, 220))
            screen.blit(
                sub_surf,
                (self.width // 2 - sub_surf.get_width() // 2, self.height // 2 + 10),
            )