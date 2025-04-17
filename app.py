import time
import sys
import os

from datetime import datetime
import time

test = False

if "--dev" in sys.argv:
    test = True

if test:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
    gpio_slow = 0
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

    gpio_slow = 3


class LEDMatrix(object):
    def __init__(self, *args, **kwargs):
        self.open = True


    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        cssc_open_font = graphics.Font()
        cssc_open_font.LoadFont("./fonts/5x8.bdf")
        other_font = graphics.Font()
        other_font.LoadFont("./fonts/6x12.bdf")

        clock_day_font = graphics.Font()
        clock_day_font.LoadFont("./fonts/6x9.bdf")

        clock_font = graphics.Font()
        clock_font.LoadFont("./fonts/5x8.bdf")

        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width


        while True:
            offscreen_canvas.Clear()
            if self.open:
                open_status = "Open"
                open_status_colour = graphics.Color(11,218,81)
            else:
                open_status = "Closed"
                open_status_colour = graphics.Color(220,20,60)
            graphics.DrawText(offscreen_canvas, other_font, 1, 16, graphics.Color(255,165,0), "CSSC:")
            graphics.DrawText(offscreen_canvas, cssc_open_font, 34, 16, open_status_colour, open_status)
            # _len = graphics.DrawText(offscreen_canvas, other_font, pos, 23, textColor, my_text)
            # pos -= 1
            # if (pos + _len < 0):
            #     pos = offscreen_canvas.width

            # time
            current_time = datetime.now().strftime('%H:%M:%S')
            current_day = ''.join(datetime.now().strftime('%A').strip()[0:3])

            graphics.DrawText(offscreen_canvas, clock_day_font, 1, 7, graphics.Color(255,165,0), current_day)
            graphics.DrawText(offscreen_canvas, clock_font, 23, 7, graphics.Color(255,165,0), current_time)


            time.sleep(0.05)
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
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

matrix = LEDMatrix()
matrix.process()