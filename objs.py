# class that inherits from pygame.rect
# methods: update, draw, colliderect, ai
import pygame

# constants
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Snake(pygame.rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.direction = "right"
        self.speed = 1

    def update(self):
        if self.direction == "right":
            self.left += self.speed
        elif self.direction == "left":
            self.left -= self.speed
        elif self.direction == "up":
            self.top -= self.speed
        elif self.direction == "down":
            self.top += self.speed
    
    def draw_line(self, surface, color, start_pos, end_pos):
        pygame.draw.line(surface, color, start_pos, end_pos)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self)

    def colliderect(self, other):
        return self.colliderect(other)

    def ai(self, food):
        if self.left < food.left:
            self.direction = "right"
        elif self.left > food.left:
            self.direction = "left"
        elif self.top < food.top:
            self.direction = "down"
        elif self.top > food.top:
            self.direction = "up"

    def move(self):
        if self.direction == "right":
            self.left += self.speed
        elif self.direction == "left":
            self.left -= self.speed
        elif self.direction == "up":
            self.top -= self.speed
        elif self.direction == "down":
            self.top += self.speed

    def grow(self):
        self.speed += 1
        self.width += 10
        self.height += 10

    def die(self):
        print("Game Over")
        pygame.quit()
        quit()

# class Food that inherits from pygame.rect
# methods: draw, update, colliderect
class Food(pygame.rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self)

    def update(self):
        self.left += 1
        self.top += 1

    def colliderect(self, other):
        return self.colliderect(other)