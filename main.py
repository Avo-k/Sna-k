import pygame
import random

from constants import *
from agents import Keyboard, Patient, Ravenous, BFS


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sna-k")
clock = pygame.time.Clock()


def draw_screen(s):
    """fill the screen and draw the grid"""
    s.fill(BLACK)
    for row in range(1, 11):
        pygame.draw.line(s, WHITE, (row * SQUARE, 0), (row * SQUARE, HEIGHT))
        pygame.draw.line(s, WHITE, (0, row * SQUARE), (WIDTH, row * SQUARE))


apple = Apple()
# snake = Keyboard()
# snake = Ravenous()
# snake = Patient()
snake = BFS()
ALL_SPRITES.add(apple)
ALL_SPRITES.add(snake)


#######################################
# Game loop
#######################################

running = True
while running:

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # check for keyboard input
        if event.type == pygame.KEYDOWN:
            snake.next_dir = event.key

    # Update all sprites
    ALL_SPRITES.update()

    # did the snake hit itself?
    if snake.rect.collidelist([bp.rect for bp in snake.body[1:]]) != -1:
        print("You tried to eat yourself")
        running = False

    # is the snake still in the screen?
    for i in range(2):
        if 0 > snake.rect.topleft[i] or snake.rect.topleft[i] > WIDTH - SQUARE:
            print("You went off screen")
            running = False

    # did the snake eat the apple?
    if snake.rect.center == apple.rect.center:
        occupied = {bp.rect.topleft for bp in snake.body}.union({snake.rect.topleft})
        if len(occupied) == 100:    # is the game won?
            running = False
        else:
            apple.rect.topleft = random.choice([sq for sq in ALL_SQUARES if sq not in occupied])
            snake.apple_pos = apple.rect.topleft
        snake.eat()

    # Draw screen and sprites
    draw_screen(screen)
    ALL_SPRITES.draw(screen)

    # flip the display
    pygame.display.flip()

print(f"Score is: {len(snake.body)}")
pygame.quit()
