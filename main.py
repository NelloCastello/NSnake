import pygame
import sys
import random

FRAME_SIZE = 600, 600
FPS = 5
CELL_SIZE = 20
BG_COLOR = pygame.Color(0, 0, 0)

TURN_UP = 0
TURN_DOWN = 1
TURN_LEFT = 2
TURN_RIGHT = 3

clock = pygame.time.Clock()
direction = TURN_RIGHT
snake = []
food = []


def draw_cells(__field):
    color = pygame.Color(5, 5, 5)
    for x in range(CELL_SIZE, FRAME_SIZE[0], CELL_SIZE):
        pygame.draw.line(__field, color,
                         (x, 0),
                         (x, FRAME_SIZE[1]))

    for y in range(CELL_SIZE, FRAME_SIZE[1], CELL_SIZE):
        pygame.draw.line(__field, color,
                         (0, y),
                         (FRAME_SIZE[1], y))


def draw_snake(__field):
    for i in snake:
        pygame.draw.rect(__field, (0, 255, 0), (
            i[0]-CELL_SIZE, i[1]-CELL_SIZE, CELL_SIZE, CELL_SIZE
        ))


def draw_food(__field):
    pygame.draw.rect(__field, (255, 255, 255), (
        food[0]-CELL_SIZE, food[1]-CELL_SIZE, CELL_SIZE, CELL_SIZE
    ))


def spawn_snake():
    position = random.randint(1, FRAME_SIZE[0]//CELL_SIZE)*CELL_SIZE,\
               random.randint(1, FRAME_SIZE[1]//CELL_SIZE)*CELL_SIZE

    snake.clear()
    snake.append(list(position))


def spawn_food():
    global food
    while True:
        food = [random.randint(1, FRAME_SIZE[0] // CELL_SIZE) * CELL_SIZE,
                random.randint(1, FRAME_SIZE[1] // CELL_SIZE) * CELL_SIZE]
        if snake[0][0] != food[0] and snake[0][1] != food[1]:
            break


def enlarge_snake():
    position = snake[0].copy()
    snake.insert(0, position)


def move_snake(__direction):
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = snake[i-1].copy()
    if __direction == TURN_UP:
        snake[0][1] -= CELL_SIZE
    elif __direction == TURN_DOWN:
        snake[0][1] += CELL_SIZE
    elif __direction == TURN_LEFT:
        snake[0][0] -= CELL_SIZE
    elif __direction == TURN_RIGHT:
        snake[0][0] += CELL_SIZE


def did_eat_food():
    if snake[0][0] == food[0] and snake[0][1] == food[1]:
        return True
    else:
        return False


def is_over():
    if snake[0][0] > FRAME_SIZE[0] or snake[0][0] < 1 or \
            snake[0][1] > FRAME_SIZE[1] or snake[0][1] < 1:
        return True

    for i in range(2, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True

    return False


def run():
    check_errors = pygame.init()
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

    pygame.display.set_caption("NSnake")
    frame = pygame.display.set_mode(FRAME_SIZE)

    spawn_snake()
    spawn_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                global direction
                if event.key == pygame.K_UP or event.key == ord('w'):
                    if direction != TURN_DOWN:
                        direction = TURN_UP
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    if direction != TURN_UP:
                        direction = TURN_DOWN
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    if direction != TURN_RIGHT:
                        direction = TURN_LEFT
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    if direction != TURN_LEFT:
                        direction = TURN_RIGHT

        if did_eat_food():
            spawn_food()
            enlarge_snake()
        if is_over():
            spawn_snake()
            spawn_food()

        frame.fill(BG_COLOR)
        draw_cells(frame)
        move_snake(direction)
        draw_snake(frame)
        draw_food(frame)
        pygame.display.flip()

        clock.tick(FPS)


if __name__ == "__main__":
    run()
