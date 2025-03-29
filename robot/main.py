from RpiMotorLib import A4988Nema
import math
from threading import Thread
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


PIXEL_SIZE = 3  # мм
GAP_SIZE = 2  # мм
STEP_PER_MM = 6.37  # шагов на 1 мм

GRID_SIZE = PIXEL_SIZE + GAP_SIZE

x1, y1 = 0, 0
x2, y2 = 184, 152

MOTOR1_GPIO_PINS = (7, 8, 25)
MOTOR1_DIRECTION = 20
MOTOR1_STEP = 21
MOTOR1 = A4988Nema(MOTOR1_DIRECTION, MOTOR1_STEP, MOTOR1_GPIO_PINS, "A4988")

MOTOR2_GPIO_PINS = (9, 10, 11)
MOTOR2_DIRECTION = 19
MOTOR2_STEP = 26
MOTOR2 = A4988Nema(MOTOR2_DIRECTION, MOTOR2_STEP, MOTOR2_GPIO_PINS, "A4988")

global_start_x = 54
global_start_y = 84


def move_to_xy(x_curr, y_curr, x, y):
    """Перемещает маркер из (x_curr, y_curr) в (x, y) с учетом рабочей области."""

    x_curr_real = global_start_x + x_curr * GRID_SIZE
    y_curr_real = global_start_y - y_curr * GRID_SIZE

    x_real = global_start_x + x * GRID_SIZE
    y_real = global_start_y - y * GRID_SIZE

    r1_curr = math.sqrt((x_curr_real - x1) ** 2 + (y_curr_real - y1) ** 2)
    r2_curr = math.sqrt((x_curr_real - x2) ** 2 + (y_curr_real - y2) ** 2)

    r1_new = math.sqrt((x_real - x1) ** 2 + (y_real - y1) ** 2)
    r2_new = math.sqrt((x_real - x2) ** 2 + (y_real - y2) ** 2)

    steps1 = int((r1_new - r1_curr) * STEP_PER_MM)
    steps2 = int((r2_new - r2_curr) * STEP_PER_MM)

    steps1 = -steps1
    steps2 = -steps2

    motor1_thread = Thread(target=lambda: MOTOR1.motor_go(steps1 > 0, "Full", abs(steps1), 0.001, False))
    motor2_thread = Thread(target=lambda: MOTOR2.motor_go(steps2 > 0, "Full", abs(steps2), 0.001, False))

    motor1_thread.start()
    motor2_thread.start()

    motor1_thread.join()
    motor2_thread.join()


def process_commands():
    x_curr = 0
    y_curr = 0
    print('Processing commands...')
    while True:
        command = redis_client.lpop("command_queue")
        if command:
            x, y, color = command.decode().split(",")
            x, y = map(int, (x, y))

            move_to_xy(x_curr, y_curr, x, y)
            x_curr = x
            y_curr = y


if __name__ == "__main__":
    process_commands()
