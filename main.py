import pygame
import sys
import random

FRAME_SIZE = 600, 600
MATRIX_SIZE = 15, 15
CELL_SIZE = FRAME_SIZE[0] // MATRIX_SIZE[0], FRAME_SIZE[1] // MATRIX_SIZE[1]
FPS = 5
BG_COLOR = (0, 0, 0)

LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"
NONE = "NONE"

snake = []
food = []
direction = NONE


def spawn_snake():
    x = random.randint(1, MATRIX_SIZE[0])
    y = random.randint(1, MATRIX_SIZE[1])
    snake.append([x, y])


def draw_cells(__container):
    for x in range(MATRIX_SIZE[0]):
        pygame.draw.line(__container, (40, 40, 40),
                         (x * CELL_SIZE[0], 0),
                         (x * CELL_SIZE[0], MATRIX_SIZE[1] * CELL_SIZE[1]))

    for y in range(MATRIX_SIZE[1]):
        pygame.draw.line(__container, (40, 40, 40),
                         (0, y * CELL_SIZE[1]),
                         (MATRIX_SIZE[0] * CELL_SIZE[0], y * CELL_SIZE[1]))


def enlarge_snake(__direction):
    left = -1, 0
    right = 1, 0
    up = 0, -1
    down = 0, 1

    position = snake[0].copy()
    if __direction == LEFT:
        position[0] += left[0]
        position[1] += left[1]
    elif __direction == RIGHT:
        position[0] += right[0]
        position[1] += right[1]
    elif __direction == UP:
        position[0] += up[0]
        position[1] += up[1]
    elif __direction == DOWN:
        position[0] += down[0]
        position[1] += down[1]

    snake.insert(0, position)


def spawn_food():
    global food
    for i in range(MATRIX_SIZE[0] * MATRIX_SIZE[1]):
        food = [random.randint(1, MATRIX_SIZE[0]), random.randint(1, MATRIX_SIZE[1])]
        for j in snake:
            if j[0] != food[0] and j[1] != food[1]:
                return


def draw_food(__container):
    pygame.draw.rect(__container, (255, 0, 0), (
        (food[0] - 1) * CELL_SIZE[0], (food[1] - 1) * CELL_SIZE[1],
        CELL_SIZE[0], CELL_SIZE[1]
    ))


def draw_snake(__container):
    pygame.draw.rect(__container, (0, 255, 255), (
        (snake[0][0] - 1) * CELL_SIZE[0], (snake[0][1] - 1) * CELL_SIZE[1],
        CELL_SIZE[0], CELL_SIZE[1]
    ))
    for i in snake:
        if snake[0] == i:
            continue
        pygame.draw.rect(__container, (0, 255, 0), (
            (i[0] - 1) * CELL_SIZE[0], (i[1] - 1) * CELL_SIZE[1],
            CELL_SIZE[0], CELL_SIZE[1]
        ))


def move_snake(__direction):
    left = -1, 0
    right = 1, 0
    up = 0, -1
    down = 0, 1

    snake_len = len(snake)

    if __direction != NONE:
        for i in range(snake_len - 1, 0, -1):
            snake[i][0] = snake[i - 1][0]
            snake[i][1] = snake[i - 1][1]

    if __direction == RIGHT:
        snake[0][0] += right[0]
        snake[0][1] += right[1]
    if __direction == LEFT:
        snake[0][0] += left[0]
        snake[0][1] += left[1]
    if __direction == UP:
        snake[0][0] += up[0]
        snake[0][1] += up[1]
    if __direction == DOWN:
        snake[0][0] += down[0]
        snake[0][1] += down[1]


def did_eat_food():
    if snake[0][0] == food[0] and snake[0][1] == food[1]:
        return True
    else:
        return False


def is_over():
    if snake[0][0] > MATRIX_SIZE[0] or snake[0][0] < 1 or \
            snake[0][1] > MATRIX_SIZE[1] or snake[0][1] < 1:
        return True
    for i in range(2, len(snake)-1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True


pygame.init()
frame = pygame.display.set_mode(FRAME_SIZE)
pygame.display.set_caption("NSnake")
clock = pygame.time.Clock()
spawn_snake()
spawn_food()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if direction != LEFT:
                    direction = RIGHT
            if event.key == pygame.K_LEFT:
                if direction != RIGHT:
                    direction = LEFT
            if event.key == pygame.K_UP:
                if direction != DOWN:
                    direction = UP
            if event.key == pygame.K_DOWN:
                if direction != UP:
                    direction = DOWN

    if did_eat_food():
        frame.fill(BG_COLOR)
        enlarge_snake(direction)
        spawn_food()
        draw_snake(frame)
        draw_food(frame)
    if is_over():
        snake.clear()
        spawn_snake()
        spawn_food()

    move_snake(direction)
    frame.fill(BG_COLOR)
    draw_cells(frame)
    draw_snake(frame)
    draw_food(frame)
    pygame.display.flip()
