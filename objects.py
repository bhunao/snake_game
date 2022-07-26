import pygame
from pygame import Vector2, draw, font, Color, Rect, mixer, event

from custom_events import ANIMATION_ON_GROW, PLAYER_DEATH
from functions import change_color
from colors import PB as pallet


class BaseObject:
    full_block = 40
    block_size = full_block - 2

    def __init__(self, pos=(5, 5), color=None):
        self.pos = Vector2(pos)
        self.color = color if color else Color(12, 103, 201)
        self.rect = Rect(*self.pos, self.block_size, self.block_size)

    def _draw(self, screen, pos=None, color=None, *args, **kwargs):
        pos = pos if pos else self.pos
        color = color if color else self.color
        pos = Vector2(pos) * self.full_block
        rect = Rect(*pos, self.block_size, self.block_size)
        draw.rect(screen, color, rect, *args, **kwargs)

    def draw(self, screen, *args, **kwargs):
        self._draw(screen, self.pos, *args, **kwargs)

    def draw_border(self, screen, *args, **kwargs):
        self._draw(screen, self.pos, change_color(self.color), *args, **kwargs)


class Snake(BaseObject):
    def __init__(self, pos=(5, 5), color=None):
        super().__init__(pos, color)
        self.pos = Vector2(pos)
        segment_color = pallet.COLOR2
        self.segments = [
            [Vector2(self.pos.x, self.pos.y + add),
             segment_color,
             0]
            for add in range(3)
        ]
        self.speed = Vector2(1, 0)
        self.color = segment_color
        self.auto = False
        self.eat_sound = mixer.Sound('sounds/eat.wav')
        self.die_sound = mixer.Sound('sounds/game_over.wav')
        self.alive = True
        self.next_move = pygame.time.get_ticks() + 100  # 100ms = 0.1s

    def respawn(self):
        s = Snake((5, 5))
        self.__dict__.update(s.__dict__)

    def brain(self, food):
        distance = Vector2(food.pos - self.pos)
        if self.auto:
            if distance.x >= 1:
                self.speed = Vector2(1, 0)
            elif distance.x <= -1:
                self.speed = Vector2(-1, 0)
            elif distance.y >= 1:
                self.speed = Vector2(0, 1)
            elif distance.y <= -1:
                self.speed = Vector2(0, -1)

    def collision(self):
        for segment, color, type_ in self.segments[1:]:
            if type_ != 0:
                return
            if segment == self.pos:
                # mixer.Sound.play(self.die_sound)
                self.speed = Vector2(0, 0)
                self.alive = False
                event.post(PLAYER_DEATH)
                if self.auto:
                    self.segments = self.segments[1:3]
                return True
        return False

    def update(self):
        if pygame.time.get_ticks() > self.next_move:
            self.next_move = pygame.time.get_ticks() + 100
        else:
            return
        if not self.alive:
            return
        self.collision()
        new_pos = self.pos + self.speed
        old_head_color = self.segments[0][1]
        new_head = [new_pos, old_head_color, 0]
        self.segments.insert(0, new_head)
        self.pos = new_pos
        self.segments.pop()

    def draw(self, screen, *args, **kwargs):
        for segment, color, type_ in self.segments:
            pos = segment
            self._draw(screen, pos, color, border_radius=2)
            self._draw(screen, pos, pallet.COLOR3, border_radius=2, width=5)

    def grow(self, food):
        self.segments.insert(1, [food.pos, pallet.COLOR4, 1])
        pygame.event.post(ANIMATION_ON_GROW)
        # mixer.Sound.play(self.eat_sound)


class Food(BaseObject):
    def __init__(self, pos=(5, 5)):
        super().__init__(pos)
        self.color = pallet.COLOR1


class Text:
    def __init__(self, pos, text=None, size=80, color=None, font_=None):
        self.pos = Vector2(pos)
        self.text = text if text else ""
        self.size = size
        self.color = color if color else pallet.COLOR4
        self.font = font_ if font_ else font.SysFont('Arial', size)

    def draw(self, screen, text=""):
        text = self.font.render(f'{self.text}{text}', True, self.color)
        text_rect = text.get_rect(center=(self.pos))
        draw.rect(screen, pallet.COLOR3, text_rect)
        draw.rect(screen, pallet.COLOR2, text_rect, width=1)
        screen.blit(text, text_rect)


class ScoreBoard(BaseObject):
    def __init__(self, pos=(5, 5)):
        super().__init__(pos)
        self.color = (0, 0, 255)

    def draw_score(self, screen, score):
        pos = self.pos * 57
        font_ = font.SysFont("Arial", 30)
        text = font_.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text, (pos.x, pos.y))


class Background:
    size: Vector2

    def __init__(self, size):
        width = size[0] // BaseObject.full_block + 1
        height = size[1] // BaseObject.full_block + 1
        self.size = Vector2(size)
        self.cells = [[BaseObject((x, y)) for x in range(width)] for y in range(height)]

    def draw(self, screen):
        for list_ in self.cells:
            for cell in list_:
                cell.draw(screen, pallet.COLOR4)
                cell.draw(screen, color=pallet.COLOR5, width=5)


class Effect:
    def __init__(self, pos, color: Color = pallet.COLOR3, size=1, total_frames=80):
        self.pos: Vector2 = Vector2(pos)
        self.color: Color = color
        self.size: int = size
        self.total_frames: int = total_frames
        self.is_over: bool = False
        self.velocity = 5

    def draw(self, screen):
        if self.is_over:
            return
        rect = Rect(self.pos.x, self.pos.y, self.size, self.size)
        rect.center = self.pos
        draw.rect(screen, self.color, rect, width=2)
        self.total_frames -= 1
        if self.total_frames <= 0:
            self.is_over = True

    def update(self):
        if self.total_frames <= 0:
            self.is_over = True
            return
        self.size += self.velocity
        self.total_frames -= 1

