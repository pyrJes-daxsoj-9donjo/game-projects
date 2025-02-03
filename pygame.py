import pygame
import random
import time

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)

# Размеры окна тут есть апскеил
WIDTH, HEIGHT = 1920, 1080

# Размер блока змейки и скорость
BLOCK_SIZE = 20
SPEED = 15

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Окно игры
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()

# отображения счета и жизней
def display_score_and_lives(score, lives):
    value = score_font.render("Опыт: " + str(score), True, YELLOW)
    win.blit(value, [10, 10])
    value = score_font.render("Жизни: " + str(lives), True, YELLOW)
    win.blit(value, [WIDTH - 150, 10])

#  отображения змейки
def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(win, GREEN, [block[0], block[1], block_size, block_size])

#  отображения врага
def draw_enemy(enemy_x, enemy_y):
    pygame.draw.rect(win, RED, [enemy_x, enemy_y, BLOCK_SIZE, BLOCK_SIZE])

#  отображения сообщения на экране
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH / 6, HEIGHT / 3])

#  генерации фруктов
def generate_fruit():
    fruit_type = random.choices(["apple", "pear", "plum"], weights=[70, 25, 5])[0]
    fruit_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    fruit_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    return fruit_type, fruit_x, fruit_y

#  отрисовки фруктов
def draw_fruit(fruit_type, fruit_x, fruit_y):
    if fruit_type == "apple":
        color = ORANGE
    elif fruit_type == "pear":
        color = YELLOW
    elif fruit_type == "plum":
        color = PURPLE
    pygame.draw.rect(win, color, [fruit_x, fruit_y, BLOCK_SIZE, BLOCK_SIZE])

#  генерации позиции врага
def generate_enemy():
    enemy_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    enemy_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    return enemy_x, enemy_y

#  отрисовки границ
def draw_borders():
    pygame.draw.rect(win, GRAY, [0, 0, WIDTH, BLOCK_SIZE])  # Верхняя граница
    pygame.draw.rect(win, GRAY, [0, HEIGHT - BLOCK_SIZE, WIDTH, BLOCK_SIZE])  # Нижняя граница
    pygame.draw.rect(win, GRAY, [0, 0, BLOCK_SIZE, HEIGHT])  # Левая граница
    pygame.draw.rect(win, GRAY, [WIDTH - BLOCK_SIZE, 0, BLOCK_SIZE, HEIGHT])  # Правая граница

# Основная функция игры
def game_loop():
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2

    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    fruit_type, fruit_x, fruit_y = generate_fruit()
    enemy_x, enemy_y = generate_enemy()
    enemy_direction = random.choice(["left", "right", "up", "down"])

    score = 0
    lives = 3

    while not game_over:

        while game_close:
            win.fill(BLACK)
            message("Вы проиграли! Нажмите Q-Выход или R-Играть снова", RED)
            display_score_and_lives(score, lives)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Проверка на выход за границы
        if x >= WIDTH - BLOCK_SIZE or x < BLOCK_SIZE or y >= HEIGHT - BLOCK_SIZE or y < BLOCK_SIZE:
            lives -= 1
            if lives == 0:
                game_close = True
            else:
                x = WIDTH / 2
                y = HEIGHT / 2
                x_change = 0
                y_change = 0
                snake_list = []
                length_of_snake = 1

        x += x_change
        y += y_change
        win.fill(BLACK)

        # Отрисовка границ
        draw_borders()

        # Отрисовка фруктов
        draw_fruit(fruit_type, fruit_x, fruit_y)

        # Движение врага
        if enemy_direction == "left":
            enemy_x -= BLOCK_SIZE
        elif enemy_direction == "right":
            enemy_x += BLOCK_SIZE
        elif enemy_direction == "up":
            enemy_y -= BLOCK_SIZE
        elif enemy_direction == "down":
            enemy_y += BLOCK_SIZE

        # Если враг выходит за границы, то он меняет направление (Хз правильно ли оно работает, но должно что-то делать)
        if enemy_x >= WIDTH - BLOCK_SIZE or enemy_x < BLOCK_SIZE or enemy_y >= HEIGHT - BLOCK_SIZE or enemy_y < BLOCK_SIZE:
            enemy_x, enemy_y = generate_enemy()
            enemy_direction = random.choice(["left", "right", "up", "down"])

        draw_enemy(enemy_x, enemy_y)

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                lives -= 1
                if lives == 0:
                    game_close = True
                else:
                    x = WIDTH / 2
                    y = HEIGHT / 2
                    x_change = 0
                    y_change = 0
                    snake_list = []
                    length_of_snake = 1

        # Проверка столкновения с врагом
        if x == enemy_x and y == enemy_y:
            lives -= 1
            if lives == 0:
                game_close = True
            else:
                enemy_x, enemy_y = generate_enemy()

        draw_snake(BLOCK_SIZE, snake_list)
        display_score_and_lives(score, lives)

        pygame.display.update()

        if x == fruit_x and y == fruit_y:
            if fruit_type == "apple":
                score += 1
            elif fruit_type == "pear":
                score += 2
            elif fruit_type == "plum":
                score += 5
            fruit_type, fruit_x, fruit_y = generate_fruit()
            length_of_snake += 1

        clock.tick(SPEED)

    pygame.quit()
    quit()

# Перезапуск игры
game_loop()