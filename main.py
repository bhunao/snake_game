import re
import pygame


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.color = (0, 255, 0)
    

class Snake(Cell):
    name: str = "Snake"
    color1 = (0, 255, 0)
    color2 = (0, 100, 0)

    def update(self, direction=None) -> None:
        if direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1
        elif direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        
        print(self.x, self.y)

class Food(Cell):
    name: str = "Snake"
    color1 = (255, 0, 0)
    color2 = (100, 0, 0)


class Display:
    def __init__(self, objects=[]) -> None:
        self.cell_size = 20
        self.size = 30
        self.width = self.cell_size * self.size
        self.height = self.cell_size * self.size
        self.objects = objects
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("snake")
    
    def draw_on_pos(self, x, y, color1, color2):
        cell_x = x * self.cell_size
        cell_y = y * self.cell_size
        width = self.cell_size
        height = self.cell_size
        rect1 = pygame.Rect(cell_x, cell_y, width*.9, height*.9)
        pygame.draw.rect(self.display, color1, rect1)
        rect2 = pygame.Rect(cell_x, cell_y, width*.6, height*.6)
        rect2.center = rect1.center
        pygame.draw.rect(self.display, color2, rect2)

    
    def draw_grid(self) -> None:
        GRAY = (100, 100, 100)
        DARK_GRAY = (50, 50, 50)
        for column in range(30):
            for row in range(30):
                self.draw_on_pos(column, row, GRAY, DARK_GRAY)

    
    def draw(self) -> None:
        LIGHT_GRAY = (128, 128, 128)
        self.display.fill(LIGHT_GRAY)
        self.draw_grid()
        for obj in self.objects:
                self.draw_on_pos(obj.x, obj.y, obj.color1, obj.color2)

        pygame.display.update()
        pygame.time.delay(10)
    
    def movement(self, obj) -> None:
            # input handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                obj.update("up")
            elif keys[pygame.K_DOWN]:
                obj.update("down")
            elif keys[pygame.K_LEFT]:
                obj.update("left")
            elif keys[pygame.K_RIGHT]:
                obj.update("right")
            elif keys[pygame.K_ESCAPE]:
                running = False

    def loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            snake = self.objects[0]
            self.movement(snake)


            self.draw()


snk = Snake(1, 1)
Display([snk]).loop()