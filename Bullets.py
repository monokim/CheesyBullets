import random
import math
import pygame
import numpy as np

screen_width = 768
screen_height = 768

class Tank:
    size = 10
    alive = True
    def __init__(self, screen):
        self.screen = screen
        self.position = [screen_width / 2, screen_height / 2]
        self.color = (0, 0, 255)

    def update(self, pos):
        tmp_pos_x = self.position[0] + pos[0]
        tmp_pos_y = self.position[1] + pos[1]
        if tmp_pos_x < 20 or tmp_pos_x > screen_width - 20 or tmp_pos_y < 20 or tmp_pos_y > screen_height - 20:
            pass
        else:
            self.position = [tmp_pos_x, tmp_pos_y]

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)

class Bullet:
    size = 5
    alive = True
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 0, 0)
        #random position
        self.position = [0, 0]
        self.angle = 0
        choice = random.randint(0, 3)
        if choice == 0:
            self.position = [1, 1]
            self.angle = random.randint(270, 360)
        elif choice == 1:
            self.position = [screen_width - 1, 1]
            self.angle = random.randint(180, 270)
        elif choice == 2:
            self.position = [1, screen_height - 1]
            self.angle = random.randint(0, 90)
        elif choice == 3:
            self.position = [screen_width - 1,  screen_height - 1]
            self.angle = random.randint(90, 180)
        #random speed
        self.speed = random.randint(3, 5)

    def update(self, pos):
        self.position[0] = self.position[0] + math.cos(math.radians(self.angle)) * self.speed
        self.position[1] = self.position[1] - math.sin(math.radians(self.angle)) * self.speed

        if self.position[0] < 0 or self.position[0] > screen_width or self.position[1] < 0 or self.position[1] > screen_height:
            self.alive = False

        if get_distance(self.position, pos) < 5:
            return True

        return False

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)


def get_distance(p1, p2):
	return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))

def run():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    tank = Tank(screen)
    done = False
    speed = 5
    bullets = []
    num_bullets = 100
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tank.update([-speed, 0])
        if keys[pygame.K_RIGHT]:
            tank.update([speed, 0])
        if keys[pygame.K_UP]:
            tank.update([0, -speed])
        if keys[pygame.K_DOWN]:
            tank.update([0, speed])

        if len(bullets) == 0:
            for i in range(num_bullets):
                bullets.append(Bullet(screen))

        for i, b in enumerate(bullets):
            if b.alive == False:
                del bullets[i]
            else:
                b.update(tank.position)

        #screen.fill((255, 255, 255))
        #tank.draw()
        #for i, b in enumerate(bullets):
            #b.draw()

        arr = pygame.surfarray.pixels3d(screen)
        gray = np.dot(arr, [0.2126, 0.7152, 0.0722])
        print(gray[0])

        print(gray.shape)
        pygame.display.flip()
        clock.tick(60)
run()
