import math
import random
import pygame

GRID_SIZE = 8
TILE_SIZE = 60
GEM_COLORS = [
    (220, 50, 50),   # Red
    (50, 200, 50),   # Green
    (50, 100, 240),  # Blue
    (240, 200, 40),  # Yellow
    (180, 50, 220),  # Purple
    (240, 130, 40),  # Orange
]


class Gem:
   
    def __init__(self, color, target_row, col):
        self.color = color
        self.target_row = target_row
        self.col = col
        # Start higher up to animate falling down
        self.current_y = (target_row - 2) * TILE_SIZE
        self.target_y = target_row * TILE_SIZE
        self.fall_speed = 12.0
        self.is_bomb = False

    def update(self):
        if self.current_y < self.target_y:
            self.current_y += self.fall_speed
            if self.current_y > self.target_y:
                self.current_y = self.target_y

    def is_animating(self):
        return self.current_y < self.target_y


class Board:
    """Manages animated gem grid, gravity drops, score, and game limits."""

    def __init__(self, offset_x, offset_y, target_score=500, max_moves=20):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.target_score = target_score
        self.max_moves = max_moves
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected = None
        self.score = 0
        self.moves_remaining = max_moves
        self.last_combo = 0
        self.reset()

    def reset(self):
        """Reset board grid, score, and move limits."""
        self.score = 0
        self.moves_remaining = self.max_moves
        self.selected = None
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                color = random.choice(GEM_COLORS)
                gem = Gem(color, r, c)
                gem.current_y = gem.target_y  # Snap instantly on initial start
                self.grid[r][c] = gem

        self.resolve_matches(spawn_bombs=False)

    def is_animating(self):
        """Returns True if any gem is currently dropping down."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] and self.grid[r][c].is_animating():
                    return True
        return False

    def swap_gems(self, pos1, pos2):
        """Swap positions and target render coordinates of two gems."""
        r1, c1 = pos1
        r2, c2 = pos2

        g1, g2 = self.grid[r1][c1], self.grid[r2][c2]
        self.grid[r1][c1], self.grid[r2][c2] = g2, g1

        if self.grid[r1][c1]:
            self.grid[r1][c1].target_row = r1
            self.grid[r1][c1].target_y = r1 * TILE_SIZE
            self.grid[r1][c1].current_y = r1 * TILE_SIZE

        if self.grid[r2][c2]:
            self.grid[r2][c2].target_row = r2
            self.grid[r2][c2].target_y = r2 * TILE_SIZE
            self.grid[r2][c2].current_y = r2 * TILE_SIZE

    def is_adjacent(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def find_runs(self):
        """Return every maximal horizontal/vertical run of 3+ same-colored gems as (cells, axis)."""
        runs = []
        for axis in ("row", "col"):
            for line in range(GRID_SIZE):
                cells = [(line, i) if axis == "row" else (i, line) for i in range(GRID_SIZE)]
                start = 0
                for end in range(1, GRID_SIZE + 1):
                    if end < GRID_SIZE:
                        a = self.grid[cells[start][0]][cells[start][1]]
                        b = self.grid[cells[end][0]][cells[end][1]]
                        if a and b and a.color == b.color:
                            continue
                    if end - start >= 3:
                        runs.append((cells[start:end], axis))
                    start = end
        return runs

    def find_matches(self):
        """Scan grid for horizontal and vertical 3-in-a-row color matches."""
        matched = set()
        for cells, _ in self.find_runs():
            matched.update(cells)
        return matched

    def cells_to_clear(self, runs):
        """Matched cells plus the rows/columns wiped out by any bombs caught in them."""
        cleared = set()
        blasts = []
        for cells, axis in runs:
            cleared.update(cells)
            blasts += [(pos, axis) for pos in cells if self.grid[pos[0]][pos[1]].is_bomb]

        detonated = set()
        while blasts:
            (r, c), axis = blasts.pop()
            if (r, c) in detonated:
                continue
            detonated.add((r, c))
            line = [(r, i) for i in range(GRID_SIZE)] if axis == "row" else [(i, c) for i in range(GRID_SIZE)]
            for pos in line:
                cleared.add(pos)
                # A bomb caught in the blast goes off across the other axis
                if self.grid[pos[0]][pos[1]].is_bomb and pos not in detonated:
                    blasts.append((pos, "col" if axis == "row" else "row"))
        return cleared, detonated

    def drop_and_refill(self):
        for c in range(GRID_SIZE):
            empty_slots = 0
            for r in range(GRID_SIZE - 1, -1, -1):
                if self.grid[r][c] is None:
                    empty_slots += 1
                elif empty_slots > 0:
                    gem = self.grid[r][c]
                    gem.target_row = r + empty_slots
                    gem.target_y = (r + empty_slots) * TILE_SIZE
                    self.grid[r + empty_slots][c] = gem
                    self.grid[r][c] = None

            for r in range(empty_slots):
                color = random.choice(GEM_COLORS)
                gem = Gem(color, r, c)
                gem.current_y = -((empty_slots - r) * TILE_SIZE)
                self.grid[r][c] = gem

    def resolve_matches(self, swapped=(), spawn_bombs=True):
        """Clear matches until the board settles; each cascade step scores a higher multiplier.

        A run of 4+ leaves a bomb behind, on the swapped cell if it is part of the run.
        """
        points = 0
        combo = 0
        while True:
            runs = self.find_runs()
            if not runs:
                break
            combo += 1
            cleared, detonated = self.cells_to_clear(runs)
            points += len(cleared) * 10 * combo

            new_bombs = set()
            if spawn_bombs:
                for cells, _ in runs:
                    if len(cells) >= 4:
                        spot = next((p for p in swapped if p in cells), cells[len(cells) // 2])
                        if spot not in detonated:
                            new_bombs.add(spot)

            for r, c in cleared - new_bombs:
                self.grid[r][c] = None
            for r, c in new_bombs:
                self.grid[r][c].is_bomb = True
            self.drop_and_refill()
            swapped = ()  # Cascades place bombs mid-run
        self.last_combo = combo
        return points

    def process_swap(self, pos1, pos2):
        if not self.is_adjacent(pos1, pos2) or self.is_game_over() or self.is_animating():
            return False

        self.swap_gems(pos1, pos2)
        matches = self.find_matches()

        if not matches:
            self.swap_gems(pos1, pos2)  # Revert invalid swap
            return False

        self.moves_remaining -= 1
        self.score += self.resolve_matches(swapped=(pos2, pos1))
        return True

    def is_game_over(self):
        return self.score >= self.target_score or self.moves_remaining <= 0

    def check_result(self):
        if self.score >= self.target_score:
            return "WIN"
        if self.moves_remaining <= 0:
            return "LOSS"
        return None

    def update(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]:
                    self.grid[r][c].update()

    def render(self, surface):
        board_rect = pygame.Rect(
            self.offset_x, self.offset_y, GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE
        )
        pygame.draw.rect(surface, (20, 22, 28), board_rect, border_radius=8)
        pygame.draw.rect(surface, (60, 65, 75), board_rect, width=3, border_radius=8)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                gem = self.grid[r][c]
                if gem:
                    x = self.offset_x + c * TILE_SIZE
                    y = self.offset_y + gem.current_y
                    tile_rect = pygame.Rect(x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4)

                    pygame.draw.rect(surface, gem.color, tile_rect, border_radius=10)
                    pygame.draw.rect(
                        surface, (255, 255, 255), tile_rect, width=1, border_radius=10
                    )

                    if gem.is_bomb:
                        pulse = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2
                        glow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        pygame.draw.rect(
                            glow, (255, 255, 255, int(90 + 140 * pulse)), glow.get_rect(),
                            width=4, border_radius=12,
                        )
                        surface.blit(glow, (x, y))
                        pygame.draw.circle(surface, (20, 22, 28), tile_rect.center, 12)
                        pygame.draw.circle(surface, (255, 255, 255), tile_rect.center, 6 + 3 * pulse)

                if self.selected == (r, c):
                    sel_x = self.offset_x + c * TILE_SIZE
                    sel_y = self.offset_y + r * TILE_SIZE
                    sel_rect = pygame.Rect(sel_x + 2, sel_y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
                    pygame.draw.rect(
                        surface, (255, 255, 255), sel_rect, width=4, border_radius=10
                    )