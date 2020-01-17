import pygame
import math


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


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
    def __init__(self, x_pos=200, y_pos=200, width=10, height=10, color=WHITE, speed=5, angle=.75*math.pi):
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
    if (paddle.x_pos - ball.width <= ball.x_pos <= paddle.x_pos + paddle.width) and ball.y_pos >= paddle.y_pos:
        ball.speed[1] *= -1



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

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                paddle.speed = -3
            elif event.key == pygame.K_RIGHT:
                paddle.speed = 3

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle.speed = 0

    # --- Game Logic

    # Move the object according to the speed vector.
    paddle.move()
    ball.move()
    check_paddle(paddle, ball)

    # --- Drawing Code

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    paddle.draw(screen)
    ball.draw(screen)


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()