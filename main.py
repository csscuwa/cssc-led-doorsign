import time
import sys
import os

import requests

import threading

from datetime import datetime
import time

import dotenv

dotenv.load_dotenv()

password = os.getenv('PASSWORD')

# Variables

gpio_slow = 4

# Dev Mode
if "--dev" in sys.argv:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
    gpio_slow = 0
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

door_status = None

def door_status():
    global door_status
    s = requests.Session()

    r = s.post('https://portal.cssc.asn.au/api/auth', data={'password': 'SussyDigger12'})

    print(r.json())

    while True:
        json_data = s.get("https://portal.cssc.asn.au/api/door_status").json()
        if json_data["door_open"]:
            door_status = True
        else:
            door_status = False
        print(door_status)

        time.sleep(5)


class LEDMatrix():
    def __init__(self, *args, **kwargs):
        self.open = True


    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        cssc_open_font = graphics.Font()
        cssc_open_font.LoadFont("./fonts/5x8.bdf")
        cssc_font = graphics.Font()
        cssc_font.LoadFont("./fonts/6x12.bdf")

        clock_day_font = graphics.Font()
        clock_day_font.LoadFont("./fonts/6x9.bdf")

        clock_font = graphics.Font()
        clock_font.LoadFont("./fonts/5x8.bdf")

        scroll_font = graphics.Font()
        scroll_font.LoadFont("./fonts/6x13.bdf")

        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width


        while True:
            offscreen_canvas.Clear()

            # CSSC DOOR STATUS
            if door_status:
                open_status = "Open"
                open_status_colour = graphics.Color(11,218,81)
            else:
                open_status = "Closed"
                open_status_colour = graphics.Color(220,20,60)
            graphics.DrawText(offscreen_canvas, cssc_font, 1, 16, graphics.Color(255,165,0), "CSSC:")
            graphics.DrawText(offscreen_canvas, cssc_open_font, 34, 16, open_status_colour, open_status)

            # time
            current_time = datetime.now().strftime('%H:%M:%S')
            current_day = ''.join(datetime.now().strftime('%A').strip()[0:3])

            graphics.DrawText(offscreen_canvas, clock_day_font, 1, 7, graphics.Color(255,165,0), current_day)
            graphics.DrawText(offscreen_canvas, clock_font, 23, 7, graphics.Color(255,165,0), current_time)

            #
            graphics.DrawLine(offscreen_canvas, 0, 18, 64, 18, graphics.Color(255, 90, 0))

            _len = graphics.DrawText(offscreen_canvas, scroll_font, pos, 30, textColor, "HAII NANI GA SUKI?? Study well for your exams!! Come to our CSSC Monthly BBQs ")
            pos -= 1
            if (pos + _len < 0):
                pos = offscreen_canvas.width



            time.sleep(0.019)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def process(self):
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

        options.gpio_slowdown = gpio_slow

        options.disable_hardware_pulsing = True

        options.drop_privileges=True

        self.matrix = RGBMatrix(options = options)

        try:
            # Start loop
            print("Press CTRL-C to stop app")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

matrix = LEDMatrix()

threading.Thread(target=door_status).start()
matrix.process()
