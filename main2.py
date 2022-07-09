import math, neat, pygame, random, sys, os

from config import *
from game_functions import check_wall_collision, get_random_snake
from models.food import Food
from models.score import Score
from models.snake import Snake

direction = "right"
gen_count = 0

# start pygame
pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

def eval_genomes(genomes, config):
    global gen_count
    gen_count += 1
    direction = "right"
    snakes = []
    scr = Score(screen, SCREEN_WIDTH - 252, 50, 0)
    snakes_alive = Score(screen, SCREEN_HEIGHT - 230, 50, 0)
    gen = Score(screen, SCREEN_HEIGHT - 400, 50, 0)

    ge = []
    nets = []

    for genome_id, genome in genomes:
        snakes.append(get_random_snake(screen))
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 1
        ge.append(genome)
        nets.append(net)

    food = Food(screen, 0, 0, FOOD_BLOCK_SIZE, FOOD_BLOCK_SIZE)
    food.spawn()



    # main game loop
    count = 0
    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
               # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # check if the event is a keypress
                elif event.type == pygame.KEYDOWN:
                    # if the key is escape, quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

        screen.fill(GRAY)
        scr.update(f'count: {count}')
        gen.update(f'gen: {gen_count}')
        snakes_alive.update(len(snakes))


        if not snakes:
           print("Game over the are no snakes left")
           return

        # update 
        for i, snake in enumerate(snakes):
            snk = snakes[i]
            snk.update()
            snk.draw_line(food.block)

            # neural network activation
            blocks = []
            for block in snk.body:
                blocks.append(block.x)
                blocks.append(block.y)
            
            blocks.append(food.block.x)
            blocks.append(food.block.y)

            blocks = [
                snk.block.x,
                snk.block.y,
                math.hypot(snk.x - food.block.x, snk.y - food.block.y)
            ]

            output = nets[i].activate((*blocks,))
            for output_index, output_value in enumerate(output):
                if output_value > 0.5:
                    if output_index == 0:
                        snk.direction = "right"
                    if output_index == 1:
                        snk.direction = "left"
                    if output_index == 2:
                        snk.direction = "up"
                    if output_index == 3:
                        snk.direction = "down"
        
            for block in snk.body[1:]:
                if ge:
                    try:
                        dist = math.hypot(snk.x - food.block.x, snk.y - food.block.y)
                        dist_score = int(dist / 250)
                        # print(dist_score)
                        if check_wall_collision(snk.block) or ge[i].fitness < -SCREEN_HEIGHT:
                            #print("hit a wall")
                            snk.score.update(snk.score.score - 1)
                            ge[i].fitness -= 50
                            # removing the snake from the list to of survivors
                            snakes.pop(i)
                            ge.pop(i)
                            nets.pop(i)
                        elif snk.check_collision(food.block) or dist < 30:
                            print(f"Score: {snk.score.score=}")
                            snk.grow()
                            food.spawn()
                            snake.score.update(ge[i].fitness)
                            ge[i].fitness += 50
                        elif dist < 200:
                            snake.score.update(ge[i].fitness)
                            ge[i].fitness += 5 - int(dist / 250) 
                        elif dist > 300:
                            snake.score.update(ge[i].fitness)
                            ge[i].fitness -= int(dist / 250) * 5
                    except Exception as e:
                        print(e)

                else:
                    print("No genomes left")
                    return

        food.update()

        if snake.check_collision(food.block):
            snake.grow()
            food.spawn()

        pygame.display.update()
        pygame.time.delay(1)
        
        count += 1
        if count > 1000:
            return

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    pop = neat.Population(config)
    pop.run(eval_genomes, 500)


# run the main function
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

