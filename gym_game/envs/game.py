import numpy as np
import time
import random
import math
import pygame
import cv2

screen_width = 768
screen_height = 768

class Player:
    size = 8
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
        self.color = (255, 255, 50)
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
            self.alive = False
            return True

        return False

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)

class Game:
    def __init__(self, is_render = True):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.SysFont("Arial", 150)
        self.game_speed = 60
        self.player = Player(self.screen)
        self.bullets = []
        self.num_bullets = 200
        self.is_render = is_render

    def action(self, action):
        # do action
        speed = 3
        if action == 0:
            self.player.update([-speed, 0])
        elif action == 1:
            self.player.update([speed, 0])
        elif action == 2:
            self.player.update([0, -speed])
        elif action == 3:
            self.player.update([0, speed])

        for i, b in enumerate(self.bullets):
            if b.alive == False:
                del self.bullets[i]
            else:
                if b.update(self.player.position):
                    self.player.alive = False

        if len(self.bullets) < 100:
            for i in range(self.num_bullets):
                self.bullets.append(Bullet(self.screen))

    def evaluate(self):
        # return reward
        reward = 0.1
        if not self.player.alive:
            reward -= 100
        return reward

    def is_done(self):
        # return episode is done or not
        return not self.player.alive

    def observe(self):
        # return observation data
        pass

    def view(self):
        # render game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

        self.screen.fill((0, 0, 0))
        self.player.draw()
        for i, b in enumerate(self.bullets):
            b.draw()
        #pos = screen_width - 25, 50
        #for i in range(self.player.hit_count):
            #pygame.draw.circle(self.screen, (255, 0, 0), [pos[0] - i * 25, pos[1]], 10)
        pygame.display.flip()
        self.clock.tick(150)

    def get_screen(self):
        size = (64, 64)
        arr = pygame.surfarray.pixels3d(self.screen)
        image = cv2.resize(arr, size).transpose((2, 0, 1))
        image = np.ascontiguousarray(image, dtype=np.float32) / 255
        return image


def get_distance(p1, p2):
	return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))
