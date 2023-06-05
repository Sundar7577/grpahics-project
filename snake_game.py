import pygame
import time
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height), DOUBLEBUF | OPENGL)

pygame.display.set_caption('Obstacle touching and scoring game')

clock = pygame.time.Clock()

gluOrtho2D(0, dis_width, 0, dis_height)
glClearColor(0.0, 0.0, 0.0, 1.0)

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def draw_text(text, font, color, x, y):
    glColor3f(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    text_data = pygame.image.tostring(text_surface, 'RGBA', True)
    glRasterPos2d(x - text_rect.width / 2, y - text_rect.height / 2)
    glDrawPixels(text_rect.width, text_rect.height,
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_snake(snake_list, length_of_snake, game_close):
    for x, y in snake_list:
        glRectf(x, y, x + snake_block, y + snake_block)

    if game_close:
        draw_text("Your Score: " + str(length_of_snake - 1),
                  score_font, yellow, dis_width // 2, dis_height // 2 + 100)
    else:
        draw_text("Your Score: " + str(length_of_snake - 1),
                  score_font, yellow, 50, 20)


def game_over_screen(score):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reset the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, dis_width, 0, dis_height)

    # Reset the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Clear the color buffer
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Fill the screen with black color
    glRectf(0, 0, dis_width, dis_height)

    # Set up the text surface and position
    text_surface = score_font.render("Game Over!", True, red)
    text_rect = text_surface.get_rect(
        center=(dis_width // 2, dis_height // 2 - 50))

    # Blit the text surface onto the screen
    dis.blit(text_surface, text_rect)

    # Set up the score surface and position
    score_surface = score_font.render(
        "Your Score: " + str(score), True, yellow)
    score_rect = score_surface.get_rect(
        center=(dis_width // 2, dis_height // 2))

    # Blit the score surface onto the screen
    dis.blit(score_surface, score_rect)

    # Set up the instruction surface and position
    instruction_surface = font_style.render(
        "Press C to Play Again or Q to Quit", True, yellow)
    instruction_rect = instruction_surface.get_rect(
        center=(dis_width // 2, dis_height // 2 + 50))

    # Blit the instruction surface onto the screen
    dis.blit(instruction_surface, instruction_rect)

    pygame.display.flip()


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width // 2
    y1 = dis_height // 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            game_over_screen(length_of_snake - 1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = -snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 1.0, 1.0)
        glRectf(foodx, foody, foodx + snake_block, foody + snake_block)
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list, length_of_snake, game_close)
        draw_text("Your Score: " + str(length_of_snake - 1),
                  score_font, yellow, 50, 20)

        pygame.display.flip()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(
                0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(
                0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
