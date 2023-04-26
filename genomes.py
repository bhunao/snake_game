import os
from random import randint

import neat
import pygame
from pygame.math import Vector2

from objects import Snake, Food, ScoreBoard, Background, Enemy

def game(genome, config):
    # Define Constants
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    WIDTH, HEIGHT = (800, 600)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    # network
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    snake = Snake()
    food = Food()
    score_board = ScoreBoard((0,0))
    bg = Background((WIDTH, HEIGHT))
    enemy = Enemy((3, 3))

    clock = pygame.time.Clock()
    while True:
        score = len(snake.segments)
        screen.fill(WHITE)
        bg.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.speed = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    snake.speed = Vector2(-1, 0)
                if event.key == pygame.K_UP:
                    snake.speed = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    snake.speed = Vector2(0, 1)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    snake = Snake()

        x = snake.pos.x * 57
        y = snake.pos.y * 57
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            genome.fitness -= 5
            print("Game Over")
            snake.alive = False
        if not snake.alive:
            break

        # snake.brain(food)
        snake.update()
        enemy.draw(screen)
        snake.draw(screen, enemy)

        food.draw(screen, border_radius=2, width=15)

        score_board.draw_score(screen, score)

        # TODO: separete when player collides with food and when it is near the food
        if abs(food.pos.x - snake.pos.x) <= 1:
            if abs(food.pos.y - snake.pos.y) <= 1:
                snake.grow(food)
                genome.fitness += 10
                food.pos = Vector2(
                    randint(0, WIDTH // 57 - 1),
                    randint(0, HEIGHT // 57 - 1)
                )


        pygame.display.update()
        clock.tick(60)
        # pygame.time.delay(100)

        # genome
        data = [
            snake.pos.x,
            snake.pos.y,
            food.pos.x,
            food.pos.y,
        ]
        # genome.fitness += 1
        activate = net.activate(data)
        if activate[0] > 0.5:
            snake.speed = Vector2(1, 0)
            print("right")
        elif activate[1] > 0.5:
            print("left")
            snake.speed = Vector2(-1, 0)
        elif activate[2] > 0.5:
            print("up")
            snake.speed = Vector2(0, -1)
        elif activate[3] > 0.5:
            print("down")
            snake.speed = Vector2(0, 1)


def run_neat(config):
    # Load the config file for the NEAT algorithm
    config = config

    # Create the population, which is the top-level object for a NEAT run
    p = neat.Population(config)
    # Load last population if exists
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-998')

    # Add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(50))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 999)

    # with open("best.pkl", "wb") as f:
    #     pickle.dump(winner, f)
    #
    # # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        game(genome, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
