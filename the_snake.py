from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    position = (0, 0)
    body_color = (255, 255, 255)

    def __init__(self, position=None, color=None):
        if position is None:
            position = self.position
        if color is None:
            color = self.body_color

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        raise NotImplementedError("Метод 'draw' реализован в подклассе.")


class Apple(GameObject):
    """Реализвция класса для Яблока"""

    APPLE_COLOR = (255, 0, 0)

    def __init__(self, snake=None):
        self.snake = snake if snake else Snake()
        self.position = self.randomize_position()
        super().__init__(self.position, self.APPLE_COLOR)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE,
        )
        pg.draw.rect(screen, self.APPLE_COLOR, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Обновляет позицию яблока."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in self.snake.positions:
                return position
            return self.randomize_position()


class Snake(GameObject):
    """Класс для Змейки."""

    def __init__(self):
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(position=self.positions[0], color=self.body_color)

    def update_direction(self):
        """Обновляет направление движения Змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )

        """Обработка столкновения с границами."""

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for pos in self.positions:
            rect = pg.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для изменения направления."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()

        # Проверка на поглащение яблока.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        """Проверка на столкновение в свое тело."""
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        """Проверка на столкновение с границами."""
        head_x, head_y = snake.get_head_position()
        if (
            head_x < 0 or head_x >= SCREEN_WIDTH
            or head_y < 0 or head_y >= SCREEN_HEIGHT
        ):
            snake.reset()
        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
