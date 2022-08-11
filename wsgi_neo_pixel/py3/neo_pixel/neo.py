"""The neo pixel defaults/connection object"""

import board
import neopixel


# NeoPixel config
PX_PIN = board.D18
NUM_PX = 30
ORDER = neopixel.GRB
AUTO_WRITE = False


def create_neo_pixel(brightness: float = 0.0) -> object:
    """
    Creates the Neo pixel object and returns it

    Args:
        brightness (float): 0 - 1.0

    Returns:
        object: The NeoPixel object
    """
    return neopixel.NeoPixel(PX_PIN, NUM_PX, auto_write=AUTO_WRITE, pixel_order=ORDER, brightness=brightness)
