import pygame
import math
from datetime import datetime

# to debug, we'll print to log
########## having issues with this, works on one machine but not another
# import sys
# sys.stdout = open('C:/breakout/output.txt', 'w')
# print('test')


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OFFWHITE = (237, 240, 245)
LIGHTBLUE = (73, 122, 204)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

points_dic = {1: WHITE, 2: GREEN, 3: RED}
target_dic = {}

def get_target_area(target_dic):
    target_area = {}
    for key in target_dic:
        upper_xy = (target_dic[key].x_pos, target_dic[key].y_pos)
        lower_xy = (target_dic[key].x_pos + target_dic[key].width, target_dic[key].y_pos + target_dic[key].height)
        target_area[key] = (upper_xy, lower_xy)
    return target_area


def initialize_screen(level=1):
    if level == 1:
        for i in range(10):
            target_dic[i] = Target(70 * i, 50, 1, i)


def populate_screen(level=1):
    for key in target_dic:
        target_dic[key].draw(screen)


class Target:
    def __init__(self, x_pos, y_pos, points, key, width=70, height=10):
        self.points = points
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = points_dic[self.points]
        self.key = key

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHTBLUE, [self.x_pos, self.y_pos, self.width, self.height])
        pygame.draw.rect(screen, self.color, [self.x_pos + 2, self.y_pos + 2, self.width - 4, self.height - 4])

    def collision(self):
        # print('collision! on key {}'.format(self.key))
        # print('upper x:{}, upper y:{}, lower x:{}, lower y:{}'.format(self.x_pos, self.y_pos, self.x_pos +
        #                                                               self.width, self.y_pos + self.height))
        self.points -= 1
        if self.points == 0:
            target_dic.pop(self.key)
            return
        self.color = points_dic[self.points]


class Paddle:
    def __init__(self, x_pos=300, y_pos=400, width=100, height=10, color=WHITE):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.speed = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos, self.width, self.height])

    def move(self):
        self.x_pos = self.x_pos + self.speed
        if self.x_pos <= 0:
            self.x_pos = 0
        if self.x_pos >= 700 - self.width:
            self.x_pos = 700 - self.width

class Ball:
    def __init__(self, x_pos=200, y_pos=200, width=10, height=10, color=WHITE, speed=3, angle=.75*math.pi):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.speed = [speed*math.cos(angle), speed*math.sin(angle)]
        self.angle = angle

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos, self.width, self.height])

    def move(self):
        self.x_pos = self.x_pos + self.speed[0]*math.cos(self.angle)
        self.y_pos = self.y_pos + self.speed[1]*math.sin(self.angle)
        if self.x_pos <= 0:
            self.x_pos = 0
        if self.x_pos >= 700 - self.width:
            self.x_pos = 700 - self.width
        if self.x_pos >= 700 - self.width or self.x_pos <= 0:
            self.speed[0] = self.speed[0] * -1
        if self.y_pos <= 0:
            self.y_pos = 0
        if self.y_pos >= 500 - self.width:
            self.y_pos = 500 - self.width
        if self.y_pos >= 500 - self.width or self.y_pos <= 0:
            self.speed[1] = self.speed[1] * -1


def check_paddle(paddle, ball):
    if (paddle.x_pos - ball.width <= ball.x_pos <= paddle.x_pos + paddle.width) and ball.y_pos + ball.height >= paddle.y_pos:
        ball.speed[1] *= -1


def check_target(target_area, ball):
    collision = False
    for key in list(target_dic.keys()):
        if (target_dic[key].x_pos - ball.width <= ball.x_pos <= target_dic[key].x_pos + ball.width + target_dic[key].width) \
                and ball.y_pos <= target_dic[key].y_pos + target_dic[key].height:
            # print('collision detected')
            # print('ball location: x_pos = {}, y_pos = {}'.format(ball.x_pos, ball.y_pos))
            # print('test used to detect collision:')
            # print('(target_dic[key].x_pos - ball.width <= ball.x_pos <= target_dic[key].x_pos + paddle.width) and ball.y_pos <= target_dic[key].y_pos + target_dic[key].height')
            # print('subbed values:')
            # print('{} - {} <= {} <= {} + {}) and {} <= {} + {}'.format(target_dic[key].x_pos, ball.width, ball.x_pos, target_dic[key].x_pos, paddle.width, ball.y_pos, target_dic[key].y_pos, target_dic[key].height))
            target_dic[key].collision()
            collision = True
    return collision


# Setup

pygame.init()

# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

paddle = Paddle()
ball = Ball()
initialize_screen(1)
i = 0
# -------- Main Program Loop -----------
while not done:
    i += 1
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                paddle.speed = -6
            elif event.key == pygame.K_RIGHT:
                paddle.speed = 6

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle.speed = 0

    # --- Game Logic
    target_area = get_target_area(target_dic)

    # Move the object according to the speed vector.
    paddle.move()
    # ball.move()
    check_paddle(paddle, ball)
    result = check_target(target_area, ball)
    if result:
        # print('flipped')
        ball.speed[1] *= -1
    ball.move()


    # --- Drawing Code

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    populate_screen(1)
    paddle.draw(screen)
    ball.draw(screen)


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # for debugging, we want to print

    # if i % 5 == 0:
    #     dateTimeObj = datetime.now()
    #     timestampStr = dateTimeObj.strftime("%m_%d_%Y_%H_%M_%S_%f")
    #     print('{}, x: {}, y: {}'.format(timestampStr, ball.x_pos, ball.y_pos))
    #     pygame.image.save(screen, "C:/breakout/screenshot" + timestampStr + ".jpg")

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()