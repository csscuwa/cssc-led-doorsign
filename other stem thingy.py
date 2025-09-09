import time
import random
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# --- Game Config ---
WIDTH = 64
HEIGHT = 32
CELL_SIZE = 2  # snake block size

# --- Snake Game ---
class SnakeGame:
    def __init__(self):
        options = RGBMatrixOptions()
        options.hardware_mapping = "regular"
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.panel_type = ""

        options.show_refresh_rate = 0

        options.gpio_slowdown = 4

        options.disable_hardware_pulsing = True

        options.drop_privileges = True

        self.matrix = RGBMatrix(options=options)
        self.offscreen = self.matrix.CreateFrameCanvas()

        self.snake = [(10, 10), (8, 10), (6, 10)]
        self.direction = (2, 0)
        self.food = self.spawn_food()
        self.score = 0

    def spawn_food(self):
        while True:
            fx = random.randrange(0, WIDTH, CELL_SIZE)
            fy = random.randrange(0, HEIGHT, CELL_SIZE)
            if (fx, fy) not in self.snake:
                return (fx, fy)

    def ai_choose_direction(self):
        """Very simple AI: go toward food, else random safe turn."""
        head_x, head_y = self.snake[0]
        fx, fy = self.food

        preferred = []
        if fx > head_x:
            preferred.append((2, 0))   # move right
        elif fx < head_x:
            preferred.append((-2, 0))  # move left
        if fy > head_y:
            preferred.append((0, 2))   # move down
        elif fy < head_y:
            preferred.append((0, -2))  # move up

        # add all possible moves to consider
        all_dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        moves = preferred + [d for d in all_dirs if d not in preferred]

        # pick first safe move
        for dx, dy in moves:
            nx, ny = head_x + dx, head_y + dy
            if (0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in self.snake):
                self.direction = (dx, dy)
                return

        # fallback (snake is trapped)
        self.direction = random.choice(all_dirs)

    def update(self):
        self.ai_choose_direction()
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # check walls or self-collision
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake):
            return False  # game over

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        return True

    def draw_block(self, x, y, color):
        for i in range(CELL_SIZE):
            for j in range(CELL_SIZE):
                self.offscreen.SetPixel(x + i, y + j, *color)

    def draw(self):
        self.offscreen.Clear()

        # draw snake
        for i, (x, y) in enumerate(self.snake):
            color = (0, 255, 0) if i > 0 else (0, 180, 255)  # head blueish
            self.draw_block(x, y, color)

        # draw food
        fx, fy = self.food
        self.draw_block(fx, fy, (255, 0, 0))

        # draw score
        font = graphics.Font()
        font.LoadFont("./fonts/4x6.bdf")
        graphics.DrawText(self.offscreen, font, 1, 7, graphics.Color(255, 255, 0), f"S:{self.score}")

        self.offscreen = self.matrix.SwapOnVSync(self.offscreen)

    def run(self):
        try:
            while True:
                alive = self.update()
                if not alive:
                    print("Game Over! Final Score:", self.score)
                    sys.exit(0)
                self.draw()
                time.sleep(0.12)
        except KeyboardInterrupt:
            print("Exiting Snake")
            sys.exit(0)

# --- Run ---
if __name__ == "__main__":
    SnakeGame().run()
