import time
import random
import threading
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


# Fake sensor functions
def read_temperature():
    return round(random.uniform(18.0, 30.0), 1)

def read_humidity():
    return round(random.uniform(30.0, 70.0), 1)

def read_co2():
    return random.randint(400, 1200)

# Shared data
temperature = 0
humidity = 0
co2 = 0

def update_sensors():
    global temperature, humidity, co2
    while True:
        temperature = read_temperature()
        humidity = read_humidity()
        co2 = read_co2()
        time.sleep(2)

class LEDMatrixWeather:
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

        # Fonts
        self.font_small = graphics.Font()
        self.font_small.LoadFont("./fonts/4x6.bdf")   # very compact
        self.font_normal = graphics.Font()
        self.font_normal.LoadFont("./fonts/5x8.bdf") # fits nicely

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()

        while True:
            offscreen_canvas.Clear()

            # Time + day (top line)
            now = datetime.now()
            time_str = now.strftime("%H:%M")
            day_str = now.strftime("%a")

            graphics.DrawText(offscreen_canvas, self.font_normal, 1, 7, graphics.Color(255, 165, 0), day_str)
            graphics.DrawText(offscreen_canvas, self.font_normal, 35, 7, graphics.Color(0, 255, 255), time_str)

            # Divider line
            graphics.DrawLine(offscreen_canvas, 0, 10, 63, 10, graphics.Color(255, 255, 255))

            # Temperature
            graphics.DrawText(offscreen_canvas, self.font_normal, 1, 20, graphics.Color(255, 255, 0), f"T:{temperature}C")

            # Humidity
            graphics.DrawText(offscreen_canvas, self.font_normal, 1, 28, graphics.Color(0, 255, 0), f"H:{humidity}%")

            # CO₂
            graphics.DrawText(offscreen_canvas, self.font_normal, 40, 20, graphics.Color(0, 200, 255), f"CO2")
            graphics.DrawText(offscreen_canvas, self.font_normal, 40, 28, graphics.Color(255, 255, 255), f"{co2}")

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(0.3)

# Start background thread for sensor updates
threading.Thread(target=update_sensors, daemon=True).start()

# Run the LED weather station
matrix = LEDMatrixWeather()
matrix.run()
