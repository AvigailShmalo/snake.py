import pygame
import sys
import random

class Snake(object):
    def __init__(self):
        self.length = 1
        self.position = [((SCREEN_WIDTH / 2), (SCREEN_HIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
        self.score = 0


    def get_head_position(self):
        return self.position[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1)== self.direction:
            return 
        else:
            self.direction = point
    
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new =(((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HIGHT)
        # collition with self
        if len(self.position) > 2 and new in self.position[2:]:
            game_over(self)
            self.reset()
        elif new[0] > SCREEN_WIDTH or new[0] < 0 or new[1] > SCREEN_HIGHT or new[1] < 0:
            game_over(self)
            self.reset()
        else:
            self.position.insert(0, new)
            if len(self.position) > self.length:
                self.position.pop()   
    
    def reset(self):
        self.length = 1
        high_score = 0
        with open('high_score.txt', "r") as f:
            high_score = f.readline()
        if self.score > int(high_score):
            with open('high_score.txt', "w") as f:
                f.write(str(self.score))
        self.score = 0
        self.position = [((SCREEN_WIDTH /2), (SCREEN_HIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    def draw(self, surface):
        for p in self.position:
            pygame.draw.rect(surface, (255, 255, 255), (p[0], p[1], GRIDSIZE, GRIDSIZE))

    def keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_a:
                    self.reset()



class Food(object):
    def __init__(self):
        self.postion = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.postion = (random.randint(0, GRID_WIDTH-1)* GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.postion[0], self.postion[1], GRIDSIZE, GRIDSIZE))

def drawGrid(surface):
    for y in range (0, int(GRID_HEIGHT)):
        for x in range(0, int (GRID_WIDTH)):
            if (x + y) % 2==0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)

            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)



SCREEN_WIDTH = 480
SCREEN_HIGHT= 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 24)

    while(True):
        clock.tick(10)
        snake.keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position()==food.postion:
            snake.length +=1
            snake.score +=1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        hs = 0
        with open('high_score.txt', "r") as f:
            hs = f.readline()
        hs_text = myfont.render(f"High Score: {hs}", True,(255, 255, 255))
        text = myfont.render(f"Score: {snake.score}", True,(255, 255, 255))
        screen.blit(surface, (0,0))
        screen.blit(text, (10, 10))
        screen.blit(hs_text, (SCREEN_WIDTH - hs_text.get_width() - 10, 10))
        pygame.display.update()

def game_over(snake):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    food = Food()

    myfont = pygame.font.SysFont("monospace", 24)
    myfont2 = pygame.font.SysFont("monospace", 50)

    run = True
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
        

        drawGrid(surface)
        
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render(f"Score: {snake.score}", True,(255, 255, 255))
        game_over_text = myfont2.render("GAME OVER", False, (0, 0, 0))
        replay_text = myfont.render("Press \"SPACE\" to play again", True, (0, 0, 0))
        screen.blit(surface, (0,0))
        screen.blit(text, (10, 10))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HIGHT // 2 - game_over_text.get_height() // 2))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HIGHT //2 + 15 +replay_text.get_height() // 2))
        pygame.display.update()

main()
