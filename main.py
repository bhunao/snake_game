# snake game
# using pygame
# size of the screen is 640x480
import random
import pygame


pygame.init()
# create screen
screen = pygame.display.set_mode((640, 480))
# set title of the window
pygame.display.set_caption("Snake Game")
# set background color
GRAY = (100, 100, 100)
screen.fill(GRAY)

# snake blocks are 20x20 pixels

# constants
# colors RED, GREEN, BLUE, WHITE

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# snake starting position and direction
# snake starts in the middle of the screen
# snake starts moving to the right
# snake starts with a length of 3
# snake is a list of rectangles
snake = [
    pygame.Rect(300, 240, 20, 20),
    pygame.Rect(280, 240, 20, 20),
    pygame.Rect(260, 240, 20, 20)
]

# food is a rectangle
# food is placed randomly on the screen
# food is 20x20 pixels
food = pygame.Rect(random.randint(0, 520), random.randint(0, 460), 20, 20)

# spawn food if snake eats food
def snake_eats_food():
    # if snake head is at the same position as food
    if snake[0].colliderect(food):
        # spawn new food
        food.left = random.randint(0, 520)
        food.top = random.randint(0, 460)
        # add a new snake block
        snake.append(pygame.Rect(0, 0, 20, 20))
        return True
    else:
        return False

# draw snake
def draw_snake():
    before_block_pos = None
    # draw snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, block)

# draw food
def draw_food():
    pygame.draw.rect(screen, RED, food)

# move snake
def move_snake():
    # move snake
    for i in range(len(snake) - 1, 0, -1):
        # move snake block
        snake[i].left = snake[i - 1].left
        snake[i].top = snake[i - 1].top
    # move snake head
    if direction == "right":
        snake[0].left += 20
    elif direction == "left":
        snake[0].left -= 20
    elif direction == "up":
        snake[0].top -= 20
    elif direction == "down":
        snake[0].top += 20
    # # if snake hits the wall
    # if snake[0].left < 0:
    #     snake[0].left = 640
    # elif snake[0].top < 0:
    #     snake[0].top = 480
    # elif snake[0].left > 640:
    #     snake[0].left = 0
    # elif snake[0].top > 480:
    #     snake[0].top = 0
    # if snake hits itself
    for block in snake[1:]:
        if snake[0].colliderect(block):
            print("Game Over")
            restart_game()
            # pygame.quit()
            # quit()

# restart game
def restart_game():
    global direction
    global score
    global snake
    global food
    direction = "right"
    score = 0
    snake = [
        pygame.Rect(300, 240, 20, 20),
        pygame.Rect(280, 240, 20, 20),
        pygame.Rect(260, 240, 20, 20)
    ]
    food = pygame.Rect(random.randint(0, 520), random.randint(0, 460), 20, 20)

# path finding for the snake to search for food
# avoiding walls and itself
# get snake head position
# get food position
# get snake and food position difference
def get_snake_food_difference():
    # get snake head position
    snake_head_pos = snake[0]
    # get food position
    food_pos = food
    # get snake and food position difference
    snake_food_difference = (snake_head_pos.left - food_pos.left, snake_head_pos.top - food_pos.top)
    print(f'snake_food_difference: {snake_food_difference}')
    return snake_food_difference

def path_finding():
    global direction
    diff = get_snake_food_difference()
    if abs(diff[0]) > abs(diff[1]):
        # if snake and food difference[0] is > 0 then snake is to the right of food
        # else if snake and food difference[0] is < 0 then snake is to the left of food
        if diff[0] > 0:
            direction = "left"
        elif diff[0] < 0:
            direction = "right"
    else:
        # if snake and food difference[1] is > 0 then snake is above food
        # else if snake and food difference[1] is < 0 then snake is below food
        if diff[1] > 0:
            direction = "up"
        elif diff[1] < 0:
            direction = "down"


# score is the length of the snake
score = len(snake)

# draw score
def draw_score():
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (0, 0))


                                                                                


# main loop
running = True
direction = "right"
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_UP:
                direction = "up"
            elif event.key == pygame.K_DOWN:
                direction = "down"
    # update
    # move snake
    move_snake()
    # spawn food if snake eats food
    if snake_eats_food():
        score += 1
    # draw
    screen.fill(GRAY)
    draw_snake()
    draw_food()
    draw_score()
    # path finding
    path_finding()
    # update screen
    pygame.display.update()
    # delay
    pygame.time.delay(100)